"""变异引擎与测量层测试。

**这是全套测试里最要紧的一组。** mutation score 是主终点，引擎是它的测量仪器；
仪器错了，后面所有结论都是错的。因此这里既测引擎的机械正确性（变异体确实是
单点变异、确定性、可复现），也测它的判别力（强测试杀得多、弱测试杀得少）。
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from eval.dataset import load_dataset
from eval.metrics import (
    Metrics,
    parse_pytest_output,
    run_pytest_on,
)
from eval.mutation import (
    Mutant,
    generate_mutants,
    mutation_summary,
)
from eval.workspace import prepare_workspace

SIMPLE = '''def classify(value, low, high):
    """把 value 分类到区间内。"""
    if value < low:
        return -1
    if value > high:
        return 1
    return 0
'''

WEAK_TEST = "from solution import classify\n\n\ndef test_smoke():\n    assert classify(5, 0, 10) is not None\n"
STRONG_TEST = (
    "from solution import classify\n\n\n"
    "def test_below():\n    assert classify(-1, 0, 10) == -1\n\n\n"
    "def test_above():\n    assert classify(99, 0, 10) == 1\n\n\n"
    "def test_inside():\n    assert classify(5, 0, 10) == 0\n\n\n"
    "def test_boundary():\n    assert classify(0, 0, 10) == 0\n    assert classify(10, 0, 10) == 0\n"
)


def _write(workspace: Path, name: str, content: str) -> Path:
    target = workspace / name
    target.write_text(content, encoding="utf-8")
    return target


# ----------------------------------------------------------------------
# 引擎机械正确性
# ----------------------------------------------------------------------
def test_generates_multiple_mutants_for_a_simple_function():
    """一个含比较与常量的函数必须产出多个变异体。

    早先的实现每次都改"文档顺序里的第一个"可变异点，去重后每个实例只剩 1 个
    变异体——杀伤率因此失去分辨率。这条测试守住这个回归。
    """
    mutants = generate_mutants(SIMPLE, max_mutants=20)
    assert len(mutants) >= 5, [m.description for m in mutants]
    operators = mutation_summary(mutants)
    assert "ROR" in operators
    assert "RVR" in operators


def test_each_mutant_differs_from_the_original_at_exactly_one_site():
    """单点变异：变异体必须能解析，且与原程序 AST 只差一处。"""
    mutants = generate_mutants(SIMPLE, max_mutants=20)
    assert mutants
    original_dump = ast.dump(ast.parse(SIMPLE))
    for mutant in mutants:
        tree = ast.parse(mutant.source)  # 必须仍可解析
        assert ast.dump(tree) != original_dump
        assert mutant.operator in {"AOR", "ROR", "LCR", "CRP", "BCR", "RVR"}
        assert mutant.line > 0


def test_mutants_are_distinct():
    mutants = generate_mutants(SIMPLE, max_mutants=20)
    sources = [mutant.source for mutant in mutants]
    assert len(sources) == len(set(sources))


def test_generation_is_deterministic():
    """同一输入必须得到同一批变异体。

    用随机抽样的话，同一份测试在两次评测里会得到不同的杀伤率，
    实验就不可复现了。
    """
    first = generate_mutants(SIMPLE, max_mutants=20)
    second = generate_mutants(SIMPLE, max_mutants=20)
    assert [(m.mutant_id, m.source) for m in first] == [(m.mutant_id, m.source) for m in second]


def test_max_mutants_is_respected():
    assert len(generate_mutants(SIMPLE, max_mutants=2)) == 2


def test_operator_filter_is_respected():
    mutants = generate_mutants(SIMPLE, max_mutants=20, operators=["ROR"])
    assert mutants
    assert {mutant.operator for mutant in mutants} == {"ROR"}


def test_syntax_error_returns_no_mutants_instead_of_raising():
    assert generate_mutants("def broken(:\n") == []


def test_function_without_mutable_operators_yields_nothing():
    """没有可变异算子时返回空列表——这是结构性事实，不是错误。"""
    source = "def identity(value):\n    return value\n"
    assert generate_mutants(source) == []


def test_mutant_is_a_frozen_dataclass_with_serializable_dict():
    mutant = generate_mutants(SIMPLE, max_mutants=1)[0]
    assert isinstance(mutant, Mutant)
    payload = mutant.to_dict()
    assert set(payload) == {"mutant_id", "operator", "line", "column", "description"}


# ----------------------------------------------------------------------
# pytest 输出解析
# ----------------------------------------------------------------------
def test_parse_pytest_output_reads_the_summary_line():
    counts = parse_pytest_output("....\n3 failed, 5 passed in 0.12s\n", "")
    assert counts["failed"] == 3
    assert counts["passed"] == 5
    assert "3 failed" in counts["summary"]


def test_parse_pytest_output_handles_errors_and_skips():
    counts = parse_pytest_output("1 error, 2 passed, 1 skipped in 0.30s", "")
    assert counts["errors"] == 1
    assert counts["passed"] == 2
    assert counts["skipped"] == 1


def test_parse_pytest_output_returns_zeros_when_no_summary():
    """取不到汇总行时返回全零，不猜测——避免把"没跑起来"误判成通过。"""
    counts = parse_pytest_output("some random output", "")
    assert counts == {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "summary": ""}


def test_pytest_result_all_pass_requires_passing_tests():
    quiet = Metrics()
    assert quiet.all_pass is False  # 根本没跑


# ----------------------------------------------------------------------
# 判别力：引擎能区分测试质量
# ----------------------------------------------------------------------
def _measure(workspace: Path, instance) -> Metrics:
    from eval.metrics import collect_metrics

    return collect_metrics(instance, workspace, checkpoint=0, include_mutation=True)


@pytest.fixture()
def simple_instance():
    from eval.dataset import Instance

    return Instance(
        instance_id="SIMPLE/0",
        prompt='def classify(value, low, high):\n    """把 value 分类到区间内。"""\n',
        solution=SIMPLE.split('"""', 2)[-1],
        entry_point="classify",
        official_tests="def check(candidate):\n    assert candidate(-1, 0, 10) == -1\n",
    )


def test_strong_tests_score_much_higher_than_weak_tests(tmp_path: Path, simple_instance):
    """这是引擎存在的意义：它必须把强弱测试区分开。

    两个测试都"通过"、覆盖率都不低，只有杀伤率能把它们分开——
    这正是我们用杀伤率作主终点的原因。
    """
    workspace = prepare_workspace(simple_instance, tmp_path / "weak")
    _write(workspace, "test_solution.py", WEAK_TEST)
    weak = _measure(workspace, simple_instance)

    workspace = prepare_workspace(simple_instance, tmp_path / "strong")
    _write(workspace, "test_solution.py", STRONG_TEST)
    strong = _measure(workspace, simple_instance)

    assert weak.all_pass and strong.all_pass, "两个测试都应通过正确实现"
    assert weak.mutants_total > 0
    assert strong.mutation_score is not None and weak.mutation_score is not None
    assert strong.mutation_score > weak.mutation_score
    assert weak.mutation_score < 0.5
    assert strong.mutation_score > 0.5


def test_no_test_file_yields_zero_coverage_and_unmeasured_mutation(tmp_path: Path, simple_instance):
    """没有测试文件：覆盖率是 0（确实没执行），但杀伤率是"未采集"。

    把"未测量"记成"测得 0"会在聚合时系统性地压低均值——两者必须区分。
    """
    workspace = prepare_workspace(simple_instance, tmp_path / "empty")
    metrics = _measure(workspace, simple_instance)
    assert metrics.has_tests is False
    assert metrics.line_coverage == 0.0
    assert metrics.mutation_score is None
    assert metrics.all_pass is False


def test_import_error_is_distinguished_from_assertion_failure(tmp_path: Path, simple_instance):
    """测试文件根本跑不起来，与"测试断言错了"是两类不同的失败。

    这里还守住一个更隐蔽的坑：模块导入失败时，`coverage` 只把 `def` 一条语句算作
    可执行行，函数体不计入，于是报告 `executable_lines=1, percent=100%`——
    **"无法测量"伪装成"测了满分"**。测量层用 AST 口径交叉校验后必须识破它，
    宁可报错也不报一个假的满分。
    """
    workspace = prepare_workspace(simple_instance, tmp_path / "broken")
    _write(workspace, "test_solution.py", "import definitely_not_a_module\n")
    metrics = _measure(workspace, simple_instance)

    assert metrics.has_tests is True
    assert metrics.pytest.import_ok is False
    assert metrics.all_pass is False
    assert metrics.line_coverage == 0.0
    assert "口径失真" in metrics.eval_error
    # 关键断言：不能出现"导不进来却覆盖率 100%"这种自相矛盾的结果
    assert metrics.line_coverage != 1.0


def test_failing_assertion_is_reported_with_counts(tmp_path: Path, simple_instance):
    workspace = prepare_workspace(simple_instance, tmp_path / "fail")
    _write(
        workspace,
        "test_solution.py",
        "from solution import classify\n\n\ndef test_wrong():\n    assert classify(5, 0, 10) == 99\n",
    )
    metrics = _measure(workspace, simple_instance)

    assert metrics.pytest.import_ok is True   # 收集成功
    assert metrics.pytest.failed == 1
    assert metrics.all_pass is False           # 但没全过
    assert metrics.line_coverage > 0.0         # 执行到了代码


def test_solution_is_restored_after_mutation_measurement(tmp_path: Path, simple_instance):
    """变异测试必须还原被测代码，否则后续 checkpoint 都建立在被改坏的代码上。"""
    workspace = prepare_workspace(simple_instance, tmp_path / "restore")
    _write(workspace, "test_solution.py", STRONG_TEST)
    before = (workspace / "solution.py").read_text(encoding="utf-8")

    metrics = _measure(workspace, simple_instance)
    assert metrics.mutants_total > 0

    after = (workspace / "solution.py").read_text(encoding="utf-8")
    assert after == before


def test_measurement_is_repeatable(tmp_path: Path, simple_instance):
    """同一个工作区连续测量两次必须得到相同结果——否则主终点不可复现。"""
    workspace = prepare_workspace(simple_instance, tmp_path / "repeat")
    _write(workspace, "test_solution.py", STRONG_TEST)

    first = _measure(workspace, simple_instance)
    second = _measure(workspace, simple_instance)
    assert first.mutation_score == second.mutation_score
    assert first.mutants_total == second.mutants_total
    assert first.line_coverage == pytest.approx(second.line_coverage)


def test_workspace_stays_clean_after_measurement(tmp_path: Path, simple_instance):
    """测量不能在工作区留下 __pycache__ 之类的产物，否则污染后续覆盖率的行数统计。"""
    workspace = prepare_workspace(simple_instance, tmp_path / "clean")
    _write(workspace, "test_solution.py", STRONG_TEST)
    _measure(workspace, simple_instance)

    leftovers = {path.name for path in workspace.iterdir()}
    assert "__pycache__" not in leftovers
    assert ".pytest_cache" not in leftovers


def test_coverage_works_with_a_relative_workspace_path(tmp_path: Path, simple_instance, monkeypatch):
    """相对路径的工作区也必须能正确测覆盖率。

    真实踩过的坑：以相对路径作为工作区时，`coverage json -o .coverage.json` 的输出
    会被解析到工作区**内部**的嵌套目录（子进程 cwd 就是工作区），而检查逻辑仍在
    工作区根目录找文件，于是覆盖率**静默变成 0%**——不是报错，是一个假的 0。
    路径在进入测量层时必须绝对化。
    """
    workspace = prepare_workspace(simple_instance, tmp_path / "relative")
    _write(workspace, "test_solution.py", STRONG_TEST)

    monkeypatch.chdir(tmp_path)  # 让"相对路径"真的成为相对路径
    relative = workspace.relative_to(tmp_path)
    assert not relative.is_absolute()

    metrics = _measure(relative, simple_instance)
    assert metrics.line_coverage > 0.0, metrics.eval_error
    assert metrics.executable_lines > 0
    assert not (workspace / "results").exists()  # 不该在非预期位置生成报告


# ----------------------------------------------------------------------
# 真实数据集上的冒烟检查
# ----------------------------------------------------------------------
def test_real_dataset_loads_and_has_expected_shape():
    dataset = load_dataset()
    assert len(dataset) == 30
    first = dataset[0]
    assert first.instance_id.startswith("HumanEval/")
    assert first.entry_point
    assert "def " in first.solution_source
    assert "check(" in first.official_test_source


def test_official_tests_pass_on_the_reference_solution(tmp_path: Path):
    """官方测试必须能在参考实现上全部通过。

    这条不成立的话，整个 baseline 就不可信——而 baseline 是主表的对照锚点。
    """
    instance = load_dataset()[0]
    workspace = prepare_workspace(instance, tmp_path / "official")
    from eval.workspace import OFFICIAL_TESTS_FILENAME, write_official_tests

    write_official_tests(instance, workspace)
    result = run_pytest_on(OFFICIAL_TESTS_FILENAME, workspace)
    assert result.all_pass, result.stdout
