"""Behavioral acceptance for development feedback and independent scoring."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

from code_agent.config import Settings
from code_agent.fault_feedback import FEEDBACK_OPERATORS, HELDOUT_OPERATORS, fingerprint, independent_pools
from code_agent.tools.factories import build_registry
from scripts.demo_fault_feedback import SOURCE, candidate


@pytest.fixture
def registry(tmp_path):
    (tmp_path / "solution.py").write_text(SOURCE)
    return build_registry(Settings(workspace=tmp_path), ("submit_tests", "inspect_survivors"))


def accept(registry, name, value, expected):
    result = registry.execute("submit_tests", {"cases": [candidate(name, value, expected)]})
    assert json.loads(result.content)["results"][0]["status"] == "ACCEPTED"


def test_feedback_requires_valid_private_suite_and_execution(registry):
    inspector = registry.get("inspect_survivors")
    assert not inspector.run().ok
    (inspector.workspace / "test_solution.py").write_text("def test_fake():\n    assert True\n")
    assert not inspector.run().ok
    accept(registry, "test_inside", 5, 0)
    inspector.settings.allow_code_execution = False
    assert not inspector.run().ok and not inspector.generation.snapshot()["fault_feedback"]


def test_changed_suite_gets_specific_feedback_cached_calls_cost_nothing(registry):
    accept(registry, "test_inside", 5, 0)
    tool, inspector = registry.get("submit_tests").generation, registry.get("inspect_survivors")
    stages = []
    tool.on_feedback = stages.append
    report = json.loads(registry.execute("inspect_survivors", {}).content)
    assert report["scope"] == "development-only" and report["survivors_total"] > 0
    assert all(s["change"] and s["line"] > 0 for s in report["survivors"])
    assert "heldout" not in report
    runs = tool.subprocess_runs
    assert json.loads(inspector.run().content)["cached"] is True
    assert tool.subprocess_runs == runs
    assert len(stages) == 1 and stages[0]["report"]["suite_sha256"] == report["suite_sha256"]
    assert (tool.workspace / "solution.py").read_text() == SOURCE
    accept(registry, "test_above", 9, 1)
    assert json.loads(inspector.run().content)["round"] == 2
    accept(registry, "test_below", 1, -1)
    assert not inspector.run().ok and len(inspector.generation.snapshot()["fault_feedback"]) == 2


def test_reference_failure_and_mutant_timeout_never_claim_detection(registry, monkeypatch):
    accept(registry, "test_inside", 5, 0)
    tool, inspector = registry.get("submit_tests").generation, registry.get("inspect_survivors")
    monkeypatch.setattr(tool, "evaluate", lambda *args, **kw: {"status": "FAIL", "returncode": 1})
    assert not inspector.run().ok and not inspector.generation.snapshot()["fault_feedback"]
    monkeypatch.setattr(tool, "evaluate", lambda *args, **kw:
        {"status": "TIMEOUT", "returncode": None} if "source" in kw else {"status": "PASS", "returncode": 0})
    report = json.loads(inspector.run().content)
    assert report["detected"] == 0 and len(report["uncertain"]) == report["total"]


def test_complete_feedback_response_fits_registry_when_many_faults_survive(registry, monkeypatch):
    accept(registry, "test_inside", 5, 0)
    tool = registry.get("submit_tests").generation
    tool.source = 'def f(x):\n    """' + ('契约' * 1000) + '"""\n    return x+1+1+1+1+1+1+1+1\n'
    monkeypatch.setattr(tool, "evaluate", lambda *args, **kw: {"status": "PASS", "returncode": 0})
    result = registry.execute("inspect_survivors", {})
    report = json.loads(result.content)
    assert result.ok and report["survivors_total"] == 8 and len(report["survivors"]) == 3
    assert json.loads(registry.execute("inspect_survivors", {}).content)["cached"] is True


def test_feedback_and_scoring_faults_are_disjoint_for_frozen_dataset():
    from eval.dataset import load_dataset
    for instance in load_dataset():
        feedback, heldout = independent_pools(instance.solution_source)
        assert not {fingerprint(m) for m in feedback} & {fingerprint(m) for m in heldout}
        assert all(m.operator in FEEDBACK_OPERATORS for m in feedback)
        assert all(m.operator in HELDOUT_OPERATORS for m in heldout)


def test_engine_move_preserves_exact_historical_fault_candidates():
    from code_agent.faults import generate_mutants
    from eval.dataset import load_dataset
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("frozen_mutation", root / "results/testgen_pilot_v2/source/eval/mutation.py")
    frozen = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = frozen
    try:
        spec.loader.exec_module(frozen)
        for instance in load_dataset():
            before = frozen.generate_mutants(instance.solution_source)
            after = generate_mutants(instance.solution_source)
            assert [(m.to_dict(), m.source) for m in before] == [(m.to_dict(), m.source) for m in after]
    finally:
        sys.modules.pop(spec.name, None)


def test_a5_runner_scores_heldout_faults_and_baseline_can_match_pool(tmp_path):
    from code_agent.agent import Agent
    from eval.dataset import Instance
    from eval.runner import default_variant, run_single
    from tests.helpers import ScriptedLLM, text_response, tool_response
    instance = Instance("DEMO/1", SOURCE[:SOURCE.index("    if")], SOURCE[SOURCE.index("    if"):], "classify", "")
    def factory(variant, settings, registry, workspace):
        llm = ScriptedLLM([tool_response(("submit_tests", {"cases": [candidate("test_inside", 5, 0)]})), text_response("done")])
        return Agent(llm=llm, tools=registry, system_prompt=variant.resolve_system_prompt(),
                     finish_turn=registry.get("submit_tests").generation.finish_turn)
    for name in ("A4", "A5"):
        outcome = run_single(instance, default_variant(name), run_root=tmp_path,
                             settings_factory=lambda w: Settings(workspace=w), agent_factory=factory,
                             defer_measurement=True, mutation_operators=HELDOUT_OPERATORS,
                             measurement_timeouts=(3, 10, 3))
        assert outcome.final["all_pass"] is True
        assert set(outcome.final["mutant_operators"]) <= set(HELDOUT_OPERATORS)
        assert outcome.final["mutants_total"] == 2 and outcome.final["mutation_score"] == 0
        assert outcome.environment["mutation_operators"] == list(HELDOUT_OPERATORS)


def test_cli_fault_flag_assembles_shared_private_tools(registry):
    from code_agent import cli
    args = cli.build_parser().parse_args(["--fault-feedback", "--mock", "--no-session"])
    agent, _, _ = cli.build_agent(args, registry.get("submit_tests").settings, lambda _: None, session_enabled=False)
    assert agent.tools.get("inspect_survivors").generation is agent.tools.get("submit_tests").generation
    assert "inspect_survivors" in agent.state.system_prompt
    args = cli.build_parser().parse_args(["--tools", "inspect_survivors", "--mock"])
    from code_agent.errors import ConfigError
    with pytest.raises(ConfigError, match="requires submit_tests"):
        cli.build_agent(args, registry.get("submit_tests").settings, lambda _: None, session_enabled=False)


def test_a5_batch_uses_matching_baseline_pool_and_refuses_old_scores(tmp_path, monkeypatch):
    from eval import runner
    from eval.dataset import Instance
    from eval.runner import RunOutcome, default_variant, run_batch, write_result
    instance = Instance("DEMO/1", "", SOURCE, "classify", "")
    calls = []
    def fake_run(instance, variant, **kw):
        calls.append((variant.name, kw["mutation_operators"]))
        return RunOutcome(instance_id=instance.instance_id, variant=variant.name,
                          environment={"mutation_operators": list(kw["mutation_operators"])})
    monkeypatch.setattr(runner, "run_single", fake_run)
    kwargs = dict(instances=[instance], variants=[default_variant("A0"), default_variant("A5")],
                  output_dir=tmp_path, settings_factory=lambda w: Settings(workspace=w))
    run_batch(**kwargs)
    assert {name for name, _ in calls} == {"A0", "A5"}
    assert all(pool == HELDOUT_OPERATORS for _, pool in calls)
    calls.clear()
    run_batch(**kwargs)
    assert not calls
    write_result(tmp_path, RunOutcome(instance_id="DEMO/old", variant="A0"))
    with pytest.raises(ValueError, match="new output directory"):
        run_batch(**kwargs)
    assert not calls


def test_report_refuses_mixed_scoring_families(tmp_path):
    from eval.report import write_report
    from eval.runner import RunOutcome
    baseline = RunOutcome(instance_id="D/1", variant="A0")
    a5 = RunOutcome(instance_id="D/1", variant="A5", environment={"mutation_operators": list(HELDOUT_OPERATORS)})
    with pytest.raises(ValueError, match="different scoring pools"):
        write_report(tmp_path, [baseline, a5])
