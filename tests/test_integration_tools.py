"""集成测试：Agent 循环 × 真实工具注册表 × 真实文件系统。

单元测试用替身验证循环逻辑，这组测试验证"循环真的能驱动真实工具"。
两者都用脚本化 LLM，因此完全离线、无 API Key、可重复。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from code_agent.agent import Agent
from code_agent.config import Settings
from code_agent.tools.base import ToolRegistry
from code_agent.tools.file_tools import ReadFileTool
from code_agent.tools.factories import GENERAL_TOOL_NAMES, available_tool_names, build_registry

from .helpers import ScriptedLLM, assert_message_sequence_valid, text_response, tool_response

SOLUTION = '''def clamp(value, low, high):
    if low > high:
        raise ValueError("low must not exceed high")
    if value < low:
        return low
    if value > high:
        return high
    return value
'''


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    (tmp_path / "solution.py").write_text(SOLUTION, encoding="utf-8")
    return tmp_path


@pytest.fixture()
def registry(workspace: Path) -> ToolRegistry:
    """用真实装配函数构造工具集——测试覆盖的是生产代码路径，不是测试自带的一套。"""
    settings = Settings(workspace=workspace, allow_write=True, allow_code_execution=False)
    return build_registry(settings)


@pytest.fixture()
def exec_registry(workspace: Path) -> ToolRegistry:
    """开启命令执行的工具集。命令类测试单独用它，不污染其他测试的配置。"""
    settings = Settings(
        workspace=workspace, allow_write=True, allow_code_execution=True, exec_timeout=120
    )
    return build_registry(settings)


def test_agent_reads_then_writes_real_files(workspace: Path, registry: ToolRegistry):
    llm = ScriptedLLM(
        [
            tool_response(("read_file", {"path": "solution.py"}), text="先读目标代码。"),
            tool_response(
                (
                    "write_file",
                    {
                        "path": "test_solution.py",
                        "content": "from solution import clamp\n\n\ndef test_low():\n    assert clamp(0, 1, 10) == 1\n",
                    },
                ),
                text="根据真实代码写测试。",
            ),
            text_response("已生成 test_solution.py。"),
        ]
    )
    events: list = []
    agent = Agent(
        llm=llm,
        tools=registry,
        system_prompt="你是一个通用编码 Agent。",
        on_event=events.append,
    )
    result = agent.run()

    assert result.status == "completed"
    assert result.tool_calls == 2
    assert result.tool_errors == 0

    generated = workspace / "test_solution.py"
    assert generated.exists()
    assert "def test_low()" in generated.read_text(encoding="utf-8")

    # 模型看到的观察结果里必须包含真实源码内容，而不是"已读取"这类空话
    first_observation = agent.state.messages[1]["content"]
    assert "def clamp(value, low, high)" in first_observation
    assert first_observation.startswith("[OK]")
    assert_message_sequence_valid(agent.state.messages)


def test_path_escape_is_rejected_and_agent_can_recover(workspace: Path, registry: ToolRegistry):
    llm = ScriptedLLM(
        [
            tool_response(("read_file", {"path": "../../etc/passwd"})),
            tool_response(("read_file", {"path": "solution.py"})),
            text_response("换成工作区内的路径。"),
        ]
    )
    agent = Agent(llm=llm, tools=registry, system_prompt="通用编码 Agent。")
    result = agent.run()

    assert result.status == "completed"
    assert result.tool_errors == 1
    escape_observation = agent.state.messages[1]["content"]
    assert escape_observation.startswith("[ERROR]")
    assert "越界" in escape_observation
    # 越界失败没有阻断循环：第二次读取成功返回了真实内容
    assert "def clamp" in agent.state.messages[3]["content"]


def test_write_refuses_to_clobber_without_overwrite_flag(workspace: Path, registry: ToolRegistry):
    llm = ScriptedLLM(
        [
            tool_response(("write_file", {"path": "solution.py", "content": "破坏内容"})),
            text_response("文件已存在，我改用 overwrite。"),
        ]
    )
    agent = Agent(llm=llm, tools=registry, system_prompt="通用编码 Agent。")
    result = agent.run()

    assert result.tool_errors == 1
    assert "已存在" in agent.state.messages[1]["content"]
    assert (workspace / "solution.py").read_text(encoding="utf-8") == SOLUTION


def test_search_code_returns_locations_for_the_model(workspace: Path, registry: ToolRegistry):
    llm = ScriptedLLM(
        [
            tool_response(("search_code", {"pattern": "def clamp"})),
            text_response("找到了定义位置。"),
        ]
    )
    agent = Agent(llm=llm, tools=registry, system_prompt="通用编码 Agent。")
    agent.run()

    observation = agent.state.messages[1]["content"]
    assert observation.startswith("[OK]")
    assert "solution.py" in observation


def test_tool_schemas_are_valid_openai_function_definitions(registry: ToolRegistry):
    for schema in registry.schemas():
        assert schema["type"] == "function"
        function = schema["function"]
        assert function["name"] and function["description"]
        assert function["parameters"]["type"] == "object"
        for name in function["parameters"].get("required", []):
            assert name in function["parameters"]["properties"]


def test_every_assemblable_tool_constructs_and_exposes_a_valid_schema(workspace: Path):
    """每个可装配的工具都必须能被真的构造出来。

    这条测试直接针对一个已发生的缺陷：`ListFilesTool` 缺 `__init__`，
    继承了基类的 `(workspace)` 签名，导致装配时崩溃。
    """
    settings = Settings(workspace=workspace)
    for name in available_tool_names():
        tool = build_registry(settings, [name]).get(name)
        assert tool is not None, f"{name} 未能装配"
        assert tool.schema()["function"]["name"] == name


def test_default_registry_is_general_purpose_only(registry: ToolRegistry):
    """A0 的工具集里不允许出现测试专用能力，否则反事实对照失效。"""
    names = set(registry.names())
    assert names == set(GENERAL_TOOL_NAMES)
    forbidden = {"run_pytest", "coverage_report", "mutation_test", "run_tests"}
    assert not (names & forbidden)


def test_unknown_tool_name_fails_at_assembly_time(workspace: Path):
    with pytest.raises(KeyError):
        build_registry(Settings(workspace=workspace), ["read_file", "no_such_tool"])


def test_agent_survives_an_entire_run_without_api_key(workspace: Path, registry: ToolRegistry):
    """无 API Key 也能跑完整闭环——这是"5 分钟可运行"硬性要求的一部分。"""
    llm = ScriptedLLM([text_response("离线回答")], fallback="离线兜底回答")
    agent = Agent(llm=llm, tools=registry, system_prompt="通用编码 Agent。")
    result = agent.run()
    assert result.status == "completed"
    assert result.final_text == "离线回答"


# ----------------------------------------------------------------------
# 命令执行：A0 能否形成"写 → 跑 → 看结果"的闭环
# ----------------------------------------------------------------------
PROBE_TEST = "def test_ok():\n    assert 1 + 1 == 2\n\n\ndef test_bad():\n    assert 1 + 1 == 3\n"


def test_agent_runs_a_command_and_observation_carries_the_real_exit_code(workspace: Path, exec_registry: ToolRegistry):
    """Agent 执行命令后，观察结果里必须是真实的退出码与输出。

    这是"A0 是否自发形成执行反馈闭环"这一观察项的技术前提：
    如果观察结果里没有真实退出码，模型无从判断自己写的东西能不能跑。
    """
    llm = ScriptedLLM(
        [
            tool_response(
                (
                    "run_command",
                    {"command": f'"{sys.executable}" -c "print(6 * 7)"'},
                )
            ),
            text_response("命令输出是 42。"),
        ]
    )
    agent = Agent(llm=llm, tools=exec_registry, system_prompt="通用编码 Agent。")
    result = agent.run()

    assert result.status == "completed"
    assert result.tool_errors == 0
    observation = agent.state.messages[1]["content"]
    assert observation.startswith("[OK]")
    assert "42" in observation
    assert "退出码 0" in observation


def test_agent_gets_actionable_feedback_from_a_failing_test_run(workspace: Path, exec_registry: ToolRegistry):
    """失败的测试运行必须带回足够定位问题的信息。

    这是 A2（执行反馈）能成立的前提：反馈若只有"失败了"三个字，循环无法修复。
    """
    (workspace / "test_probe.py").write_text(PROBE_TEST, encoding="utf-8")
    llm = ScriptedLLM(
        [
            tool_response(
                ("run_command", {"command": f'"{sys.executable}" -m pytest test_probe.py -q'})
            ),
            text_response("有一个用例失败，需要修正。"),
        ]
    )
    agent = Agent(llm=llm, tools=exec_registry, system_prompt="通用编码 Agent。")
    result = agent.run()

    observation = agent.state.messages[1]["content"]
    assert observation.startswith("[ERROR]")   # 非零退出码 → 失败观察结果
    assert "1 failed" in observation
    assert "1 passed" in observation
    assert "test_bad" in observation           # 指明是哪个用例
    assert result.tool_errors == 1


def test_agent_recovers_after_a_command_fails(workspace: Path, exec_registry: ToolRegistry):
    """命令失败不能中断循环——Agent 必须能根据失败信息继续下一步。"""
    llm = ScriptedLLM(
        [
            tool_response(("run_command", {"command": "definitely-not-a-real-binary-xyz"})),
            tool_response(("read_file", {"path": "solution.py"})),
            text_response("换个方式继续。"),
        ]
    )
    agent = Agent(llm=llm, tools=exec_registry, system_prompt="通用编码 Agent。")
    result = agent.run()

    assert result.status == "completed"
    assert result.tool_calls == 2
    assert agent.state.messages[1]["content"].startswith("[ERROR]")
    assert "def clamp" in agent.state.messages[3]["content"]
    assert_message_sequence_valid(agent.state.messages)

# ----------------------------------------------------------------------
# 评审整改：参数类型校验、超限文件反馈
# ----------------------------------------------------------------------
def test_registry_rejects_wrong_parameter_types(workspace: Path, registry: ToolRegistry):
    """schema 声明 boolean 的参数绝不能接受字符串（评审 A1）。

    旧实现：`overwrite: "false"` 是非空字符串、为真值，导致已有文件被覆盖。
    修复后：类型校验在 tool.run() 之前执行，非法参数零副作用。
    """
    target = workspace / "victim.txt"
    target.write_text("original content", encoding="utf-8")

    result = registry.execute("write_file", {
        "path": "victim.txt", "content": "overwritten!", "overwrite": "false",
    })
    assert result.ok is False
    assert "boolean" in result.content
    assert target.read_text(encoding="utf-8") == "original content"

    # 字符串数字同样被拒（integer 字段）
    result = registry.execute("read_file", {"path": "victim.txt", "start_line": "1"})
    assert result.ok is False
    assert "integer" in result.content
    # bool 是 int 的子类：integer 字段也不能收 bool
    result = registry.execute("read_file", {"path": "victim.txt", "start_line": True})
    assert result.ok is False


def test_registry_accepts_correct_types_still_works(workspace: Path, registry: ToolRegistry):
    target = workspace / "ok.txt"
    result = registry.execute("write_file", {"path": "ok.txt", "content": "v1"})
    assert result.ok is True
    result = registry.execute("write_file", {"path": "ok.txt", "content": "v2", "overwrite": True})
    assert result.ok is True
    assert target.read_text(encoding="utf-8") == "v2"


def test_oversized_file_partial_read_with_explicit_range(tmp_path: Path):
    """超限文件 + 显式行区间 → 流式部分读取成功（评审 F2 的可执行恢复路径）。"""
    settings = type("S", (), {"workspace": tmp_path, "max_file_bytes": 1000})()
    tool = ReadFileTool(settings)
    big = tmp_path / "big.txt"
    big.write_text("\n".join(f"line {i}" for i in range(1, 501)), encoding="utf-8")

    result = tool.run(path="big.txt")  # 不给区间：整读被拒
    assert result.ok is False
    assert "start_line/end_line" in result.content
    assert "分段读取" not in result.content  # 旧提示与能力不符，必须移除

    result = tool.run(path="big.txt", start_line=490, end_line=500)
    assert result.ok is True
    assert "line 490" in result.content and "line 500" in result.content
    assert "部分读取" in result.content


def test_oversized_file_partial_read_respects_line_budget(tmp_path: Path):
    settings = type("S", (), {"workspace": tmp_path, "max_file_bytes": 100})()
    tool = ReadFileTool(settings)
    big = tmp_path / "big.txt"
    big.write_text("\n".join(f"row {i}" for i in range(1, 101)), encoding="utf-8")
    result = tool.run(path="big.txt", start_line=1, max_lines=5)
    assert result.ok is True
    assert "row 1" in result.content and "row 6" not in result.content
    assert "继续读取" in result.content
