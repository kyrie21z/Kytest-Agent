"""消息类型层测试：LLM 契约的解析与用量归一化。"""
from __future__ import annotations

from code_agent.message import AssistantMessage, TextBlock, ToolCallBlock, Usage
from code_agent.llm import ToolCall


def test_usage_from_openai_reads_prompt_and_completion():
    usage = Usage.from_openai({"prompt_tokens": 120, "completion_tokens": 30})
    assert usage.input_tokens == 120
    assert usage.output_tokens == 30
    assert usage.total_tokens == 150


def test_usage_from_openai_tolerates_missing_and_null():
    assert Usage.from_openai(None).total_tokens == 0
    assert Usage.from_openai({}).total_tokens == 0
    assert Usage.from_openai({"prompt_tokens": None}).input_tokens == 0


def test_usage_reads_cached_tokens():
    """缓存量是 prompt_tokens 的**分项**，不是额外的加数。

    旧实现把 cache_read 加进总数（100+10+64=174），同一批缓存 token 被数两次。
    正确口径：total = input + output = 110，缓存量独立呈现。
    这个反例在旧实现下会失败——防止计数错误再次被固化为预期。
    """
    usage = Usage.from_openai(
        {"prompt_tokens": 100, "completion_tokens": 10, "prompt_tokens_details": {"cached_tokens": 64}}
    )
    assert usage.cache_read_tokens == 64
    assert usage.input_tokens == 100
    assert usage.total_tokens == 110


def test_usage_total_excludes_cache_breakdown_when_cache_zero_or_missing():
    assert Usage.from_openai({"prompt_tokens": 50, "completion_tokens": 5}).total_tokens == 55
    assert Usage.from_openai(
        {"prompt_tokens": 50, "completion_tokens": 5, "prompt_tokens_details": {}}
    ).total_tokens == 55


def test_usage_total_uses_reported_fields_not_recount():
    """总数由 input+output 组成；缓存分项只做呈现，绝不参与求和。"""
    usage = Usage(input_tokens=100, output_tokens=20, cache_read_tokens=80)
    assert usage.total_tokens == 120  # 若按 100+20+80 则重复计数
    assert usage.to_dict()["cache_read_tokens"] == 80


def test_usage_addition_is_componentwise():
    total = Usage(1, 2, 3, 4) + Usage(10, 20, 30, 40)
    assert (total.input_tokens, total.output_tokens) == (11, 22)
    assert (total.cache_read_tokens, total.cache_write_tokens) == (33, 44)


def test_assistant_message_separates_text_and_tool_calls():
    message = AssistantMessage(
        content=[
            TextBlock(text="先读文件，"),
            ToolCallBlock(id="c1", name="read_file", arguments={"path": "a.py"}),
            TextBlock(text="然后判断。"),
        ],
        stop_reason="tool_use",
    )
    assert message.text == "先读文件，然后判断。"
    assert [call.name for call in message.tool_calls] == ["read_file"]
    assert message.tool_calls[0].arguments == {"path": "a.py"}
    assert message.is_error is False


def test_assistant_message_marks_error_state():
    message = AssistantMessage(stop_reason="error", error_message="HTTP 401")
    assert message.is_error is True
    assert message.text == ""
    assert message.tool_calls == []


def test_tool_call_argument_parsing_reports_truncation_actionably():
    """参数被截断时必须给出可操作的诊断。

    真实场景：服务端概率性截断工具参数，还把 `finish_reason` 谎报成 `tool_calls`。
    若这里退回成 `{"_raw": ...}`，上层只会报"缺少必填参数"，模型会误以为是自己
    漏了字段，于是反复重写同一个大调用，把 turn 预算烧光。
    """
    call = ToolCall(id="c1", name="write_file", arguments='{"path": "a.py", "content": "x')
    parsed = call.parsed_arguments()
    assert "_malformed" in parsed
    assert "不是合法 JSON" in parsed["_malformed"]
    assert "截断" in parsed["_malformed"]
    assert "拆成多次" in parsed["_malformed"]   # 给出明确的下一步动作
    assert "_raw_tail" in parsed


def test_registry_surfaces_the_truncation_diagnosis():
    """注册表必须把截断诊断直接返回，而不是报"缺少必填参数"。"""
    from code_agent.tools.base import ToolRegistry
    from tests.helpers import RecordingTool

    registry = ToolRegistry()
    registry.register(RecordingTool("write_file"))
    call = ToolCall(id="c1", name="write_file", arguments='{"path": "a.py", "content": "x')

    result = registry.execute(call.name, call.parsed_arguments())
    assert result.ok is False
    assert "不是合法 JSON" in result.content
    assert "缺少必填参数" not in result.content


def test_tool_call_argument_parsing_handles_non_object_json():
    call = ToolCall(id="c1", name="echo", arguments='["a", "b"]')
    assert call.parsed_arguments() == {"input": ["a", "b"]}


def test_assistant_message_serializes_to_plain_dict():
    message = AssistantMessage(
        content=[TextBlock(text="hi"), ToolCallBlock(id="c1", name="t", arguments={"k": 1})],
        stop_reason="tool_use",
        usage=Usage(5, 7),
    )
    payload = message.to_dict()
    assert payload["stop_reason"] == "tool_use"
    assert payload["usage"]["total_tokens"] == 12
    assert payload["content"][1]["arguments"] == {"k": 1}
