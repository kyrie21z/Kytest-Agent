"""Agent 状态：规范消息历史 + 上下文预算裁剪。

裁剪是这里唯一有难度的地方。核心约束来自 OpenAI 兼容 API 的硬性要求：

    role="tool" 的消息必须紧跟在带 tool_calls 的 assistant 消息之后。

如果按"滑动窗口"从中间截断，就会出现孤立的 tool 消息，API 直接返回 400。
Pi 用 `convertToLlm` 解决这个问题；我们用**按组裁剪**解决：

    一个组 = 一条 user 消息，或一条 assistant 消息 + 它触发的全部 tool 消息

裁剪以组为单位进行，结构上不可能切出孤立的 tool 消息。若单个组本身就超出预算，
则对组内超长内容做**保留头尾的截断**，并在截断处留下明确标记——这样模型知道
自己漏看了内容（Pi 的 compaction 用摘要回注达到类似效果，我们用它 1% 的复杂度）。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..message import AssistantMessage, Usage

# 组内单条消息超长时的保留头尾比例
_HEAD_RATIO = 0.6
_MIN_TAIL_CHARS = 200
_TRUNCATION_NOTE = "\n...[内容过长已折叠 {dropped} 字符]...\n"


def estimate_chars(text: Any) -> int:
    """粗略估算一次 LLM 请求的字符量。字符数是最省事且无依赖的预算单位。"""
    if text is None:
        return 0
    if isinstance(text, str):
        return len(text)
    if isinstance(text, dict):
        total = 0
        for key, value in text.items():
            total += len(str(key)) + estimate_chars(value)
        return total
    if isinstance(text, (list, tuple)):
        return sum(estimate_chars(item) for item in text)
    return len(str(text))


def clamp_text(text: str, limit: int) -> str:
    """保留头尾地截断超长文本，中间插入可读的省略标记。"""
    if limit <= 0 or len(text) <= limit:
        return text
    head = int(limit * _HEAD_RATIO)
    tail = max(_MIN_TAIL_CHARS, limit - head)
    if head + tail >= len(text):
        return text
    dropped = len(text) - head - tail
    return text[:head] + _TRUNCATION_NOTE.format(dropped=dropped) + text[-tail:]


def group_messages(messages: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """把消息切成不可分割的组：assistant 与其后续 tool 消息同组。"""
    groups: List[List[Dict[str, Any]]] = []
    for message in messages:
        role = message.get("role")
        if role == "tool" and groups and any(m.get("role") == "assistant" for m in groups[-1]):
            groups[-1].append(message)
        else:
            groups.append([message])
    return groups


def trim_messages(messages: List[Dict[str, Any]], max_chars: int) -> List[Dict[str, Any]]:
    """按字符预算裁剪消息，保证 assistant/tool 配对完整。

    保留策略（按优先级）：
    1. 第一条消息是任务描述，丢了这个 run 就没有意义——即使超预算也必须留下；
    2. 带工具调用的 assistant 组整体保留或整体丢弃，绝不切出孤立的 tool 消息；
    3. 从最新一组往前保留，直到预算用尽；
    4. 若仍超预算，对保留组内的超长内容做头尾截断。

    因此返回值是"预算软约束 + 两条硬优先级"，而不是严格小于 max_chars。
    """
    if not messages or max_chars <= 0:
        return list(messages)

    first = messages[0]
    rest = messages[1:]
    budget = max(200, max_chars - estimate_chars(first))
    groups = group_messages(rest) if rest else []
    sizes = [sum(estimate_chars(m) for m in group) for group in groups]

    # 最新一组无论如何都保留——它是"刚刚发生了什么"，丢掉它比超预算更糟。
    keep_from = max(0, len(groups) - 1)
    used = sizes[keep_from] if groups else 0
    for index in range(len(groups) - 2, -1, -1):
        if used + sizes[index] > budget:
            break
        used += sizes[index]
        keep_from = index

    kept = [first] + [message for group in groups[keep_from:] for message in group]

    # 兜底：即使只剩最新一组也放不下，就对超长内容做头尾截断。
    total = sum(estimate_chars(m) for m in kept)
    if total > max_chars:
        allowance = max(200, max_chars // len(kept))
        clamped: List[Dict[str, Any]] = []
        for message in kept:
            clone = dict(message)
            content = clone.get("content")
            if isinstance(content, str):
                clone["content"] = clamp_text(content, allowance)
            elif content is not None:
                clone["content"] = clamp_text(str(content), allowance)
            clamped.append(clone)
        kept = clamped

    return kept


@dataclass
class AgentState:
    """一个 Agent 运行期的全部可变状态。计数器只增不减，便于成本分析。"""

    system_prompt: str = ""
    messages: List[Dict[str, Any]] = field(default_factory=list)

    # 工具调用的元数据（是否出错、是否请求终止）。**不放进 messages**，
    # 因为 messages 会被原样发给 LLM，多出的字段是非法的 API 载荷。
    tool_meta: List[Dict[str, Any]] = field(default_factory=list)

    turn_index: int = 0
    llm_calls: int = 0
    tool_calls: int = 0
    tool_errors: int = 0
    # 因模型输出被 token 上限截断而未执行的工具调用数。单独计数，
    # 因为它属于"模型输出不完整"，不属于"工具失败"，两者在失败分类里是不同类别。
    tool_calls_skipped: int = 0
    usage: Usage = field(default_factory=Usage)

    started_at: float = 0.0
    finished_at: float = 0.0

    # ------------------------------------------------------------------
    # 写入
    # ------------------------------------------------------------------
    def add_user(self, content: str) -> Dict[str, Any]:
        message = {"role": "user", "content": content}
        self.messages.append(message)
        return message

    def add_assistant(self, message: AssistantMessage) -> Dict[str, Any]:
        """把 LLM 返回的消息转成规范历史格式（OpenAI 兼容形状）。"""
        record: Dict[str, Any] = {"role": "assistant", "content": message.text}
        calls = [
            {
                "id": block.id,
                "type": "function",
                "function": {"name": block.name, "arguments": block.arguments},
            }
            for block in message.tool_calls
        ]
        if calls:
            record["tool_calls"] = calls
        self.messages.append(record)
        return record

    def add_tool_result(self, call_id: str, name: str, content: str) -> Dict[str, Any]:
        record = {
            "role": "tool",
            "tool_call_id": call_id,
            "name": name,
            "content": content,
        }
        self.messages.append(record)
        return record

    def record_tool_meta(
        self, call_id: str, name: str, is_error: bool, terminate: bool = False
    ) -> Dict[str, Any]:
        meta = {
            "id": call_id,
            "name": name,
            "is_error": is_error,
            "terminate": terminate,
        }
        self.tool_meta.append(meta)
        return meta

    # ------------------------------------------------------------------
    # 读取
    # ------------------------------------------------------------------
    def build_request_messages(self, max_chars: int) -> List[Dict[str, Any]]:
        """返回可直接发给 LLM 的消息列表（含 system，已按预算裁剪）。"""
        system = {"role": "system", "content": self.system_prompt}
        if not self.messages:
            return [system]
        budget = max(500, max_chars - estimate_chars(self.system_prompt))
        return [system] + trim_messages(self.messages, budget)

    def last_assistant(self) -> Optional[Dict[str, Any]]:
        for message in reversed(self.messages):
            if message.get("role") == "assistant":
                return message
        return None

    def pending_tool_calls(self) -> List[Dict[str, Any]]:
        """返回最后一条 assistant 消息里尚未配对 tool 结果的调用。

        正常情况下永远为空；非空意味着消息序列不合法，是必须暴露的 bug 而非静默容忍。
        """
        answered = {
            message.get("tool_call_id")
            for message in self.messages
            if message.get("role") == "tool"
        }
        assistant = self.last_assistant() or {}
        return [
            call
            for call in (assistant.get("tool_calls") or [])
            if call.get("id") not in answered
        ]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "turn_index": self.turn_index,
            "llm_calls": self.llm_calls,
            "tool_calls": self.tool_calls,
            "tool_errors": self.tool_errors,
            "tool_calls_skipped": self.tool_calls_skipped,
            "usage": self.usage.to_dict(),
            "messages": self.messages,
            "tool_meta": self.tool_meta,
        }
