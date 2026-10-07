"""Runner 与汇总层测试。

用注入的脚本化 Agent 驱动整条管线：不联网、不需要 API Key、结果确定。
覆盖三件事：

1. **断点续跑**——30 个实例的实验必须能在崩溃后接着跑，否则迭代不动；
2. **状态判定**——`no_tests` / `import_error` / `partial_pass` / `all_pass` 的区分
   直接决定失败分类的可信度；
3. **汇总不做筛选**——协议 §5 的 ITT 原则：所有运行都进分母。
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from code_agent.agent import Agent
from code_agent.config import Settings
from eval.dataset import Instance
from eval.report import (
    failure_cases,
    mutation_scores,
    quality_curves,
    render_main_table,
    summarize_variant,
    write_report,
)
from eval.runner import (
    CHECKPOINTS,
    RunOutcome,
    Variant,
    default_variant,
    load_results,
    run_batch,
    run_single,
)

SOLUTION = '''def classify(value, low, high):
    """把 value 分类到区间内。"""
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
WEAK_TEST = "from solution import classify\n\n\ndef test_smoke():\n    classify(5, 0, 10)\n"


@pytest.fixture()
def instance() -> Instance:
    return Instance(
        instance_id="SIMPLE/0",
        prompt='def classify(value, low, high):\n    """把 value 分类到区间内。"""\n',
        solution=SOLUTION.split('"""', 2)[-1],
        entry_point="classify",
        official_tests=(
            "def check(candidate):\n"
            "    assert candidate(-1, 0, 10) == -1\n"
            "    assert candidate(99, 0, 10) == 1\n"
            "    assert candidate(5, 0, 10) == 0\n"
        ),
    )


def _fake_agent_factory(test_source: str, *, write: bool = True):
    """构造一个不调用 LLM 的 Agent：直接"生成"给定的测试文件后自然结束。

    这是 `agent_factory` 注入点的用途——让评测管线可以在完全离线、确定性的条件下被测试。
    """
    from tests.helpers import ScriptedLLM, tool_response, text_response

    def factory(variant: Variant, settings: Settings, registry, workspace: Path) -> Agent:
        if write:
            (Path(workspace) / "test_solution.py").write_text(test_source, encoding="utf-8")
        llm = ScriptedLLM(
            [
                tool_response(("write_file", {"path": "test_solution.py", "content": test_source})),
                text_response("完成"),
            ]
        )
        return Agent(
            llm=llm,
            tools=registry,
            system_prompt=variant.resolve_system_prompt(),
            max_turns=variant.max_turns,
        )

    return factory


def _settings_factory(workspace: Path) -> Settings:
    return Settings(workspace=workspace, allow_write=True, allow_code_execution=False)


# ----------------------------------------------------------------------
# run_single
# ----------------------------------------------------------------------
def test_solution_modified_is_restored_before_final_measurement(tmp_path: Path, instance: Instance):
    """Agent 改写 solution.py 不能进入测量口径，也必须留下可见痕迹。

    测试断言 classify(-1,0,10) == -1；Agent 先把实现改坏成永远返回 0 的桩。
    采集入口会把实现恢复为原始版本再测量——"改实现迁就测试"这条作弊通道
    在测量上无利可图；同时 solution_modified 标志让该行为在失败分类里可见。
    """
    stub_solution = "def classify(value, low, high):\n    return 0\n"

    from tests.helpers import ScriptedLLM, tool_response, text_response

    def factory(variant: Variant, settings: Settings, registry, workspace: Path) -> Agent:
        (Path(workspace) / "solution.py").write_text(stub_solution, encoding="utf-8")
        (Path(workspace) / "test_solution.py").write_text(STRONG_TEST, encoding="utf-8")
        llm = ScriptedLLM(
            [
                tool_response(("write_file", {"path": "test_solution.py", "content": STRONG_TEST})),
                text_response("完成"),
            ]
        )
        return Agent(
            llm=llm,
            tools=registry,
            system_prompt=variant.resolve_system_prompt(),
            max_turns=variant.max_turns,
        )

    outcome = run_single(
        instance,
        default_variant(),
        run_root=tmp_path / "runs",
        settings_factory=_settings_factory,
        agent_factory=factory,
        checkpoints=(1, 2),
        max_mutants=5,
    )
    # 标志必须为真（桩在第一次采集时被发现），且指标按原始实现测出——
    # STRONG_TEST 对原始实现是有效测试，所以成绩是 all_pass 而不是被桩抬高或压低。
    assert outcome.solution_modified is True
    assert outcome.checkpoints[0]["solution_modified"] is True
    assert outcome.status == "all_pass"
    assert outcome.final["mutation_score"] is not None
    # 恢复后的工作区必须是原始实现
    assert (tmp_path / "runs" / default_variant().name / instance.instance_id / "solution.py").read_text(
        encoding="utf-8"
    ) == instance.solution_source


def test_run_single_produces_metrics_and_strong_status(tmp_path: Path, instance: Instance):
    outcome = run_single(
        instance,
        default_variant(),
        run_root=tmp_path / "runs",
        settings_factory=_settings_factory,
        agent_factory=_fake_agent_factory(STRONG_TEST),
        checkpoints=(1, 2),
        max_mutants=5,
    )
    assert outcome.status == "all_pass"
    assert outcome.final["all_pass"] is True
    assert outcome.final["mutation_score"] is not None
    assert outcome.final["mutants_total"] > 0
    assert outcome.agent["llm_calls"] >= 1
    assert "def test_below" in outcome.tests_source
    assert outcome.environment["python"]


def test_run_single_records_checkpoint_curve(tmp_path: Path, instance: Instance):
    """checkpoint 必须被记录，且 has_tests 随轮次推进而变化。"""
    outcome = run_single(
        instance,
        default_variant(),
        run_root=tmp_path / "runs",
        settings_factory=_settings_factory,
        agent_factory=_fake_agent_factory(STRONG_TEST),
        checkpoints=(1, 2),
        max_mutants=3,
    )
    assert [record["checkpoint"] for record in outcome.checkpoints] == [1, 2]
    assert outcome.checkpoints[0]["has_tests"] is True
    # checkpoint 处不采集主终点——成本高一个数量级，协议 §3 只在最终采集
    assert outcome.checkpoints[0]["mutation_score"] is None


def test_run_single_reports_cumulative_turns_not_the_last_call(tmp_path: Path, instance: Instance):
    """turns 必须是累计值，且 run 结束后不得被拉起幽灵轮次。

    checkpoint 循环会多次调用 `run_until`，每次返回的是"本次调用跑了几个 turn"
    （`paused` 时为 0）。若报告取那个值，会出现"实际跑了 8 个 turn 却显示 turns=0"。
    另外模型自然完成（completed）后，旧的实现会无条件再调一次 agent.run()——
    多烧一次 LLM 调用、多出一个无意义轮次。修复后 run 一旦结束就不再续跑。
    """
    outcome = run_single(
        instance,
        default_variant(),
        run_root=tmp_path / "runs",
        settings_factory=_settings_factory,
        agent_factory=_fake_agent_factory(STRONG_TEST),
        checkpoints=(1, 2),
        max_mutants=3,
    )
    assert outcome.agent["turns"] >= 2, outcome.agent
    # 写文件（turn 1）+ 收尾文本（turn 2）= 恰好 2；幽灵第三轮不应存在
    assert outcome.agent["turns"] == 2, outcome.agent


def test_run_single_without_writing_tests_reports_no_tests(tmp_path: Path, instance: Instance):
    outcome = run_single(
        instance,
        default_variant(),
        run_root=tmp_path / "runs",
        settings_factory=_settings_factory,
        agent_factory=_fake_agent_factory("", write=False),
        checkpoints=(1,),
        max_mutants=3,
    )
    assert outcome.status == "no_tests"
    assert outcome.final["has_tests"] is False
    assert outcome.final["line_coverage"] == 0.0
    assert outcome.final["mutation_score"] == 0


def test_run_single_detects_unimportable_tests(tmp_path: Path, instance: Instance):
    outcome = run_single(
        instance,
        default_variant(),
        run_root=tmp_path / "runs",
        settings_factory=_settings_factory,
        agent_factory=_fake_agent_factory("import not_a_real_module\n"),
        checkpoints=(1,),
        max_mutants=3,
    )
    assert outcome.status == "import_error"
    assert outcome.final["import_ok"] is False


def test_run_single_detects_partial_pass(tmp_path: Path, instance: Instance):
    broken = "from solution import classify\n\n\ndef test_wrong():\n    assert classify(5, 0, 10) == 99\n"
    outcome = run_single(
        instance,
        default_variant(),
        run_root=tmp_path / "runs",
        settings_factory=_settings_factory,
        agent_factory=_fake_agent_factory(broken),
        checkpoints=(1,),
        max_mutants=3,
    )
    assert outcome.status == "partial_pass"
    assert outcome.final["import_ok"] is True
    assert outcome.final["all_pass"] is False


def test_run_single_isolates_failures_from_the_batch(tmp_path: Path, instance: Instance):
    """Agent 工厂抛异常时，该实例应记为 eval_error 而不是让整批倒下。"""

    def exploding_factory(variant, settings, registry, workspace):
        raise RuntimeError("模拟 Agent 构造失败")

    outcome = run_single(
        instance,
        default_variant(),
        run_root=tmp_path / "runs",
        settings_factory=_settings_factory,
        agent_factory=exploding_factory,
        checkpoints=(1,),
    )
    assert outcome.status == "eval_error"
    assert "模拟 Agent 构造失败" in outcome.error


def test_workspace_is_recreated_for_each_run(tmp_path: Path, instance: Instance):
    """同一路径复用时必须先清空，否则上一次的产物会泄漏进这一次的测量。"""
    root = tmp_path / "runs"
    variant = default_variant()
    stale = root / variant.name / instance.instance_id / "test_solution.py"
    stale.parent.mkdir(parents=True)
    stale.write_text("from solution import classify\n", encoding="utf-8")

    run_single(
        instance,
        variant,
        run_root=root,
        settings_factory=_settings_factory,
        agent_factory=_fake_agent_factory(STRONG_TEST),
        checkpoints=(1,),
        max_mutants=3,
    )
    # 旧内容被清掉，只剩这一次写入的测试
    content = stale.read_text(encoding="utf-8")
    assert "def test_below" in content


# ----------------------------------------------------------------------
# run_batch：并发、写盘、续跑
# ----------------------------------------------------------------------
def _batch_kwargs(tmp_path: Path, instance: Instance):
    return dict(
        instances=[instance],
        variants=[default_variant()],
        output_dir=tmp_path / "out",
        settings_factory=_settings_factory,
        agent_factory=_fake_agent_factory(STRONG_TEST),
        checkpoints=(1,),
        max_mutants=3,
        concurrency=1,
    )


def test_run_batch_writes_one_result_file_per_instance(tmp_path: Path, instance: Instance):
    outcomes = run_batch(**_batch_kwargs(tmp_path, instance))
    assert len(outcomes) == 1
    result_files = list((tmp_path / "out" / "A0").glob("*.json"))
    assert len(result_files) == 1
    payload = json.loads(result_files[0].read_text(encoding="utf-8"))
    assert payload["instance_id"] == instance.instance_id
    assert payload["variant"] == "A0"


def test_run_batch_resume_skips_completed_instances(tmp_path: Path, instance: Instance):
    """断点续跑：第二次调用不应重跑已完成的实例。

    这是"实验能在有限时间里迭代"的前提——跑到一半崩了不能从头再来。
    """
    kwargs = _batch_kwargs(tmp_path, instance)
    run_batch(**kwargs)

    calls = {"count": 0}
    inner = kwargs["agent_factory"]

    def counting_factory(variant, settings, registry, workspace):
        calls["count"] += 1
        return inner(variant, settings, registry, workspace)

    kwargs["agent_factory"] = counting_factory
    run_batch(**kwargs)
    assert calls["count"] == 0, "已完成的实例被重跑了"


def test_run_batch_no_resume_reruns_everything(tmp_path: Path, instance: Instance):
    kwargs = _batch_kwargs(tmp_path, instance)
    run_batch(**kwargs)

    calls = {"count": 0}
    inner = kwargs["agent_factory"]

    def counting_factory(variant, settings, registry, workspace):
        calls["count"] += 1
        return inner(variant, settings, registry, workspace)

    run_batch(**{**kwargs, "agent_factory": counting_factory, "resume": False})
    assert calls["count"] == 1, "关闭续跑后已有结果应被重跑"


def test_results_can_be_loaded_back(tmp_path: Path, instance: Instance):
    run_batch(**_batch_kwargs(tmp_path, instance))
    loaded = load_results(tmp_path / "out")
    assert len(loaded) == 1
    assert loaded[0].status == "all_pass"
    assert "def test_below" in loaded[0].tests_source


# ----------------------------------------------------------------------
# 汇总层：不做筛选
# ----------------------------------------------------------------------
def _outcome(status: str, mutation, coverage: float = 0.5, variant: str = "A0") -> RunOutcome:
    return RunOutcome(
        instance_id=f"X/{status}",
        variant=variant,
        status=status,
        agent={"turns": 3, "total_tokens": 100},
        final={
            "all_pass": status == "all_pass",
            "import_ok": status in ("all_pass", "partial_pass"),
            "has_tests": status != "no_tests",
            "line_coverage": coverage,
            "mutation_score": mutation,
        },
    )


def test_every_started_run_counts_toward_the_denominator():
    """协议 §5 的 ITT 原则：失败的运行也必须进分母。"""
    outcomes = [
        _outcome("all_pass", 0.8),
        _outcome("no_tests", None),
        _outcome("import_error", 0.0),
        _outcome("timeout", None),
        _outcome("llm_error", 0.0),
    ]
    summary = summarize_variant("A0", outcomes)
    assert summary.n == 5
    assert summary.all_pass_rate == pytest.approx(0.2)
    assert sum(summary.status_counts.values()) == 5


def test_unmeasured_mutation_is_excluded_from_its_denominator_only():
    """未采集的杀伤率不进杀伤率分母，但该实例的其它指标仍计入。"""
    outcomes = [_outcome("all_pass", 0.8), _outcome("no_tests", None), _outcome("all_pass", 0.6)]
    summary = summarize_variant("A0", outcomes)
    assert summary.n == 3
    assert summary.mutation_n == 2
    assert summary.mutation_mean == pytest.approx(0.7)


def test_mutation_scores_helper_skips_none_but_keeps_zero():
    outcomes = [_outcome("a", 0.0), _outcome("b", None), _outcome("c", 0.5)]
    assert mutation_scores(outcomes) == [0.0, 0.5]


def test_quality_curve_aggregates_by_checkpoint():
    outcomes = [
        RunOutcome(
            instance_id=f"X/{index}",
            variant="A0",
            status="all_pass",
            checkpoints=[
                {"checkpoint": 1, "all_pass": False, "line_coverage": 0.1, "has_tests": True},
                {"checkpoint": 2, "all_pass": True, "line_coverage": 0.5, "has_tests": True},
            ],
        )
        for index in range(4)
    ]
    curves = quality_curves(outcomes)
    assert curves["1"][0]["line_coverage"] == pytest.approx(0.1)
    assert curves["2"][0]["all_pass_rate"] == pytest.approx(1.0)
    assert curves["1"][0]["n"] == 4


def test_failure_cases_groups_instance_ids_by_status():
    outcomes = [_outcome("no_tests", None), _outcome("no_tests", None), _outcome("timeout", None)]
    buckets = failure_cases(outcomes)
    assert buckets["no_tests"] == ["X/no_tests", "X/no_tests"]
    assert "timeout" in buckets


def test_main_table_renders_unmeasured_mutation_explicitly():
    """主表不能把"未采集"显示成 0——那会被读成"测得 0 分"。"""
    table = render_main_table([summarize_variant("A0", [_outcome("no_tests", None)])])
    assert "未采集" in table


def test_report_writes_markdown_json_and_csv(tmp_path: Path):
    outcomes = [
        _outcome("all_pass", 0.8, variant="A0"),
        _outcome("partial_pass", 0.3, variant="A0"),
        _outcome("all_pass", 0.9, variant="A1"),
    ]
    path = write_report(tmp_path, outcomes, title="测试报告")
    assert path.exists()

    text = path.read_text(encoding="utf-8")
    assert "测试报告" in text
    assert "A0" in text and "A1" in text
    assert (tmp_path / "summary.json").exists()
    assert (tmp_path / "per_instance.csv").exists()

    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    variants = {item["variant"]: item for item in summary["variants"]}
    assert variants["A0"]["n"] == 2
    assert variants["A1"]["n"] == 1
    assert summary["checkpoints"] == list(CHECKPOINTS)


def test_report_csv_has_one_row_per_run(tmp_path: Path):
    outcomes = [_outcome("all_pass", 0.8), _outcome("no_tests", None)]
    write_report(tmp_path, outcomes)
    rows = (tmp_path / "per_instance.csv").read_text(encoding="utf-8").strip().splitlines()
    assert len(rows) == 3  # 表头 + 2 行
    assert "instance_id" in rows[0]


def test_variant_defaults_are_general_purpose():
    """A0 的默认工具集不能包含测试专用能力，否则反事实对照失效。"""
    variant = default_variant()
    assert "run_command" in variant.tool_names
    forbidden = {"run_pytest", "coverage_report", "mutation_test"}
    assert not (set(variant.tool_names) & forbidden)
