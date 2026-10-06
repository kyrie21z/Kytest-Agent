"""测试公共构件：脚本化 LLM 与最小工具集。

脚本化 LLM 让"Agent 循环"这件事可以被确定性地测试——不需要网络、不需要 API Key、
不需要真实模型。这是把 Agent 循环纳入单元测试的前提，也是离线演示的基础。
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Sequence

from code_agent.agent.events import _EventTypes
from code_agent.llm import BaseLLM, LLMResponse, ToolCall


class ScriptedLLM(BaseLLM):
    """按脚本顺序返回响应；脚本用尽时返回一条不含工具调用的兜底文本。

    每次调用都记录收到的 messages，便于断言"发给模型的消息序列是否合法"。
    """

    def __init__(
        self,
        responses: Sequence[LLMResponse],
        fallback: str = "（脚本已用尽）",
    ) -> None:
        self._responses: List[LLMResponse] = list(responses)
        self._cursor = 0
        self.fallback = fallback
        self.requests: List[List[Dict[str, Any]]] = []

    @property
    def name(self) -> str:
        return "ScriptedLLM"

    @property
    def calls(self) -> int:
        return self._cursor

    def chat(
        self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None
    ) -> LLMResponse:
        self.requests.append([dict(m) for m in messages])
        if self._cursor < len(self._responses):
            response = self._responses[self._cursor]
            self._cursor += 1
            return response
        return LLMResponse(content=self.fallback)


class FailingLLM(BaseLLM):
    """每次调用都抛异常，用于验证"错误是数据"的约定。"""

    def __init__(self, message: str = "connection reset") -> None:
        self.message = message

    @property
    def name(self) -> str:
        return "FailingLLM"

    def chat(
        self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None
    ) -> LLMResponse:
        raise RuntimeError(self.message)


def tool_response(
    *calls: tuple,
    text: str = "",
    usage: Optional[Dict[str, int]] = None,
    finish_reason: str = "tool_calls",
) -> LLMResponse:
    """构造一次带工具调用的 LLM 响应。

    Args:
        calls: 每个元素是 `(name, arguments_dict)` 或 `(id, name, arguments_dict)`。
    """
    tool_calls: List[ToolCall] = []
    for index, spec in enumerate(calls):
        if len(spec) == 2:
            name, arguments = spec  # type: ignore[misc]
            call_id = f"call_{index + 1}"
        else:
            call_id, name, arguments = spec  # type: ignore[misc]
        tool_calls.append(
            ToolCall(id=call_id, name=name, arguments=json.dumps(arguments))
        )
    raw_usage = usage or {"prompt_tokens": 100, "completion_tokens": 20}
    return LLMResponse(
        content=text,
        tool_calls=tool_calls,
        usage=dict(raw_usage),
        raw={"choices": [{"finish_reason": finish_reason}]},
    )


def text_response(
    text: str, usage: Optional[Dict[str, int]] = None, finish_reason: str = "stop"
) -> LLMResponse:
    """构造一次纯文本（无工具调用）的 LLM 响应。"""
    raw_usage = usage or {"prompt_tokens": 50, "completion_tokens": 10}
    return LLMResponse(
        content=text,
        usage=dict(raw_usage),
        raw={"choices": [{"finish_reason": finish_reason}]},
    )


class RecordingTool:
    """记录调用参数的假工具，避免测试触碰真实文件系统。"""

    def __init__(self, name: str, behavior: Any = None) -> None:
        self.name = name
        self.description = f"{name} 测试替身"
        self.parameters: Dict[str, Any] = {
            "type": "object",
            "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
        }
        self.calls: List[Dict[str, Any]] = []
        self._behavior = behavior

    def schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def run(self, **kwargs: Any) -> Any:
        from code_agent.tools.base import ToolResult

        self.calls.append(kwargs)
        if self._behavior is not None:
            produced = self._behavior(**kwargs)
            if isinstance(produced, ToolResult):
                return produced
            return ToolResult.success(str(produced))
        return ToolResult.success(f"{self.name} 已执行，参数：{kwargs}")


class StubRegistry:
    """工具注册表的测试替身：支持注入未知工具与抛异常的工具。"""

    def __init__(self, tools: Optional[Sequence[Any]] = None) -> None:
        self._tools: Dict[str, Any] = {tool.name: tool for tool in (tools or [])}
        self.executed: List[tuple] = []

    def names(self) -> List[str]:
        return sorted(self._tools)

    def schemas(self) -> List[Dict[str, Any]]:
        return [tool.schema() for tool in self._tools.values()]

    def execute(self, name: str, arguments: Dict[str, Any]) -> Any:
        from code_agent.tools.base import ToolResult

        self.executed.append((name, arguments))
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult.failure(f"未知工具 `{name}`")
        return tool.run(**arguments)


def assert_message_sequence_valid(messages: Sequence[Dict[str, Any]]) -> None:
    """断言消息序列满足 OpenAI 兼容 API 的硬性要求。

    这是本项目最重要的一条不变量：每个 tool 消息必须能对应到前面某条 assistant
    消息里的 tool_call，否则真实 API 会直接返回 400。
    """
    seen_calls: set = set()
    for message in messages:
        role = message.get("role")
        if role == "assistant":
            for call in message.get("tool_calls") or []:
                seen_calls.add(call.get("id"))
        elif role == "tool":
            assert message.get("tool_call_id") in seen_calls, (
                f"孤立 tool 消息：{message.get('tool_call_id')} 没有对应的 assistant tool_call"
            )


__all__ = [
    "FailingLLM",
    "RecordingTool",
    "ScriptedLLM",
    "StubRegistry",
    "_EventTypes",
    "assert_message_sequence_valid",
    "text_response",
    "tool_response",
]
