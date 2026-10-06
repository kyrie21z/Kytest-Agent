"""状态层测试：上下文裁剪必须保持 assistant/tool 配对完整。

这是全套测试里最重要的一组。消息序列一旦出现孤立 tool 消息，
真实 OpenAI 兼容 API 会直接返回 400，而这类 bug 在开发期很难复现。
"""
from __future__ import annotations

from code_agent.agent.state import AgentState, clamp_text, estimate_chars, group_messages, trim_messages
from code_agent.message import AssistantMessage, TextBlock, ToolCallBlock

from .helpers import assert_message_sequence_valid


def _assistant_with_call(call_id: str, name: str = "read_file") -> AssistantMessage:
    return AssistantMessage(
        content=[ToolCallBlock(id=call_id, name=name, arguments={"path": "a.py"})],
        stop_reason="tool_use",
    )


def _conversation(turns: int) -> list:
    """构造 `turns` 轮 用户→助手→工具 的对话。"""
    state = AgentState(system_prompt="sys")
    for index in range(turns):
        state.add_user(f"任务 {index}：" + "x" * 400)
        state.add_assistant(_assistant_with_call(f"call_{index}"))
        state.add_tool_result(f"call_{index}", "read_file", "y" * 400)
    return state.messages


# ----------------------------------------------------------------------
# 字符估算与截断
# ----------------------------------------------------------------------
def test_estimate_chars_covers_strings_dicts_and_lists():
    assert estimate_chars("abc") == 3
    assert estimate_chars(None) == 0
    assert estimate_chars({"a": "bc"}) == 3  # 键 1 + 值 2
    assert estimate_chars(["ab", "c"]) == 3
    assert estimate_chars(123) == 3


def test_clamp_text_keeps_head_and_tail_with_marker():
    text = "H" * 500 + "M" * 500 + "T" * 500
    clamped = clamp_text(text, 300)
    assert len(clamped) < len(text)
    assert clamped.startswith("H")
    assert clamped.endswith("T")
    assert "内容过长已折叠" in clamped


def test_clamp_text_is_noop_within_limit():
    assert clamp_text("short", 100) == "short"


# ----------------------------------------------------------------------
# 分组：配对不可分割
# ----------------------------------------------------------------------
def test_group_messages_keeps_assistant_and_tools_together():
    messages = _conversation(2)
    groups = group_messages(messages)
    assert len(groups) == 4  # 2 × (user, assistant+tool)
    assert [m["role"] for m in groups[1]] == ["assistant", "tool"]
    assert [m["role"] for m in groups[3]] == ["assistant", "tool"]


def test_group_messages_handles_two_calls_in_one_assistant_message():
    state = AgentState(system_prompt="sys")
    state.add_user("任务")
    state.add_assistant(
        AssistantMessage(
            content=[
                ToolCallBlock(id="c1", name="a", arguments={}),
                ToolCallBlock(id="c2", name="b", arguments={}),
            ],
            stop_reason="tool_use",
        )
    )
    state.add_tool_result("c1", "a", "r1")
    state.add_tool_result("c2", "b", "r2")
    groups = group_messages(state.messages)
    assert len(groups) == 2
    assert [m["role"] for m in groups[1]] == ["assistant", "tool", "tool"]


# ----------------------------------------------------------------------
# 裁剪：不变量
# ----------------------------------------------------------------------
def test_trim_drops_old_groups_but_never_orphans_tool_messages():
    messages = _conversation(6)
    trimmed = trim_messages(messages, 1500)
    assert_message_sequence_valid(trimmed)
    assert len(trimmed) < len(messages)
    # 最新一轮必须保留
    assert trimmed[-1]["content"].startswith("y")


def test_trim_always_keeps_first_message():
    """第一条消息是任务描述，丢了 Agent 就不知道要做什么。"""
    messages = _conversation(6)
    trimmed = trim_messages(messages, 900)
    assert trimmed[0]["role"] == "user"
    assert trimmed[0]["content"].startswith("任务 0")


def test_trim_keeps_first_message_even_when_it_exceeds_budget():
    """任务描述本身就超预算时，优先级高于"严格不超预算"。"""
    state = AgentState(system_prompt="sys")
    state.add_user("任务：" + "u" * 5000)
    state.add_assistant(_assistant_with_call("c1"))
    state.add_tool_result("c1", "read_file", "t" * 5000)
    trimmed = trim_messages(state.messages, 600)
    assert trimmed[0]["role"] == "user"
    assert trimmed[0]["content"].startswith("任务：")
    assert_message_sequence_valid(trimmed)


def test_trim_clamps_when_a_single_group_exceeds_budget():
    """最新一组必须保留（它记录"刚刚发生了什么"），代价是超预算时做头尾截断。"""
    state = AgentState(system_prompt="sys")
    state.add_user("任务：" + "u" * 3000)
    state.add_assistant(_assistant_with_call("c1"))
    state.add_tool_result("c1", "read_file", "t" * 5000)
    trimmed = trim_messages(state.messages, 800)
    assert_message_sequence_valid(trimmed)
    assert trimmed[0]["role"] == "user"
    assert trimmed[1]["role"] == "assistant"
    assert trimmed[-1]["role"] == "tool"
    assert "内容过长已折叠" in trimmed[-1]["content"]
    assert sum(estimate_chars(m) for m in trimmed) < 3000


def test_trim_handles_empty_and_degenerate_budgets():
    assert trim_messages([], 1000) == []
    messages = _conversation(2)
    assert trim_messages(messages, 0) == messages


# ----------------------------------------------------------------------
# 请求构造与状态记账
# ----------------------------------------------------------------------
def test_build_request_messages_prepends_system_and_stays_valid():
    state = AgentState(system_prompt="你是编码助手")
    state.messages = _conversation(8)
    request = state.build_request_messages(2000)
    assert request[0] == {"role": "system", "content": "你是编码助手"}
    assert_message_sequence_valid(request)


def test_add_assistant_records_tool_calls_in_api_shape():
    state = AgentState()
    state.add_assistant(_assistant_with_call("call_9"))
    record = state.messages[-1]
    assert record["role"] == "assistant"
    assert record["tool_calls"][0]["id"] == "call_9"
    assert record["tool_calls"][0]["function"]["name"] == "read_file"
    assert record["tool_calls"][0]["type"] == "function"


def test_add_assistant_omits_tool_calls_key_for_plain_text():
    state = AgentState()
    state.add_assistant(AssistantMessage(content=[TextBlock(text="做完了")]))
    assert "tool_calls" not in state.messages[-1]


def test_pending_tool_calls_is_empty_for_balanced_conversation():
    state = AgentState()
    state.messages = _conversation(3)
    assert state.pending_tool_calls() == []


def test_pending_tool_calls_reports_unanswered_call():
    """未配对的调用必须可被检测出来——它是评测数据可信度的前提。"""
    state = AgentState()
    state.add_user("任务")
    state.add_assistant(_assistant_with_call("call_x"))
    pending = state.pending_tool_calls()
    assert [call["id"] for call in pending] == ["call_x"]


def test_tool_meta_is_not_written_into_api_messages():
    state = AgentState()
    state.add_user("任务")
    state.add_assistant(_assistant_with_call("c1"))
    state.add_tool_result("c1", "read_file", "[OK] 内容")
    state.record_tool_meta("c1", "read_file", is_error=False, terminate=True)
    tool_message = state.messages[-1]
    assert set(tool_message) == {"role", "tool_call_id", "name", "content"}
    assert state.tool_meta[0]["terminate"] is True
