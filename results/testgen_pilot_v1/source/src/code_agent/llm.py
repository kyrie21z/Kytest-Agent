"""LLM 客户端层。

设计目标：
1. 只依赖标准库 urllib，避免安装/网络受限导致无法运行；
2. 统一 OpenAI 兼容的 /chat/completions 协议，可接 OpenAI / DeepSeek / 通义千问等；
3. 内置指数退避重试，处理 429 限流、5xx 服务端错误与网络超时；
4. 提供 MockLLM，使项目在没有 API Key 时也能完整演示 Agent 循环。
"""
from __future__ import annotations

import json
import random
import re
import time
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from .errors import LLMError

RETRYABLE_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}
MAX_ERROR_BODY = 600


@dataclass
class ToolCall:
    """一次原生 Function Calling 请求。"""

    id: str
    name: str
    arguments: str = "{}"

    def parsed_arguments(self) -> Dict[str, Any]:
        """把 arguments 解析成 dict，兼容部分服务商直接返回对象的情况。

        解析失败时**必须给出可操作的诊断**，而不是塞一个 `_raw` 让上层报
        "缺少必填参数"。原因是真实遇到过的：服务端会概率性地把工具参数截断，
        同时把 `finish_reason` 谎报为 `tool_calls`（而不是 `length`）。
        此时模型只会看到"缺少必填参数：content"，于是不断重写同一个大文件，
        把整个 turn 预算烧光。把"参数不完整"明确说出来，模型才有机会改用
        更小的分块写入。
        """
        if isinstance(self.arguments, dict):  # 服务商直接返回对象
            return dict(self.arguments)

        text = (self.arguments or "").strip() or "{}"
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            return {
                "_malformed": (
                    f"工具 `{self.name}` 的参数不是合法 JSON（{exc.msg}，位置 {exc.pos}，"
                    f"共收到 {len(text)} 字符）。这通常意味着参数在传输中被截断。"
                    "请把这次写入拆成多次更小的调用（例如先写一部分，再用追加方式补全），"
                    "或减少单次写入的内容量。"
                ),
                "_raw_tail": text[-200:],
            }
        if isinstance(data, dict):
            return data
        return {"input": data}

    def to_message(self) -> Dict[str, Any]:
        """转换回 API 消息格式，用于写入对话历史。"""
        arguments = self.arguments
        if not isinstance(arguments, str):
            arguments = json.dumps(arguments, ensure_ascii=False)
        return {
            "id": self.id,
            "type": "function",
            "function": {"name": self.name, "arguments": arguments},
        }


@dataclass
class LLMResponse:
    """LLM 一次回复的结构化表示。"""

    content: str = ""
    tool_calls: List[ToolCall] = field(default_factory=list)
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


class BaseLLM(ABC):
    """LLM 抽象基类，方便替换服务商或注入测试桩。"""

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> LLMResponse:
        """发送对话并返回模型回复。"""


def _read_error_body(exc: urllib.error.HTTPError) -> str:
    try:
        body = exc.read().decode("utf-8", errors="replace").strip()
    except Exception:  # noqa: BLE001 - 读取错误响应失败时退化为状态描述
        body = str(exc.reason)
    return body[:MAX_ERROR_BODY] if body else str(exc.reason)


class OpenAICompatibleLLM(BaseLLM):
    """OpenAI 兼容 Chat Completions 客户端。"""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        timeout: int = 60,
        max_retries: int = 3,
    ) -> None:
        if not api_key or not base_url or not model:
            raise LLMError("OpenAICompatibleLLM 需要 api_key、base_url、model 三个参数")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        # 输出上限必须 ≥1：服务端会校验范围（例如千问要求 [1, 131072]），传 0 直接 400。
        # 这里兜一层底，而不是信任调用方——"0 表示不限"是 Agent 侧预算的语义，
        # 在请求体里没有这种表达方式。
        self.max_tokens = max(1, int(max_tokens or 2048))
        self.timeout = timeout
        self.max_retries = max(0, max_retries)

    @property
    def name(self) -> str:
        return f"OpenAICompatibleLLM({self.model})"

    # ------------------------------------------------------------------
    # 请求
    # ------------------------------------------------------------------
    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> LLMResponse:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        return self._parse(self._post(payload))

    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "code-agent/1.0",
        }
        last_error: Optional[LLMError] = None
        for attempt in range(self.max_retries + 1):
            request = urllib.request.Request(url, data=body, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    raw = response.read().decode("utf-8", errors="replace")
                return json.loads(raw)
            except urllib.error.HTTPError as exc:
                detail = _read_error_body(exc)
                last_error = LLMError(f"HTTP {exc.code}: {detail}")
                if exc.code in RETRYABLE_STATUS and attempt < self.max_retries:
                    time.sleep(self._retry_delay(attempt, exc.headers.get("Retry-After")))
                    continue
                raise LLMError(f"LLM 请求失败（HTTP {exc.code}）：{detail}") from exc
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                last_error = LLMError(f"网络错误：{exc}")
                if attempt < self.max_retries:
                    time.sleep(self._retry_delay(attempt, None))
                    continue
                raise LLMError(f"LLM 请求失败（网络异常，已重试 {self.max_retries} 次）：{exc}") from exc
            except json.JSONDecodeError as exc:
                raise LLMError("LLM 返回的内容不是合法 JSON，可能是网关错误") from exc
        raise last_error or LLMError("LLM 请求失败")

    def _retry_delay(self, attempt: int, retry_after: Optional[str]) -> float:
        """指数退避 + 抖动；服务端给出 Retry-After 时优先遵守。"""
        if retry_after:
            try:
                return min(float(retry_after), 30.0)
            except (TypeError, ValueError):
                pass
        base = min(2.0 ** attempt, 8.0) * 0.8
        return base + random.uniform(0, 0.4)

    def _parse(self, data: Dict[str, Any]) -> LLMResponse:
        choices = data.get("choices") or []
        if not choices:
            raise LLMError(f"LLM 返回缺少 choices 字段：{str(data)[:300]}")
        message = choices[0].get("message") or {}
        content = message.get("content") or ""
        if isinstance(content, list):  # 兼容分段内容格式
            content = "".join(
                str(part.get("text", "")) if isinstance(part, dict) else str(part) for part in content
            )
        calls: List[ToolCall] = []
        for item in message.get("tool_calls") or []:
            function = item.get("function") or {}
            arguments = function.get("arguments", "{}")
            if not isinstance(arguments, str):
                arguments = json.dumps(arguments, ensure_ascii=False)
            calls.append(
                ToolCall(
                    id=item.get("id") or f"call_{len(calls)}",
                    name=function.get("name", ""),
                    arguments=arguments,
                )
            )
        return LLMResponse(
            content=content.strip(),
            tool_calls=calls,
            usage=data.get("usage") or {},
            raw=data,
        )


class MockLLM(BaseLLM):
    """离线规则模拟 LLM：没有 API Key 时也能跑出完整的多轮 Agent 循环。

    行为（确定性，不依赖随机）：
    1. 若传入 `responses`（测试用脚本），按顺序返回；
    2. 有 `list_files` 且没用过 → 先看工作区里有什么；
    3. 从消息里找到候选文件且 `read_file` 没用过 → 读取真实内容；
    4. 已经拿到观察结果 → 基于**真实**工具输出做小结；
    5. 否则说明当前处于离线模式以及如何启用真实模型。

    刻意保持通用：不假设任务类型，不提测试、覆盖率等专用概念。
    它的用途是让"Agent 循环 + 工具调用"在没有网络的环境下可被看见和验收。
    """

    _FILE_RE = re.compile(
        r"[\w./\\-]+\.(?:py|pyi|js|jsx|ts|tsx|java|go|rs|c|h|cpp|hpp|cs|rb|php|swift|kt|sh|sql|toml|md|txt|json|ya?ml)\b",
        re.IGNORECASE,
    )
    _MAX_FILES_TO_READ = 2

    def __init__(self, responses: Optional[Sequence[LLMResponse]] = None, workspace: Optional[Any] = None) -> None:
        self._scripted: List[LLMResponse] = list(responses or [])
        self._cursor = 0
        self._counter = 0
        self.workspace = workspace

    @property
    def name(self) -> str:
        return "MockLLM（离线规则模拟）"

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> LLMResponse:
        if self._cursor < len(self._scripted):
            response = self._scripted[self._cursor]
            self._cursor += 1
            return response
        return self._rule_based(messages, tools or [])

    # ------------------------------------------------------------------
    # 规则模拟
    # ------------------------------------------------------------------
    def _next_id(self) -> str:
        self._counter += 1
        return f"mock_call_{self._counter}"

    def _tool_call(self, name: str, arguments: Dict[str, Any], thought: str) -> LLMResponse:
        return LLMResponse(
            content=thought,
            tool_calls=[ToolCall(id=self._next_id(), name=name, arguments=json.dumps(arguments, ensure_ascii=False))],
            usage={"prompt_tokens": 600, "completion_tokens": 80},
            raw={"choices": [{"finish_reason": "tool_calls"}]},
        )

    def _text(self, content: str) -> LLMResponse:
        return LLMResponse(
            content=content,
            usage={"prompt_tokens": 700, "completion_tokens": 120},
            raw={"choices": [{"finish_reason": "stop"}]},
        )

    def _used_tools(self, messages: List[Dict[str, Any]]) -> set:
        return {str(m.get("name") or "") for m in messages if m.get("role") == "tool"}

    def _observations(self, messages: List[Dict[str, Any]]) -> List[str]:
        return [
            str(m.get("content") or "")
            for m in messages
            if m.get("role") == "tool" and not str(m.get("content") or "").startswith("[ERROR]")
        ]

    def _candidate_files(self, messages: List[Dict[str, Any]]) -> List[str]:
        """找出消息里提到的、且在工作区真实存在的文件。"""
        text = "\n".join(str(m.get("content") or "") for m in messages)
        seen: List[str] = []
        for match in self._FILE_RE.findall(text):
            candidate = match.replace("\\", "/")
            if candidate in seen:
                continue
            seen.append(candidate)
        if self.workspace is None:
            return seen
        root = Path(self.workspace)
        return [name for name in seen if (root / name).is_file()]

    def _last_user_text(self, messages: List[Dict[str, Any]]) -> str:
        for message in reversed(messages):
            if message.get("role") == "user":
                return str(message.get("content") or "")
        return ""

    def _already_read(self, messages: List[Dict[str, Any]]) -> set:
        """已经读过的文件路径。避免离线模式反复读同一个文件而耗尽 turn 预算。"""
        read: set = set()
        for message in messages:
            if message.get("role") != "assistant":
                continue
            for call in message.get("tool_calls") or []:
                function = call.get("function") or {}
                if function.get("name") != "read_file":
                    continue
                raw = function.get("arguments")
                if isinstance(raw, str):
                    try:
                        raw = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                if isinstance(raw, dict) and raw.get("path"):
                    read.add(str(raw["path"]).replace("\\", "/"))
        return read

    def _rule_based(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> LLMResponse:
        available = {item.get("function", {}).get("name") for item in tools}
        used = self._used_tools(messages)
        observations = self._observations(messages)

        # 1. 先看工作区里有什么（只在还没有任何观察结果时做一次）
        if "list_files" in available and "list_files" not in used and not observations:
            return self._tool_call(
                "list_files",
                {"path": ".", "recursive": True},
                "收到任务。先看看工作区里有哪些文件，再决定读什么。",
            )

        # 2. 读取尚未读过的真实文件（最多两个，避免离线模式无限循环）
        if "read_file" in available:
            already_read = self._already_read(messages)
            pending = [
                name for name in self._candidate_files(messages) if name not in already_read
            ]
            if pending and len(already_read) < self._MAX_FILES_TO_READ:
                target = pending[0]
                return self._tool_call(
                    "read_file",
                    {"path": target},
                    f"读取 `{target}` 的真实内容，避免凭空推断。",
                )

        # 3. 已经拿到真实工具输出，基于它做小结
        if observations:
            joined = "\n\n".join(observations[-2:])
            if len(joined) > 2200:
                joined = joined[:2200] + "\n…（内容过长已截断）"
            return self._text(
                "【离线 Mock 模式】以下是刚才通过工具获得的真实信息：\n\n"
                f"{joined}\n\n"
                "以上内容来自真实工具调用，而非模型推断。配置 LLM_API_KEY / LLM_BASE_URL / "
                "LLM_MODEL 后，Agent 会基于同样的信息完成代码审查、解释、测试生成或重构建议。"
            )


        # 4. 兜底说明
        task = self._last_user_text(messages)
        names = "、".join(sorted(name for name in available if name)) or "（无）"
        return self._text(
            "【离线 Mock 模式】当前没有配置真实 LLM，我只能演示 Agent 的工具调用流程。\n"
            f"你刚才的任务：{task[:120]}\n"
            f"我可以使用的工具：{names}\n\n"
            "在 .env 中配置 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL 后即可获得真实模型回答。"
        )