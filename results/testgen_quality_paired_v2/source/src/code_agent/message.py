"""消息与用量类型：Agent 循环与 LLM 层之间的唯一契约。

设计决定（对照 Pi Agent 的 `packages/ai/src/types.ts`）：

1. **工具调用是 content block 的一种，而不是与文本平行的字段**。
   `AssistantMessage.content` 是有序的 `TextBlock | ToolCallBlock` 列表，
   与模型实际生成顺序一致。好处：文本里出现 `{"name": ..., "arguments": ...}`
   这类伪造内容时，永远不会被误当成工具调用——纯文本协议最典型的失败模式被结构性排除。
2. **只有一种消息形态**，非流式与将来的流式共用。加流式时只需要多一个适配器，
   不需要改动 Agent 循环。
3. `arguments` 在 `ToolCallBlock` 里是**已解析的 dict**。非流式响应天然是完整 JSON，
   因此本层不需要"半截 JSON 抢救"逻辑（Pi 需要，因为它的工具调用是流式逐字符累积的）。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional, Union

StopReason = Literal["stop", "length", "tool_use", "error", "aborted"]


@dataclass
class Usage:
    """token 用量。字段顺序与 OpenAI 兼容响应的 usage 语义一致。

    计数口径（明确约定）：**total = input + output**。
    OpenAI 兼容接口的 `prompt_tokens` **已包含**缓存命中部分
    （`prompt_tokens_details.cached_tokens` 是它的子集），缓存字段只是分项，
    绝不能加进总数——否则同一批 token 被数两次，预算与成本比较全部失真。
    """

    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def __add__(self, other: "Usage") -> "Usage":
        if not isinstance(other, Usage):  # pragma: no cover - 防御性
            return self
        return Usage(
            self.input_tokens + other.input_tokens,
            self.output_tokens + other.output_tokens,
            self.cache_read_tokens + other.cache_read_tokens,
            self.cache_write_tokens + other.cache_write_tokens,
        )

    @classmethod
    def from_openai(cls, raw: Optional[Dict[str, Any]]) -> "Usage":
        """从 OpenAI 兼容的 usage 对象构造；缺失字段按 0 处理。"""
        raw = raw or {}
        details = raw.get("prompt_tokens_details") or {}
        return cls(
            input_tokens=int(raw.get("prompt_tokens") or 0),
            output_tokens=int(raw.get("completion_tokens") or 0),
            cache_read_tokens=int(details.get("cached_tokens") or 0),
        )

    def to_dict(self) -> Dict[str, int]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "cache_write_tokens": self.cache_write_tokens,
            "total_tokens": self.total_tokens,
        }


@dataclass
class TextBlock:
    """一段模型输出的自然语言文本（含推理内容时的思考文本）。"""

    text: str
    kind: Literal["text"] = "text"

    def to_dict(self) -> Dict[str, Any]:
        return {"kind": "text", "text": self.text}


@dataclass
class ToolCallBlock:
    """一次工具调用请求。`arguments` 是已解析的 dict，永远不会是半截 JSON。"""

    id: str
    name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    kind: Literal["tool_call"] = "tool_call"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": "tool_call",
            "id": self.id,
            "name": self.name,
            "arguments": self.arguments,
        }


ContentBlock = Union[TextBlock, ToolCallBlock]


@dataclass
class AssistantMessage:
    """一次 LLM 调用的完整结果。

    `error_message` 只在 `stop_reason in {"error", "aborted"}` 时有值。
    这是"错误是数据"约定的载体：LLM 层不向 Agent 循环抛异常表达请求失败，
    而是返回一个 `stop_reason="error"` 的消息，由循环决定如何记账。
    """

    content: list[ContentBlock] = field(default_factory=list)
    stop_reason: StopReason = "stop"
    usage: Usage = field(default_factory=Usage)
    error_message: Optional[str] = None

    @property
    def text(self) -> str:
        """把全部文本块拼起来，便于展示与日志。"""
        return "".join(b.text for b in self.content if isinstance(b, TextBlock))

    @property
    def tool_calls(self) -> list[ToolCallBlock]:
        """按生成顺序返回工具调用块。"""
        return [b for b in self.content if isinstance(b, ToolCallBlock)]

    @property
    def is_error(self) -> bool:
        return self.stop_reason in ("error", "aborted")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": [b.to_dict() for b in self.content],
            "stop_reason": self.stop_reason,
            "usage": self.usage.to_dict(),
            "error_message": self.error_message,
        }
