"""Agent 主循环测试。

覆盖四类核心行为：
1. 多轮循环与事件顺序；
2. `run_until` 的检查点语义（固定预算质量曲线的前提）；
3. 错误是数据（LLM 失败、未知工具、工具抛异常）；
4. 预算与终止条件。
"""
from __future__ import annotations

from code_agent.agent import Agent, TurnDecision
from code_agent.agent.events import _EventTypes
from code_agent.tools.base import ToolRegistry, ToolResult

from .helpers import (
    FailingLLM,
    RecordingTool,
    ScriptedLLM,
    StubRegistry,
    assert_message_sequence_valid,
    text_response,
    tool_response,
)


def _echo_registry() -> StubRegistry:
    return StubRegistry([RecordingTool("read_file"), RecordingTool("write_file")])


def _three_turn_script() -> ScriptedLLM:
    """三轮回合：读文件 → 写文件 → 自然结束。"""
    return ScriptedLLM(
        [
            tool_response(("read_file", {"path": "solution.py"}), text="先读代码。"),
            tool_response(("write_file", {"path": "test_x.py", "content": "def test_a(): pass"})),
            text_response("测试已生成。"),
        ]
    )


def _agent(llm, registry=None, **kwargs) -> tuple[Agent, list]:
    events: list = []
    agent = Agent(
        llm=llm,
        tools=registry or _echo_registry(),
        system_prompt="你是一个编码 Agent。",
        on_event=events.append,
        **kwargs,
    )
    return agent, events


def _types(events) -> list:
    return [event.type for event in events]


# ----------------------------------------------------------------------
# 1. 多轮循环
# ----------------------------------------------------------------------
def test_three_turn_run_completes_with_expected_accounting():
    agent, events = _agent(_three_turn_script())
    result = agent.run()

    assert result.status == "completed"
    assert result.turns == 3
    assert result.llm_calls == 3
    assert result.tool_calls == 2
    assert result.final_text == "测试已生成。"
    assert result.input_tokens == 100 + 100 + 50
    assert result.output_tokens == 20 + 20 + 10
    assert result.error is None


def test_event_sequence_matches_loop_structure():
    agent, events = _agent(_three_turn_script())
    agent.run()

    assert _types(events) == [
        "run_start",
        "turn_start", "assistant_message", "tool_call_start", "tool_call_end", "turn_end",
        "turn_start", "assistant_message", "tool_call_start", "tool_call_end", "turn_end",
        "turn_start", "assistant_message", "turn_end",
        "run_end",
    ]
    assert all(isinstance(event, _EventTypes) for event in events)
    assert events[-1].status == "completed"
    assert events[0].tools == ["read_file", "write_file"]


def test_tool_arguments_reach_the_tool_intact():
    registry = _echo_registry()
    agent, _ = _agent(_three_turn_script(), registry)
    agent.run()
    assert registry.executed == [
        ("read_file", {"path": "solution.py"}),
        ("write_file", {"path": "test_x.py", "content": "def test_a(): pass"}),
    ]


def test_message_history_is_api_valid_and_balanced():
    llm = _three_turn_script()
    agent, _ = _agent(llm)
    agent.run()

    assert_message_sequence_valid(agent.state.messages)
    assert agent.state.pending_tool_calls() == []
    assert [m["role"] for m in agent.state.messages] == [
        "assistant", "tool", "assistant", "tool", "assistant",
    ]
    # 第二次请求必须已经包含第一次的工具结果
    second_request = llm.requests[1]
    assert second_request[0]["role"] == "system"
    assert any(m["role"] == "tool" for m in second_request)
    assert_message_sequence_valid(second_request)


def test_two_tool_calls_in_one_turn_both_execute():
    llm = ScriptedLLM(
        [
            tool_response(
                ("read_file", {"path": "a.py"}),
                ("read_file", {"path": "b.py"}),
            ),
            text_response("完成"),
        ]
    )
    registry = _echo_registry()
    agent, _ = _agent(llm, registry)
    result = agent.run()

    assert result.tool_calls == 2
    assert [call[1]["path"] for call in registry.executed] == ["a.py", "b.py"]
    assert_message_sequence_valid(agent.state.messages)


# ----------------------------------------------------------------------
# 2. run_until 检查点语义
# ----------------------------------------------------------------------
def test_run_until_pauses_and_resumes_with_cumulative_counters():
    agent, events = _agent(_three_turn_script())

    first = agent.run_until(2)
    assert first.status == "paused"
    assert first.turns == 2
    assert first.tool_calls == 2
    assert agent.state.turn_index == 2
    assert "run_end" in _types(events)

    second = agent.run_until(4)
    assert second.status == "completed"
    assert second.turns == 3 - 2 or second.turns == 1  # 本次调用只跑了 1 个 turn
    assert second.llm_calls == 3  # 累计值
    assert second.total_tokens == 300  # 累计值


def test_run_until_snapshots_produce_a_monotonic_quality_curve():
    """固定预算质量曲线：在第 1/2/3 个 turn 处各取一次样，指标单调不减。"""
    llm = ScriptedLLM(
        [
            tool_response(("write_file", {"path": "test_v1.py", "content": "v1"})),
            tool_response(("write_file", {"path": "test_v2.py", "content": "v2"})),
            tool_response(("write_file", {"path": "test_v3.py", "content": "v3"})),
            text_response("完成"),
        ]
    )
    agent, _ = _agent(llm)

    snapshots = []
    for checkpoint in (1, 2, 3):
        result = agent.run_until(checkpoint)
        snapshots.append((result.turns, result.tool_calls, result.status))

    assert [turn for turn, _, _ in snapshots] == [1, 1, 1]
    assert [calls for _, calls, _ in snapshots] == [1, 2, 3]
    final = agent.run_until(10)
    assert final.status == "completed"
    assert final.turns == 1  # 第 4 个 turn 自然结束
    assert agent.state.tool_calls == 3


def test_run_until_zero_is_a_noop():
    llm = _three_turn_script()
    agent, events = _agent(llm)
    result = agent.run_until(0)
    assert result.turns == 0
    assert result.status == "paused"
    assert llm.calls == 0
    assert _types(events) == ["run_start", "run_end"]


# ----------------------------------------------------------------------
# 3. 错误是数据
# ----------------------------------------------------------------------
def test_llm_failure_becomes_llm_error_status_not_exception():
    agent, events = _agent(FailingLLM("connection reset"))
    result = agent.run()

    assert result.status == "llm_error"
    assert "connection reset" in (result.error or "")
    assert result.turns == 0
    assert "error" in _types(events)
    assert events[-1].status == "llm_error"


def test_unknown_tool_is_an_error_observation_and_loop_continues():
    llm = ScriptedLLM(
        [
            tool_response(("read_file", {"path": "a.py"}), text="读文件"),
            tool_response(("nonexistent_tool", {"x": 1}), text="换一个工具"),
            text_response("结束"),
        ]
    )
    agent, _ = _agent(llm)
    result = agent.run()

    assert result.status == "completed"
    assert result.turns == 3
    error_observation = agent.state.messages[3]
    assert error_observation["role"] == "tool"
    assert error_observation["content"].startswith("[ERROR]")
    assert "未知工具" in error_observation["content"]
    assert agent.state.tool_errors == 1
    assert_message_sequence_valid(agent.state.messages)


def test_tool_exception_is_contained_and_reported():
    def boom(**kwargs):
        raise ValueError("磁盘满了")

    llm = ScriptedLLM(
        [
            tool_response(("read_file", {"path": "a.py"})),
            text_response("好的"),
        ]
    )
    registry = StubRegistry([RecordingTool("read_file", behavior=boom)])
    agent, _ = _agent(llm, registry)
    result = agent.run()

    assert result.status == "completed"
    assert agent.state.tool_errors == 1
    assert "ValueError" in agent.state.messages[1]["content"]


def test_tool_reported_failure_is_marked_error_but_does_not_abort():
    def failure(**kwargs):
        return ToolResult.failure("路径越界：`../etc/passwd`")

    llm = ScriptedLLM(
        [tool_response(("read_file", {"path": "../etc/passwd"})), text_response("换个路径")]
    )
    registry = StubRegistry([RecordingTool("read_file", behavior=failure)])
    agent, events = _agent(llm, registry)
    result = agent.run()

    assert result.status == "completed"
    tool_ends = [e for e in events if e.type == "tool_call_end"]
    assert tool_ends[0].is_error is True
    assert "路径越界" in tool_ends[0].content
    assert agent.state.tool_errors == 1


def test_truncated_output_never_executes_tool_calls():
    """max_tokens 截断会让工具参数变成半截 JSON：必须拒绝执行。"""
    llm = ScriptedLLM(
        [
            tool_response(
                ("write_file", {"path": "test_x.py", "content": "def test_a():"}),
                finish_reason="length",
            ),
            text_response("重新发起调用"),
        ]
    )
    registry = _echo_registry()
    agent, events = _agent(llm, registry)
    result = agent.run()

    assert registry.executed == []  # 关键断言：工具一次都没被执行
    assert agent.state.tool_errors == 0      # 工具没失败，不该记进工具错误
    assert agent.state.tool_calls_skipped == 1  # 单独归类为"输出不完整"
    tool_end = next(e for e in events if e.type == "tool_call_end")
    assert tool_end.is_error is True
    assert "截断" in tool_end.content
    # 但 tool 消息仍然产生，保证消息序列合法
    assert_message_sequence_valid(agent.state.messages)
    assert result.status == "completed"


# ----------------------------------------------------------------------
# 4. 预算、终止与钩子
# ----------------------------------------------------------------------
def test_max_turns_budget_stops_the_loop():
    llm = ScriptedLLM(
        [tool_response(("read_file", {"path": f"{i}.py"})) for i in range(10)]
    )
    agent, _ = _agent(llm, max_turns=3)
    result = agent.run()

    assert result.status == "max_turns"
    assert result.turns == 3
    assert llm.calls == 3


def test_max_llm_calls_budget_is_independent_of_max_turns():
    llm = ScriptedLLM([tool_response(("read_file", {"path": "a.py"})) for _ in range(10)])
    agent, _ = _agent(llm, max_turns=10, max_llm_calls=2)
    result = agent.run()

    assert result.status == "max_turns"
    assert "LLM 调用上限" in (result.error or "")
    assert result.turns == 2


def test_abort_stops_before_next_turn():
    calls = {"n": 0}

    def before_turn(agent, state):
        calls["n"] += 1
        if calls["n"] == 2:
            agent.abort()

    llm = ScriptedLLM([tool_response(("read_file", {"path": "a.py"})) for _ in range(5)])
    agent, _ = _agent(llm, before_turn=before_turn)
    result = agent.run()

    assert result.status == "aborted"
    assert result.turns == 1


def test_finish_turn_can_end_the_loop_with_a_reason():
    def finish_turn(agent, outcome):
        return TurnDecision(end=True, reason="已经足够")

    llm = ScriptedLLM([tool_response(("read_file", {"path": "a.py"})) for _ in range(5)])
    agent, _ = _agent(llm, finish_turn=finish_turn)
    result = agent.run()

    assert result.status == "stopped"
    assert result.error == "已经足够"
    assert result.turns == 1


def test_finish_turn_can_force_another_turn_without_tool_calls():
    """A2 的"修完再跑一次"依赖这条能力：没有工具调用也能继续。"""
    seen = {"n": 0}

    def finish_turn(agent, outcome):
        seen["n"] += 1
        if seen["n"] == 1:
            return TurnDecision(continue_=True)
        return None

    llm = ScriptedLLM([text_response("我没有调用工具"), text_response("第二次回答")])
    agent, _ = _agent(llm, finish_turn=finish_turn)
    result = agent.run()

    assert result.status == "completed"
    assert result.turns == 2
    assert result.final_text == "第二次回答"


def test_tool_terminate_requests_end_the_run():
    llm = ScriptedLLM([tool_response(("read_file", {"path": "a.py"})), text_response("不应到达")])
    registry = ToolRegistry()
    registry.register(RecordingTool(
        "read_file", behavior=lambda **kwargs: ToolResult(ok=True, content="读完了", terminate=True)))
    agent, _ = _agent(llm, registry)
    result = agent.run()

    assert result.status == "stopped"
    assert result.turns == 1
    assert result.final_text == ""  # 没有进入第二个 turn


def test_before_turn_hook_runs_once_per_turn():
    seen: list = []
    llm = _three_turn_script()
    agent, _ = _agent(llm, before_turn=lambda a, s: seen.append(s.turn_index))
    agent.run()
    assert seen == [0, 1, 2]


def test_result_is_json_serializable_for_the_eval_harness():
    import json

    agent, _ = _agent(_three_turn_script())
    payload = agent.run().to_dict()
    assert json.loads(json.dumps(payload))["turns"] == 3
