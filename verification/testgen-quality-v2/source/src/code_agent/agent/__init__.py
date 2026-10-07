"""Minimal general coding agent：无 IO 的 Agent 运行时。

与 Pi Agent 的 `@earendil-works/pi-agent-core` 对应。本包不做任何输入输出，
只通过事件（`events.py`）对外汇报状态，因此 CLI、批处理评测 harness 与
单元测试都是同一套核心的不同订阅者。
"""

from .core import Agent, RunResult, RunStatus, TurnDecision, TurnOutcome
from .events import (
    AgentEvent,
    AssistantMessageEvent,
    ErrorEvent,
    RunEnd,
    RunStart,
    ToolCallEnd,
    ToolCallStart,
    TurnEnd,
    TurnStart,
)
from .state import AgentState, clamp_text, estimate_chars, group_messages, trim_messages

__all__ = [
    "Agent",
    "AgentEvent",
    "AgentState",
    "AssistantMessageEvent",
    "ErrorEvent",
    "RunEnd",
    "RunResult",
    "RunStart",
    "RunStatus",
    "ToolCallEnd",
    "ToolCallStart",
    "TurnDecision",
    "TurnEnd",
    "TurnOutcome",
    "TurnStart",
    "clamp_text",
    "estimate_chars",
    "group_messages",
    "trim_messages",
]
