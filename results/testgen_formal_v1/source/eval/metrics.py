"""测量层：把工作区里的产出转成协议定义的指标。

三层测量，成本依次上升：

| 层 | 方法 | 成本 |
|---|---|---|
| 可通过性 | `pytest` 一次 | 百毫秒级 |
| 覆盖率 | `coverage run` + `coverage json` | 秒级 |
| 变异杀伤率 | 每个变异体一次 pytest | 十秒级 |

**测量档位**（协议 §3 补充）：checkpoint 处的质量曲线只采集前两层，
主终点只在运行结束后采集。理由是成本——30 个实例 × 4 个 checkpoint × 20 个变异体
= 2400 次 pytest，仅这一项就要一小时以上，而曲线本身只需要一个能反映进展的指标。
这样既不丢掉"进展 vs 预算"的信息，也不把预算烧在重复测量上。
"""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from code_agent.proc import run_capture

from .mutation import Mutant, generate_mutants, mutation_summary
from .source_stats import _MIN_RATIO
from .workspace import SOLUTION_FILENAME, clean_ephemeral, has_tests, restore_solution

PYTEST_TIMEOUT_SEC = 120
MUTANT_TIMEOUT_SEC = 60
COVERAGE_TIMEOUT_SEC = 180

# 子进程基础环境：输出稳定、不写字节码缓存（评测后工作区必须干净）
_BASE_ENV = {
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONIOENCODING": "utf-8",
    "PYTHONUNBUFFERED": "1",
}


def child_env(workspace: Path) -> Dict[str, str]:
    """构造子进程环境，**把工作区显式放进 PYTHONPATH**。

    这一步不能省。pytest 8 默认的 import 模式不会可靠地把"被测文件所在目录"
    加进 `sys.path`：显式指定目标路径运行时通常可以，但 `coverage run -m pytest`
    （不带目标路径）就会失败，报 `ModuleNotFoundError: No module named 'solution'`。
    表现是"覆盖率报 no data / 测试收集失败"，而真正的原因藏在 import 机制里。

    只**追加**工作区，不丢弃已有的 `PYTHONPATH`——`os.environ` 里可能有解释器
    自身需要的路径，覆盖掉会让子进程里连 pytest 都导入不了。
    """
    env = dict(_BASE_ENV)
    existing = os.environ.get("PYTHONPATH", "")
    parts = [str(Path(workspace).resolve())]
    if existing:
        parts.append(existing)
    env["PYTHONPATH"] = os.pathsep.join(parts)
    return env

# pytest 汇总行，例如 "3 failed, 5 passed in 0.12s" / "2 passed, 1 warning in 0.05s"
_SUMMARY = re.compile(
    r"^(?=.*\b(?:passed|failed|error|errors|skipped|xfailed|xpassed)\b)"
    r".*\bin \d+(?:\.\d+)?s",
    re.IGNORECASE,
)
_COUNT = re.compile(r"(\d+)\s+(passed|failed|error|errors|skipped|xfailed|xpassed|warning|warnings)", re.I)


@dataclass
class PytestResult:
    """一次 pytest 运行的结构化结果。"""

    ran: bool = False
    returncode: Optional[int] = None
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    timed_out: bool = False
    duration_sec: float = 0.0
    summary_line: str = ""
    stdout: str = ""
    stderr: str = ""

    @property
    def collected(self) -> int:
        return self.passed + self.failed + self.skipped

    @property
    def all_pass(self) -> bool:
        """全部通过且无收集错误。

        这是协议 §2.2 的门槛指标。`errors > 0` 一律判否——包括测试文件无法导入、
        fixture 报错、收集期异常。
        """
        return (
            self.ran
            and not self.timed_out
            and self.returncode == 0
            and self.failed == 0
            and self.errors == 0
            and self.passed > 0
        )

    @property
    def import_ok(self) -> bool:
        """测试文件能否被正常收集。用于区分"测试逻辑错"与"文件根本跑不起来"。"""
        return self.ran and not self.timed_out and self.errors == 0 and self.collected > 0

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload.pop("stdout", None)
        payload.pop("stderr", None)
        payload["all_pass"] = self.all_pass
        payload["import_ok"] = self.import_ok
        return payload


@dataclass
class Metrics:
    """一个 checkpoint 或最终结果上的全套指标。字段名与协议表格一一对应。"""

    checkpoint: int = 0
    has_tests: bool = False
    pytest: PytestResult = field(default_factory=PytestResult)
    line_coverage: float = 0.0
    covered_lines: int = 0
    executable_lines: int = 0
    mutation_score: Optional[float] = None      # None = 未采集（与"测得 0"不同）
    mutants_total: int = 0
    mutants_killed: int = 0
    mutants_errors: int = 0
    mutants_survived: List[Dict[str, Any]] = field(default_factory=list)
    mutant_operators: Dict[str, int] = field(default_factory=dict)
    killed_by_operator: Dict[str, int] = field(default_factory=dict)
    # 本轮采集入口处 solution.py 是否被 Agent 改写过。所有指标都针对**原始实现**
    # 测量（采集入口先恢复），所以这个标志不改变指标值，只标记行为本身——
    # "改实现迁就测试"是失败分类里的一类，必须可见。
    solution_modified: bool = False
    eval_error: str = ""
    eval_duration_sec: float = 0.0

    @property
    def all_pass(self) -> bool:
        return self.pytest.all_pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checkpoint": self.checkpoint,
            "has_tests": self.has_tests,
            "all_pass": self.all_pass,
            "import_ok": self.pytest.import_ok,
            "passed": self.pytest.passed,
            "failed": self.pytest.failed,
            "errors": self.pytest.errors,
            "pytest_returncode": self.pytest.returncode,
            "pytest_timed_out": self.pytest.timed_out,
            "pytest_summary": self.pytest.summary_line,
            "line_coverage": round(self.line_coverage, 4),
            "covered_lines": self.covered_lines,
            "executable_lines": self.executable_lines,
            "mutation_score": None if self.mutation_score is None else round(self.mutation_score, 4),
            "mutants_total": self.mutants_total,
            "mutants_killed": self.mutants_killed,
            "mutants_errors": self.mutants_errors,
            "mutants_survived": self.mutants_survived,
            "mutant_operators": self.mutant_operators,
            "killed_by_operator": self.killed_by_operator,
            "solution_modified": self.solution_modified,
            "eval_error": self.eval_error,
            "eval_duration_sec": round(self.eval_duration_sec, 3),
        }


# ----------------------------------------------------------------------
# pytest
# ----------------------------------------------------------------------
def parse_pytest_output(stdout: str, stderr: str) -> Dict[str, int]:
    """从 pytest 输出里提取计数。

    优先用汇总行，因为它是 pytest 自己算出来的、包含全部类别。取不到时返回全零，
    由调用方依据退出码判断"是否跑起来过"——不猜测，避免把没跑起来误判成通过。
    """
    text = f"{stdout}\n{stderr}"
    summary_line = ""
    for line in reversed(text.splitlines()):
        stripped = line.strip().strip("= ").strip()
        if stripped and _SUMMARY.match(stripped):
            summary_line = stripped
            break
    if not summary_line:
        return {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "summary": ""}

    counts = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}
    for value, label in _COUNT.findall(summary_line):
        label = label.lower()
        if label == "passed":
            counts["passed"] = int(value)
        elif label == "failed":
            counts["failed"] = int(value)
        elif label.startswith("error"):
            counts["errors"] = int(value)
        elif label == "skipped":
            counts["skipped"] = int(value)
    return {**counts, "summary": summary_line}


def run_pytest_on(
    target: str,
    cwd: Path,
    *,
    timeout: float = PYTEST_TIMEOUT_SEC,
    extra_args: Optional[Sequence[str]] = None,
) -> PytestResult:
    """在 `cwd` 下运行 `pytest <target>` 并解析结果。"""
    argv = [sys.executable, "-m", "pytest", target, "-q", "-p", "no:cacheprovider", "--continue-on-collection-errors"]
    if extra_args:
        argv.extend(extra_args)
    directory = Path(cwd).expanduser().resolve()
    completed = run_capture(argv, cwd=directory, timeout=timeout, env=child_env(directory))

    counts = parse_pytest_output(completed.stdout, completed.stderr)
    return PytestResult(
        ran=True,
        returncode=completed.returncode,
        passed=counts["passed"],
        failed=counts["failed"],
        errors=counts["errors"],
        skipped=counts["skipped"],
        timed_out=completed.timed_out,
        duration_sec=completed.duration_sec,
        summary_line=counts["summary"],
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


# ----------------------------------------------------------------------
# 覆盖率
# ----------------------------------------------------------------------
def measure_coverage(workspace: Path, target: str, *, timeout: float = COVERAGE_TIMEOUT_SEC) -> Dict[str, Any]:
    """测量 `target`（工作区内的相对路径）的行覆盖率。

    用 `coverage run` 而不是 `pytest-cov`：后者是插件依赖，而项目要求零第三方依赖
    （`coverage` 是评测层依赖，不进 Agent）。
    """
    from .source_stats import count_file

    workspace = Path(workspace).expanduser().resolve()
    data_file = workspace / ".coverage"
    json_file = workspace / ".coverage.json"
    for stale in (data_file, json_file):
        stale.unlink(missing_ok=True)

    lint = run_capture(
        [sys.executable, "-m", "coverage", "--version"], cwd=workspace, timeout=60, env=child_env(workspace)
    )
    if lint.returncode != 0:
        return {"error": "coverage 不可用：未安装或无法执行"}

    run_capture(
        [sys.executable, "-m", "coverage", "run", "-m", "pytest", "-q",
         "-p", "no:cacheprovider", "--continue-on-collection-errors"],
        cwd=workspace,
        timeout=timeout,
        env=child_env(workspace),
    )
    report = run_capture(
        [sys.executable, "-m", "coverage", "json", "-o", str(json_file), "--pretty-print"],
        cwd=workspace,
        timeout=120,
        env=child_env(workspace),
    )
    if not json_file.exists():
        tail = (report.stderr or report.stdout or "").strip()[-300:]
        return {"error": f"coverage 未生成报告：{tail}"}

    try:
        payload = json.loads(json_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"error": f"coverage 报告解析失败：{exc}"}

    wanted = str(target).replace("\\", "/")
    entry = None
    for name, value in (payload.get("files") or {}).items():
        if name.replace("\\", "/").endswith(wanted):
            entry = value
            break
    if entry is None:
        return {"error": f"coverage 报告里没有 {wanted}"}

    summary = entry.get("summary") or {}
    executable_lines = int(summary.get("num_statements") or 0)
    covered_lines = int(summary.get("covered_lines") or 0)

    # 交叉校验：覆盖率工具在"模块导入失败"时只数到 `def` 这一条语句，
    # 函数体不计入，于是 percent 会是 100%——"无法测量"伪装成"测了满分"。
    # 用独立的 AST 口径识破它，宁可报 0 也不能报一个假的满分。
    ast_statements = count_file(workspace / target)
    if ast_statements and executable_lines < ast_statements * _MIN_RATIO:
        return {
            "error": (
                f"覆盖率口径失真：coverage 报告可执行行 {executable_lines}，"
                f"AST 统计 {ast_statements}（测试可能未能导入被测模块）"
            )
        }

    return {
        "percent": float(summary.get("percent_covered") or 0.0) / 100.0,
        "covered_lines": covered_lines,
        "executable_lines": executable_lines,
    }


# ----------------------------------------------------------------------
# 变异测试
# ----------------------------------------------------------------------
def run_mutation_tests(
    workspace: Path,
    original_source: str,
    tests_target: str,
    *,
    max_mutants: int = 20,
    timeout: float = MUTANT_TIMEOUT_SEC,
    operators: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """对 `solution.py` 施加变异，用给定测试套件去杀。

    每个变异体都是"写入变异体 → 跑一次测试 → 判断是否被杀 → 还原"。
    还原是必须的：任何一次遗漏都会让后续测量建立在被改坏的代码上。
    """
    workspace = Path(workspace).expanduser().resolve()
    solution_path = workspace / SOLUTION_FILENAME
    mutants: List[Mutant] = generate_mutants(original_source, max_mutants=max_mutants, operators=operators)

    result: Dict[str, Any] = {
        "total": len(mutants),
        "killed": 0,
        "survived": [],
        "operators": mutation_summary(mutants),
        "killed_by_operator": {},
        "errors": 0,
    }
    if not mutants:
        return result

    killed_by_operator: Dict[str, int] = {}
    try:
        for mutant in mutants:
            solution_path.write_text(mutant.source, encoding="utf-8")
            outcome = run_pytest_on(tests_target, workspace, timeout=timeout)
            if outcome.timed_out:
                # 超时算"未杀死"：无法证明测试发现了这个变异。
                result["errors"] += 1
            elif outcome.failed > 0 or outcome.errors > 0:
                result["killed"] += 1
                killed_by_operator[mutant.operator] = killed_by_operator.get(mutant.operator, 0) + 1
            else:
                result["survived"].append(mutant.to_dict())
    finally:
        solution_path.write_text(original_source, encoding="utf-8")

    result["killed_by_operator"] = killed_by_operator
    result["score"] = result["killed"] / result["total"] if result["total"] else None
    return result


# ----------------------------------------------------------------------
# 汇总
# ----------------------------------------------------------------------
def collect_metrics(
    instance,
    workspace: Path,
    checkpoint: int,
    *,
    include_mutation: bool,
    tests_target: str = "test_solution.py",
    max_mutants: int = 20,
    pytest_timeout: float = PYTEST_TIMEOUT_SEC,
    coverage_timeout: float = COVERAGE_TIMEOUT_SEC,
    mutant_timeout: float = MUTANT_TIMEOUT_SEC,
    mutation_operators: Optional[Sequence[str]] = None,
) -> Metrics:
    """采集一个 checkpoint 上的指标。

    Args:
        include_mutation: 是否采集主终点。checkpoint 处传 False 以节省预算
            （见模块开头"测量档位"）。
    """
    import time

    started = time.monotonic()
    workspace = Path(workspace).expanduser().resolve()
    metrics = Metrics(checkpoint=checkpoint)
    clean_ephemeral(workspace)

    # 入口处先核查并恢复原始实现，再测量：pytest/coverage/变异都必须针对
    # 原始实现，Agent 对 solution.py 的任何改写都不能进入测量口径。
    solution_path = workspace / SOLUTION_FILENAME
    try:
        metrics.solution_modified = (
            not solution_path.exists()
            or solution_path.read_text(encoding="utf-8", errors="replace") != instance.solution_source
        )
    except OSError:
        metrics.solution_modified = True
    restore_solution(instance, workspace)

    metrics.has_tests = has_tests(workspace)

    if not metrics.has_tests:
        # 协议 §5：没有测试文件时覆盖率是 0（确实没执行到任何代码）。
        # 但杀伤率是 **None（未采集）** 而不是 0——该实例根本没有变异体集合，
        # 把"未测量"记成"测得 0"会在聚合时系统性地压低均值。
        metrics.line_coverage = 0.0
        metrics.mutation_score = None
        metrics.eval_duration_sec = time.monotonic() - started
        return metrics

    metrics.pytest = run_pytest_on(tests_target, workspace, timeout=pytest_timeout)

    coverage = measure_coverage(workspace, SOLUTION_FILENAME, timeout=coverage_timeout)
    if "error" in coverage:
        metrics.eval_error = str(coverage["error"])
    else:
        metrics.line_coverage = coverage["percent"]
        metrics.covered_lines = coverage["covered_lines"]
        metrics.executable_lines = coverage["executable_lines"]

    if include_mutation:
        mutation = run_mutation_tests(
            workspace, instance.solution_source, tests_target, max_mutants=max_mutants, timeout=mutant_timeout,
            operators=mutation_operators,
        )
        metrics.mutants_total = mutation["total"]
        metrics.mutants_killed = mutation["killed"]
        metrics.mutants_errors = mutation["errors"]
        metrics.mutants_survived = mutation["survived"]
        metrics.mutant_operators = mutation["operators"]
        metrics.killed_by_operator = mutation["killed_by_operator"]
        # 无变异体的实例（源码里没有可变异算子）记为 None 而不是 0：
        # 该实例无法测量杀伤率，计入分母会凭空拉低均值。协议 §2.1 已注明。
        metrics.mutation_score = mutation["score"] if mutation["total"] else None

    restore_solution(instance, workspace)
    clean_ephemeral(workspace)
    metrics.eval_duration_sec = time.monotonic() - started
    return metrics


def official_baseline(instance, workspace: Path, *, max_mutants: int = 20) -> Metrics:
    """用官方测试测一遍，作为最强对照。

    它回答的是：**"官方测试能得到多少分"**。没有这个锚点，任何杀伤率数字都无从判断好坏。
    官方测试只在测量期间存在于工作区，测完立即删除。
    """
    import time

    from .workspace import OFFICIAL_TESTS_FILENAME, write_official_tests

    started = time.monotonic()
    workspace = Path(workspace).expanduser().resolve()
    clean_ephemeral(workspace)
    official = write_official_tests(instance, workspace)
    try:
        metrics = Metrics(checkpoint=0, has_tests=True)
        metrics.pytest = run_pytest_on(OFFICIAL_TESTS_FILENAME, workspace)
        coverage = measure_coverage(workspace, SOLUTION_FILENAME)
        if "error" in coverage:
            metrics.eval_error = str(coverage["error"])
        else:
            metrics.line_coverage = coverage["percent"]
            metrics.covered_lines = coverage["covered_lines"]
            metrics.executable_lines = coverage["executable_lines"]
        mutation = run_mutation_tests(
            workspace, instance.solution_source, OFFICIAL_TESTS_FILENAME, max_mutants=max_mutants
        )
        metrics.mutants_total = mutation["total"]
        metrics.mutants_killed = mutation["killed"]
        metrics.mutants_errors = mutation["errors"]
        metrics.mutants_survived = mutation["survived"]
        metrics.mutant_operators = mutation["operators"]
        metrics.killed_by_operator = mutation["killed_by_operator"]
        metrics.mutation_score = mutation["score"] if mutation["total"] else None
        return metrics
    finally:
        official.unlink(missing_ok=True)
        restore_solution(instance, workspace)
        clean_ephemeral(workspace)
        metrics.eval_duration_sec = time.monotonic() - started
