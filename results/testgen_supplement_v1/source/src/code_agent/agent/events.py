"""Agent 事件：Agent 循环唯一的输出通道。

设计决定：

1. **Agent 核心不 print、不读 stdin。** 所有对外信息都是这里定义的事件，
   由订阅者决定怎么用：CLI 渲染成文本、harness 落成 JSONL、单测断言顺序。
   这直接满足"评测器与 Agent 解耦"——测量不需要解析 stdout。
2. 事件名沿用 Pi Agent 的 `AgentEvent` 十个名字中最必要的一个子集
   （`packages/agent/src/types.ts:514-529`），便于日后对照参考实现。
   本层不做流式，因此省略 `message_update` / `tool_execution_update`。
3. 事件里的消息一律是**普通 dict**，不是内部对象。这样落盘 JSONL 与断言都直接可用，
   且事件订阅者无法通过持有对象引用反向修改 Agent 状态。
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from ..message import Usage


@dataclass
class AgentEvent:
    """所有事件的基类。子类通过 `type` 区分，可直接序列化为 JSON。"""

    type: str = "event"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RunStart(AgentEvent):
    """一次 run()/run_until() 调用开始。"""

    type: str = "run_start"
    system_prompt_chars: int = 0
    tools: List[str] = field(default_factory=list)


@dataclass
class TurnStart(AgentEvent):
    """一个 turn 开始。turn 的定义：一次 LLM 调用 + 它触发的全部工具执行。"""

    type: str = "turn_start"
    turn: int = 0
    request_messages: int = 0
    request_chars: int = 0


@dataclass
class AssistantMessageEvent(AgentEvent):
    """一次 LLM 调用返回的完整消息。"""

    type: str = "assistant_message"
    turn: int = 0
    text: str = ""
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    stop_reason: str = "stop"
    usage: Dict[str, int] = field(default_factory=dict)


@dataclass
class ToolCallStart(AgentEvent):
    type: str = "tool_call_start"
    turn: int = 0
    id: str = ""
    name: str = ""
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolCallEnd(AgentEvent):
    type: str = "tool_call_end"
    turn: int = 0
    id: str = ""
    name: str = ""
    is_error: bool = False
    content: str = ""
    duration_sec: float = 0.0
    terminate: bool = False


@dataclass
class TurnEnd(AgentEvent):
    type: str = "turn_end"
    turn: int = 0
    tool_calls: int = 0
    errors: int = 0


@dataclass
class RunEnd(AgentEvent):
    type: str = "run_end"
    status: str = ""
    turns: int = 0
    error: Optional[str] = None


@dataclass
class ErrorEvent(AgentEvent):
    """可恢复的内部异常（LLM 请求失败、工具注册表异常等），用于排障与失败分类。"""

    type: str = "error"
    where: str = ""
    message: str = ""


_EventTypes = (
    RunStart,
    TurnStart,
    AssistantMessageEvent,
    ToolCallStart,
    ToolCallEnd,
    TurnEnd,
    RunEnd,
    ErrorEvent,
)
"""全部事件类型的清单，供 harness 做穷举断言与 schema 校验。"""

__all__ = [
    "AgentEvent",
    "AssistantMessageEvent",
    "ErrorEvent",
    "RunEnd",
    "RunStart",
    "ToolCallEnd",
    "ToolCallStart",
    "TurnEnd",
    "TurnStart",
    "Usage",
    "_EventTypes",
]
