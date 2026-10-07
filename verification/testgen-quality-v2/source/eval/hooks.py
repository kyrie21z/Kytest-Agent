"""A2/A3 的系统编排钩子：把"模型自发验证"升级为"系统确定性反馈"。

架构依据（`agent/core.py`）：变体差异只允许通过 `finish_turn` 钩子注入，循环本身
不改。钩子在每轮结束后运行，做三件事：

1. **检测**：`test_solution.py` 自上次系统运行后是否有变化（内容哈希）；
2. **执行**：变了就跑一次 pytest（系统级，不依赖模型自发调用）；
3. **反馈**：把结构化结果注入为 user 消息，并决定循环去留——
   失败 → `continue_` 强制再来一轮（修复）；通过 → `end`（A2 收尾，A3 进覆盖率）。

预算纪律：系统 pytest 次数与覆盖率轮数都有硬上限（Variant 字段冻结），
钩子绝不会把 run 拖入无限修复循环。测试文件无变化时钩子不动作，
模型若放弃修复，run 自然结束（状态如实反映为 partial_pass）。

防作弊：钩子运行 pytest 前核查 `solution.py` 是否被改写，改写过先恢复并在
反馈里注明——与采集层（`metrics.collect_metrics`）的口径一致。
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from code_agent.agent import TurnDecision
from code_agent.proc import run_capture

from .metrics import child_env
from .workspace import SOLUTION_FILENAME, TESTS_FILENAME

PYTEST_TIMEOUT_SEC = 90
COVERAGE_TIMEOUT_SEC = 180
MAX_FAILURES_IN_FEEDBACK = 5
MAX_MESSAGE_CHARS = 160


@dataclass
class HookState:
    """钩子的全部可变状态（跨 turn 与 run_until 段持久）。"""

    last_test_hash: Optional[str] = None
    pytest_runs: int = 0
    coverage_rounds: int = 0
    # 日志：每次系统动作一条，落进 outcome 供失败分类
    actions: List[Dict[str, Any]] = field(default_factory=list)


def _hash_text(text: str) -> str:
    import hashlib

    return hashlib.sha1(text.encode("utf-8", errors="replace")).hexdigest()


def _read_workspace_solution(workspace: Path, original: str) -> tuple[bool, bool]:
    """返回 (solution 是否存在, 是否与原始实现不同)。"""
    path = workspace / SOLUTION_FILENAME
    if not path.exists():
        return False, True
    try:
        current = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False, True
    return True, current != original


def _run_pytest(workspace: Path) -> Dict[str, Any]:
    """跑一次 pytest 并解析成结构化结果（不抛异常）。"""
    completed = run_capture(
        [sys.executable, "-m", "pytest", TESTS_FILENAME, "-q", "--no-header",
         "-p", "no:cacheprovider", "--tb=no", "-rA"],
        cwd=str(workspace), timeout=PYTEST_TIMEOUT_SEC, env=child_env(workspace),
    )
    out = (completed.stdout or "") + (completed.stderr or "")
    counts: Dict[str, int] = {}
    failures: List[str] = []
    for line in out.splitlines():
        stripped = line.strip()
        # pytest 短摘要行：`FAILED test_solution.py::test_x - AssertionError: ...`
        # `PASSED`/`SKIPPED` 等同格式，由 `-rA` 打开
        for tag in ("FAILED", "ERROR"):
            if stripped.startswith(tag + " "):
                failures.append(stripped[:200])
        if " in " in stripped and ("passed" in stripped or "failed" in stripped or "error" in stripped):
            for value, label in re.findall(r"(\d+)\s+(passed|failed|error|errors)", stripped):
                key = "errors" if label.startswith("error") else label
                counts[key] = counts.get(key, 0) + int(value)
    status = "PASS" if completed.returncode == 0 and counts.get("passed", 0) > 0 else "FAIL"
    if completed.timed_out:
        status = "TIMEOUT"
    return {
        "status": status,
        "passed": counts.get("passed", 0),
        "failed": counts.get("failed", 0),
        "errors": counts.get("errors", 0),
        "failures": failures[:MAX_FAILURES_IN_FEEDBACK],
        "returncode": completed.returncode,
    }


def _coverage_missing_lines(workspace: Path) -> Dict[str, Any]:
    """跑一次覆盖率并返回 solution.py 的未覆盖行（压缩成区间）。"""
    data_file = workspace / ".coverage"
    json_file = workspace / ".coverage.json"
    data_file.unlink(missing_ok=True)
    json_file.unlink(missing_ok=True)
    execution = run_capture([sys.executable, "-m", "coverage", "run", "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                cwd=str(workspace), timeout=COVERAGE_TIMEOUT_SEC, env=child_env(workspace))
    if execution.timed_out or execution.returncode != 0:
        return {"error": "coverage 执行超时或测试未通过"}
    exported = run_capture([sys.executable, "-m", "coverage", "json", "-o", str(json_file), "--pretty-print"],
                cwd=str(workspace), timeout=120, env=child_env(workspace))
    if exported.timed_out or exported.returncode != 0:
        return {"error": "coverage JSON 导出失败"}
    if not json_file.exists():
        return {"error": "coverage 未生成报告"}
    try:
        payload = json.loads(json_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"error": f"coverage 报告解析失败：{exc}"}
    entry = None
    for name, value in (payload.get("files") or {}).items():
        if name.replace("\\", "/").endswith(SOLUTION_FILENAME):
            entry = value
            break
    if entry is None:
        return {"error": f"coverage 报告里没有 {SOLUTION_FILENAME}"}
    summary = entry.get("summary") or {}
    missing = [int(line) for line in entry.get("missing_lines") or []]

    def compress(lines: List[int]) -> str:
        if not lines:
            return "none"
        ranges: List[str] = []
        start = prev = lines[0]
        for line in lines[1:]:
            if line == prev + 1:
                prev = line
                continue
            ranges.append(f"{start}-{prev}" if prev > start else f"{start}")
            start = prev = line
        ranges.append(f"{start}-{prev}" if prev > start else f"{start}")
        return ", ".join(ranges)

    return {
        "percent": float(summary.get("percent_covered") or 0.0) / 100.0,
        "missing": compress(missing),
        "missing_count": len(missing),
    }


def _format_feedback(result: Dict[str, Any], *, solution_restored: bool, coverage: Optional[Dict[str, Any]]) -> str:
    """把系统动作格式化为注入给模型的 user 消息。"""
    header = "[System] Automated test run: "
    if result["status"] == "PASS":
        header += f"ALL PASS ({result['passed']} passed)"
    elif result["status"] == "TIMEOUT":
        header += "TIMEOUT (the test run did not finish in time)"
    else:
        header += f"FAIL ({result['passed']} passed, {result['failed']} failed, {result['errors']} errors)"

    lines = [header]
    if result.get("failures"):
        lines.append("Failing tests:")
        lines.extend(f"  - {item}" for item in result["failures"])
    if coverage is not None:
        if "error" in coverage:
            lines.append(f"Coverage analysis unavailable: {coverage['error']}")
        else:
            lines.append(
                f"Line coverage: {coverage['percent']:.0%}. "
                f"Uncovered lines in solution.py: {coverage['missing']}."
            )
            lines.append("Add tests that execute these uncovered lines and assert their behavior.")
    if solution_restored:
        lines.append(
            "Note: solution.py had been modified; it was restored to the original "
            "implementation. Tests must target the original code."
        )
    if result["status"] != "PASS" and coverage is None:
        lines.append("Fix the failing tests and write the file again (pass overwrite=true).")
    if coverage is not None and coverage.get("missing_count"):
        lines.append("Write the improved test file again (pass overwrite=true).")
    return "\n".join(lines)


def make_guided_hook(
    workspace: Path,
    original_solution: str,
    *,
    max_pytest_runs: int = 4,
    max_coverage_rounds: int = 0,
) -> Callable[[Any, Any], Optional[Any]]:
    """构造 A2（coverage_rounds=0）或 A3（>0）的 finish_turn 钩子。

    返回值符合 `Agent.finish_turn` 的签名：`(agent, outcome) -> TurnDecision | None`。
    """
    workspace = Path(workspace).expanduser().resolve()
    state = HookState()
    enable_coverage = max_coverage_rounds > 0
    from code_agent.agent.core import TurnDecision  # 局部导入避免循环依赖

    def finish_turn(agent, outcome) -> Optional[TurnDecision]:
        tests_path = workspace / TESTS_FILENAME
        if not tests_path.exists():
            return None
        try:
            current = tests_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
        digest = _hash_text(current)
        if digest == state.last_test_hash:
            return None  # 测试无变化：不重复运行，不追加反馈

        if state.pytest_runs >= max_pytest_runs:
            return None  # 系统运行预算耗尽：交回自然结束

        # 防作弊核查：solution.py 缺失或被改写，先恢复原实现，反馈里注明
        _, modified = _read_workspace_solution(workspace, original_solution)
        if modified:
            (workspace / SOLUTION_FILENAME).write_text(original_solution, encoding="utf-8")

        result = _run_pytest(workspace)
        state.pytest_runs += 1
        state.last_test_hash = digest

        coverage: Optional[Dict[str, Any]] = None
        decision: Optional[TurnDecision] = None
        if result["status"] == "PASS" and enable_coverage:
            if state.coverage_rounds < max_coverage_rounds:
                coverage = _coverage_missing_lines(workspace)
                state.coverage_rounds += 1
                if "error" in coverage or "missing_count" not in coverage:
                    decision = TurnDecision(end=True, reason="coverage_unavailable")
                elif coverage.get("missing_count"):
                    decision = TurnDecision(continue_=True, reason="coverage_incomplete")
                else:
                    decision = TurnDecision(end=True, reason="coverage_full")
            else:
                decision = TurnDecision(end=True, reason="tests_passed")
        elif result["status"] == "PASS":
            decision = TurnDecision(end=True, reason="tests_passed")
        else:
            decision = TurnDecision(continue_=True, reason="tests_failed")

        message = _format_feedback(result, solution_restored=modified, coverage=coverage)
        agent.state.add_user(message)
        state.actions.append(
            {
                "turn": outcome.turn,
                "pytest_runs": state.pytest_runs,
                "coverage_rounds": state.coverage_rounds,
                "status": result["status"],
                "decision": decision.reason if decision else "",
                "solution_restored": modified,
                "coverage": coverage,
            }
        )
        return decision

    finish_turn.state = state  # 供测试与结果记录检查
    return finish_turn
