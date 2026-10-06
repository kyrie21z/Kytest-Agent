"""事件层测试：事件必须可以被直接序列化进 JSONL 轨迹。

评测 harness 与 CLI 都只通过事件观察 Agent，因此"事件 JSON 可序列化"
不是细节，而是"测量不依赖解析 stdout"这条设计约束的前提。
"""
from __future__ import annotations

import json

from code_agent.agent.events import (
    AssistantMessageEvent,
    ErrorEvent,
    RunEnd,
    RunStart,
    ToolCallEnd,
    ToolCallStart,
    TurnEnd,
    TurnStart,
    _EventTypes,
)
from code_agent.message import Usage


def test_every_event_type_declares_a_unique_type_tag():
    tags = [event_type().type for event_type in _EventTypes]
    assert len(tags) == len(set(tags))
    assert set(tags) == {
        "run_start",
        "turn_start",
        "assistant_message",
        "tool_call_start",
        "tool_call_end",
        "turn_end",
        "run_end",
        "error",
    }


def test_events_serialize_to_json_without_custom_encoder():
    events = [
        RunStart(system_prompt_chars=12, tools=["read_file"]),
        TurnStart(turn=1, request_messages=2, request_chars=300),
        AssistantMessageEvent(turn=1, text="读文件", stop_reason="tool_use", usage=Usage(1, 2).to_dict()),
        ToolCallStart(turn=1, id="c1", name="read_file", arguments={"path": "a.py"}),
        ToolCallEnd(turn=1, id="c1", name="read_file", content="[OK] 内容", duration_sec=0.01),
        TurnEnd(turn=1, tool_calls=1, errors=0),
        RunEnd(status="completed", turns=1),
        ErrorEvent(where="llm", message="HTTP 503"),
    ]
    for event in events:
        line = json.dumps(event.to_dict(), ensure_ascii=False)
        assert json.loads(line)["type"] == event.type


def test_tool_call_end_defaults_are_safe_for_the_harness():
    event = ToolCallEnd()
    assert event.is_error is False
    assert event.terminate is False
    assert event.content == ""


def test_event_dicts_are_detached_from_internal_state():
    """事件里的可变对象必须是副本，否则订阅者改动会污染 Agent 状态。"""
    arguments = {"path": "a.py"}
    event = ToolCallStart(turn=1, id="c1", name="read_file", arguments=arguments)
    payload = event.to_dict()
    payload["arguments"]["path"] = "../etc/passwd"
    assert event.arguments["path"] == "a.py"
