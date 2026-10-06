"""命令执行工具测试。

这组测试回答一个问题：**Agent 通过这个工具拿到的，是不是真实、完整、可判断的命令输出。**
覆盖输出格式、退出码语义、超时、路径边界、护栏与配置开关。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from code_agent.config import Settings
from code_agent.tools.shell_tools import MAX_TIMEOUT_SEC, RunCommandTool

PROBE = "import sys; print('out'); sys.stderr.write('err\\n'); sys.exit({code})"
PYTEST_TEST = (
    "def test_ok():\n"
    "    assert 1 + 1 == 2\n"
    "\n"
    "\n"
    "def test_bad():\n"
    "    assert 1 + 1 == 3, 'expected 2 but got 3'\n"
)


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    (tmp_path / "test_sample.py").write_text(PYTEST_TEST, encoding="utf-8")
    return tmp_path


@pytest.fixture()
def tool(workspace: Path) -> RunCommandTool:
    return RunCommandTool(Settings(workspace=workspace, exec_timeout=60))


def test_successful_command_returns_stdout_and_zero_exit(tool: RunCommandTool):
    result = tool.run(command=f'"{sys.executable}" -c "print(40 + 2)"', timeout=60)
    assert result.ok is True
    assert "42" in result.content
    assert "退出码 0" in result.content
    # 协议标记（[OK]/[ERROR]）由 Agent 循环统一添加，工具自身的 content 保持干净。
    # 两处各自格式化会导致消息里出现 "[OK] [OK]"——真实发生过的缺陷。
    assert "[OK]" not in result.content


def test_failing_command_reports_exit_code_and_stderr(tool: RunCommandTool):
    result = tool.run(command=f'"{sys.executable}" -c "{PROBE.format(code=3)}"', timeout=60)
    assert result.ok is False
    assert "[ERROR]" not in result.content
    assert "退出码 3" in result.content
    assert "--- stdout ---" in result.content
    assert "--- stderr ---" in result.content
    assert "err" in result.content


def test_output_sections_are_omitted_when_empty(tool: RunCommandTool):
    result = tool.run(command=f'"{sys.executable}" -c "pass"', timeout=60)
    assert result.ok is True
    assert "--- stdout ---" not in result.content
    assert "命令没有产生任何输出" in result.content


def test_timeout_is_reported_actionably(tool: RunCommandTool):
    result = tool.run(
        command=f'"{sys.executable}" -c "import time; time.sleep(30)"',
        timeout=1.5,
    )
    assert result.ok is False
    assert "超时" in result.content
    assert "已连同其子进程一起终止" in result.content
    assert "交互式等待或死循环" in result.content  # 给出可操作的排查方向


def test_timeout_is_clamped_to_the_configured_ceiling(tool: RunCommandTool):
    """模型给超大 timeout 不能绕过整体预算控制。"""
    result = tool.run(command=f'"{sys.executable}" -c "pass"', timeout=99999)
    assert result.ok is True
    assert f"超时上限 {MAX_TIMEOUT_SEC:g}s" in result.content


def test_non_positive_timeout_falls_back_to_default(workspace: Path):
    tool = RunCommandTool(Settings(workspace=workspace, exec_timeout=25))
    result = tool.run(command=f'"{sys.executable}" -c "pass"', timeout=0)
    assert result.ok is True
    assert "超时上限 25s" in result.content


def test_missing_executable_is_reported_clearly(tool: RunCommandTool):
    result = tool.run(command="definitely-not-a-real-binary-xyz --version", timeout=30)
    assert result.ok is False
    assert "启动失败" in result.content
    assert "找不到可执行文件" in result.content


def test_command_runs_inside_the_workspace_not_the_project_cwd(tool: RunCommandTool, workspace: Path):
    """默认执行目录必须是工作区，否则 Agent 会跑到项目根目录去乱写。"""
    result = tool.run(
        command=f'"{sys.executable}" -c "import os; print(os.getcwd())"',
        timeout=60,
    )
    assert result.ok is True
    assert str(workspace).lower() in result.content.lower()


def test_cwd_can_point_into_a_workspace_subdirectory(tool: RunCommandTool, workspace: Path):
    nested = workspace / "pkg"
    nested.mkdir()
    result = tool.run(
        command=f'"{sys.executable}" -c "import os; print(os.getcwd())"',
        cwd="pkg",
        timeout=60,
    )
    assert result.ok is True
    assert "pkg" in result.content


def test_escape_cwd_outside_workspace_is_rejected(tool: RunCommandTool):
    result = tool.run(command=f'"{sys.executable}" -c "pass"', cwd="../..", timeout=30)
    assert result.ok is False
    assert "执行目录不可用" in result.content
    assert "越界" in result.content


def test_empty_command_is_rejected(tool: RunCommandTool):
    for command in ("", "   "):
        result = tool.run(command=command)
        assert result.ok is False
        assert "不能为空" in result.content


def test_destructive_command_is_refused(tool: RunCommandTool):
    result = tool.run(command="rm -rf / --no-preserve-root")
    assert result.ok is False
    assert "安全护栏" in result.content


def test_execution_can_be_disabled_by_configuration(workspace: Path):
    tool = RunCommandTool(Settings(workspace=workspace, allow_code_execution=False))
    result = tool.run(command=f'"{sys.executable}" -c "print(1)"')
    assert result.ok is False
    assert "已被配置禁用" in result.content


def test_shell_metacharacters_are_passed_through_as_literal_arguments(tool: RunCommandTool):
    """命令不经过 shell：`&&`、`|` 会被当作普通参数而非连接符。

    这不是缺陷，而是有意的设计——它让"Agent 到底执行了什么"在轨迹里可以逐参数核对。
    验证方式是让子进程把 sys.argv 原样打印出来，看这些字符是不是数据。
    """
    result = tool.run(
        command=f'"{sys.executable}" -c "import sys; print(sys.argv[1:])" a && b | c',
        timeout=30,
    )
    assert result.ok is True
    assert "['a', '&&', 'b', '|', 'c']" in result.content


def test_pycache_is_not_written_into_the_workspace(tool: RunCommandTool, workspace: Path):
    """工作区必须保持干净：评测时它同时是被测代码与 Agent 产物的载体。"""
    (workspace / "mod.py").write_text("VALUE = 1\n", encoding="utf-8")
    result = tool.run(
        command=f'"{sys.executable}" -c "import mod; print(mod.VALUE)"',
        timeout=60,
    )
    assert result.ok is True
    assert "1" in result.content
    assert not (workspace / "__pycache__").exists()


def test_long_output_keeps_the_tail_where_failures_appear(tool: RunCommandTool):
    code = "for i in range(4000): print(f'line {i}')"
    result = tool.run(command=f'"{sys.executable}" -c "{code}"', timeout=60)
    assert result.ok is True
    assert "此处省略" in result.content
    assert "line 3999" in result.content  # 末尾被保留


def test_real_pytest_run_gives_usable_failure_information(tool: RunCommandTool, workspace: Path):
    """最有价值的一条：Agent 真的跑一次 pytest，并拿到足够修复的失败信息。

    这是"A0 能自发形成执行反馈闭环"这一观察项的技术前提。
    """
    result = tool.run(command=f'"{sys.executable}" -m pytest test_sample.py -q', timeout=120)
    assert result.ok is False  # 有一个用例故意写成失败
    assert "1 failed" in result.content
    assert "1 passed" in result.content
    assert "test_bad" in result.content
    assert "expected 2 but got 3" in result.content
    assert not (workspace / "__pycache__").exists()


def test_schema_declares_command_as_required(tool: RunCommandTool):
    schema = tool.schema()["function"]
    assert schema["name"] == "run_command"
    assert schema["parameters"]["required"] == ["command"]
    assert "shell" in schema["description"]  # 必须明确告知"不经过 shell"
