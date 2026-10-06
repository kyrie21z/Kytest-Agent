"""A2/A3 编排钩子测试（eval/hooks.py）。

用脚本化 LLM 驱动真实 Agent + 真实 pytest（临时工作区，不联网、确定），
覆盖五个决定性场景：

1. 失败 → 结构化反馈 → 修复 → 通过 → 收尾（A2 的完整闭环）；
2. 一次通过即收尾（A2 的确定性终止）；
3. 测试文件无变化时不重复运行、不追加反馈（防预算泄漏）；
4. A3：通过后覆盖率分析 → 未覆盖行定向反馈 → 补测 → 覆盖率封顶收尾；
5. 防作弊：solution.py 被改写时，钩子恢复原实现并在反馈中注明。
"""
from __future__ import annotations

from pathlib import Path

from code_agent.agent import Agent
from code_agent.config import Settings
from code_agent.tools.factories import build_registry
from eval.hooks import make_guided_hook

SOLUTION = '''def classify(value, low, high):
    """Return -1 below, 1 above, 0 inside."""
    if value < low:
        return -1
    if value > high:
        return 1
    return 0
'''

STRONG_TEST = (
    "from solution import classify\n\n\n"
    "def test_below():\n    assert classify(-1, 0, 10) == -1\n\n\n"
    "def test_above():\n    assert classify(99, 0, 10) == 1\n\n\n"
    "def test_inside():\n    assert classify(5, 0, 10) == 0\n"
)
WEAK_TEST = (
    "from solution import classify\n\n\n"
    "def test_inside():\n    assert classify(5, 0, 10) == 0\n"
)
FAILING_TEST = (
    "from solution import classify\n\n\n"
    "def test_wrong():\n    assert classify(5, 0, 10) == 99\n"
)


def _settings(workspace: Path) -> Settings:
    return Settings(workspace=workspace, allow_write=True, allow_code_execution=False)


def _run_agent(workspace: Path, llm_responses, *, finish_turn) -> Agent:
    """构造真实 Agent（脚本化 LLM + 真实工具注册表）并跑完一次任务。"""
    agent = Agent(
        llm=llm_responses,
        tools=build_registry(_settings(workspace)),
        system_prompt="You are a coding agent.",
        max_turns=12,
        finish_turn=finish_turn,
    )
    agent.state.add_user("Generate unit tests for solution.py. Write them to test_solution.py.")
    agent.run()
    return agent


def _injected_messages(agent: Agent) -> list[str]:
    return [
        str(m.get("content") or "")
        for m in agent.state.messages
        if m.get("role") == "user" and str(m.get("content") or "").startswith("[System]")
    ]


def test_fail_then_repair_then_pass(tmp_path: Path):
    """失败回灌 → 修复 → 通过收尾：A2 的完整闭环。"""
    from tests.helpers import ScriptedLLM, text_response, tool_response

    workspace = tmp_path / "ws"
    workspace.mkdir()
    (workspace / "solution.py").write_text(SOLUTION, encoding="utf-8")
    hook = make_guided_hook(workspace, SOLUTION, max_pytest_runs=4, max_coverage_rounds=0)
    llm = ScriptedLLM(
        [
            tool_response(("write_file", {"path": "test_solution.py", "content": FAILING_TEST})),
            tool_response(("write_file", {"path": "test_solution.py", "content": STRONG_TEST, "overwrite": True})),
            text_response("done"),
        ]
    )
    agent = _run_agent(workspace, llm, finish_turn=hook)

    injected = _injected_messages(agent)
    assert len(injected) == 2
    assert "FAIL" in injected[0] and "Failing tests:" in injected[0]
    assert "ALL PASS" in injected[1]
    assert hook.state.pytest_runs == 2
    # 第二次注入后钩子以 end 收尾，循环停止而不是让模型继续说话
    assert agent.state.turn_index == 2


def test_pass_on_first_write_ends_run(tmp_path: Path):
    """一次通过即收尾：系统终止，不需要模型再收尾一轮。"""
    from tests.helpers import ScriptedLLM, tool_response

    workspace = tmp_path / "ws"
    workspace.mkdir()
    (workspace / "solution.py").write_text(SOLUTION, encoding="utf-8")
    hook = make_guided_hook(workspace, SOLUTION, max_pytest_runs=4, max_coverage_rounds=0)
    llm = ScriptedLLM(
        [tool_response(("write_file", {"path": "test_solution.py", "content": STRONG_TEST}))]
    )
    agent = _run_agent(workspace, llm, finish_turn=hook)

    injected = _injected_messages(agent)
    assert len(injected) == 1 and "ALL PASS" in injected[0]
    assert hook.state.pytest_runs == 1
    assert agent.state.turn_index == 1


def test_unchanged_tests_do_not_trigger_rerun(tmp_path: Path):
    """测试文件无变化：不重复运行 pytest，不追加反馈（防预算泄漏）。"""
    from tests.helpers import ScriptedLLM, text_response, tool_response

    workspace = tmp_path / "ws"
    workspace.mkdir()
    (workspace / "solution.py").write_text(SOLUTION, encoding="utf-8")
    hook = make_guided_hook(workspace, SOLUTION, max_pytest_runs=4, max_coverage_rounds=0)
    llm = ScriptedLLM(
        [
            tool_response(("write_file", {"path": "test_solution.py", "content": FAILING_TEST})),
            text_response("I cannot fix it."),
        ]
    )
    agent = _run_agent(workspace, llm, finish_turn=hook)

    assert hook.state.pytest_runs == 1
    assert len(_injected_messages(agent)) == 1


def test_coverage_feedback_and_rounds_cap(tmp_path: Path):
    """A3：通过后覆盖率分析 → 未覆盖行反馈 → 补测 → 第二轮封顶收尾。"""
    from tests.helpers import ScriptedLLM, tool_response

    workspace = tmp_path / "ws"
    workspace.mkdir()
    (workspace / "solution.py").write_text(SOLUTION, encoding="utf-8")
    hook = make_guided_hook(workspace, SOLUTION, max_pytest_runs=4, max_coverage_rounds=2)
    llm = ScriptedLLM(
        [
            tool_response(("write_file", {"path": "test_solution.py", "content": WEAK_TEST})),
            tool_response(("write_file", {"path": "test_solution.py", "content": STRONG_TEST, "overwrite": True})),
        ]
    )
    agent = _run_agent(workspace, llm, finish_turn=hook)

    injected = _injected_messages(agent)
    # 第一次：通过但覆盖率不满 → 定向反馈；第二次：补测后覆盖率满 → 收尾
    assert len(injected) == 2
    assert "Uncovered lines" in injected[0]
    assert "Line coverage: 100%" in injected[1] or "Uncovered lines: 无" in injected[1]
    assert hook.state.coverage_rounds == 2
    assert hook.state.pytest_runs == 2


def test_hook_restores_modified_solution(tmp_path: Path):
    """防作弊：solution.py 被改写时，钩子恢复原实现并在反馈中注明。"""
    from tests.helpers import ScriptedLLM, tool_response

    workspace = tmp_path / "ws"
    workspace.mkdir()
    stub = "def classify(value, low, high):\n    return 0\n"
    (workspace / "solution.py").write_text(stub, encoding="utf-8")
    hook = make_guided_hook(workspace, SOLUTION, max_pytest_runs=4, max_coverage_rounds=0)
    llm = ScriptedLLM(
        [tool_response(("write_file", {"path": "test_solution.py", "content": STRONG_TEST}))]
    )
    agent = _run_agent(workspace, llm, finish_turn=hook)

    assert hook.state.actions[0]["solution_restored"] is True
    assert "restored to the original" in _injected_messages(agent)[0]
    # 反馈针对原始实现：STRONG_TEST 在原始实现上通过
    assert "ALL PASS" in _injected_messages(agent)[0]
    assert (workspace / "solution.py").read_text(encoding="utf-8") == SOLUTION
