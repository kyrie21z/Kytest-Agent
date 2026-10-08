"""Acceptance against invalid-score, weak-oracle and bypassed-feedback counterexamples."""
import json
from pathlib import Path

import pytest

from code_agent.agent import Agent
from code_agent.config import Settings
from code_agent.testgen import TestGeneration as Generation
from code_agent.tools.factories import build_registry
from eval.dataset import Instance
from eval.metrics import MEASUREMENT_VERSION, collect_metrics, run_mutation_tests
from code_agent.proc import ProcResult
from code_agent.pytest_result import parse_pytest_result
from eval.mutation import Mutant
from tests.helpers import ScriptedLLM, text_response, tool_response

SOURCE = 'def count(n):\n    """For a positive integer n, return n plus one."""\n    return n + 1\n'
QUOTE = "For a positive integer n, return n plus one."


def proposal(code, name="test_count", quote=QUOTE):
    return {"name": name, "code": code, "contract_quote": quote,
            "input_domain": "positive integer n", "oracle_reason": "Independent arithmetic",
            "fault_hypothesis": "incorrect offset"}


@pytest.fixture
def submitter(tmp_path):
    (tmp_path / "solution.py").write_text(SOURCE)
    return Generation(Settings(workspace=tmp_path))


def submit(tool, body, prefix="from solution import count\n", quote=QUOTE):
    code = prefix + "def test_count():\n" + body
    return json.loads(tool.submit(cases=[proposal(code, quote=quote)]).content)["results"][0]


def test_invalid_reference_has_zero_quality_without_executing_mutants(tmp_path):
    instance = Instance("D/1", "", SOURCE, "count", "")
    (tmp_path / "solution.py").write_text(instance.solution_source)
    (tmp_path / "test_solution.py").write_text("from solution import count\ndef test_wrong():\n    assert count(2)==999\n")
    result = collect_metrics(instance, tmp_path, 0, include_mutation=True, max_mutants=1)
    assert not result.all_pass and result.mutation_score == 0
    assert result.mutants_total == 1 and result.mutants_killed == 0
    assert result.mutation_status == "reference_invalid"
    assert result.mutant_results[0]["status"] == "NOT_RUN"
    assert result.to_dict()["measurement_version"] == MEASUREMENT_VERSION


def test_no_suite_retains_reference_fault_denominator(tmp_path):
    instance = Instance("D/1", "", SOURCE, "count", "")
    (tmp_path / "solution.py").write_text(instance.solution_source)
    result = collect_metrics(instance, tmp_path, 0, include_mutation=True)
    assert not result.has_tests and result.mutants_total > 0
    assert result.mutation_score == 0 and result.mutation_status == "no_tests"


def test_zero_mutant_reference_is_the_only_structural_exclusion(tmp_path):
    instance = Instance("D/0", "", 'def identity(x):\n    return x\n', "identity", "")
    (tmp_path / "solution.py").write_text(instance.solution_source)
    result = collect_metrics(instance, tmp_path, 0, include_mutation=True)
    assert result.mutants_total == 0 and result.mutation_score is None
    assert result.mutation_status == "no_mutants"


def test_generated_test_cannot_modify_reference_and_claim_quality(tmp_path):
    instance = Instance("D/1", "", SOURCE, "count", "")
    (tmp_path / "solution.py").write_text(instance.solution_source)
    (tmp_path / "test_solution.py").write_text("from solution import count\ndef test_tamper():\n    open('solution.py','w').write('def count(n): return 999')\n    assert count(2)==3\n")
    result = collect_metrics(instance, tmp_path, 0, include_mutation=True, max_mutants=1)
    assert result.all_pass and result.solution_modified
    assert result.mutation_score == 0 and result.mutation_status == "solution_modified"
    assert (tmp_path / "solution.py").read_text() == instance.solution_source


def test_v2_report_retains_constructor_failures_and_refuses_mixed_versions(tmp_path):
    from eval.report import summarize_variant, write_report
    from eval.runner import RunOutcome
    measured = RunOutcome(instance_id="D/1", variant="A0", environment={"measurement_version": MEASUREMENT_VERSION},
        final={"measurement_version": MEASUREMENT_VERSION, "all_pass": True, "mutants_total": 2,
               "mutation_score": .5, "mutation_upper_bound": 1, "mutation_completion_rate": .5})
    failed = RunOutcome(instance_id="D/2", variant="A0", status="eval_error",
        environment={"measurement_version": MEASUREMENT_VERSION, "reference_mutants_total": 2})
    summary = summarize_variant("A0", [measured, failed])
    assert summary.mutation_n == 2 and summary.mutation_mean == .25
    assert summary.mutation_completion_mean == .25 and summary.mutation_upper_mean == .5
    write_report(tmp_path, [measured, failed])
    with pytest.raises(ValueError, match="measurement versions"):
        write_report(tmp_path, [measured, RunOutcome(instance_id="old", variant="A1")])


def test_mutant_states_require_differential_failure_evidence(tmp_path, monkeypatch):
    from eval import metrics
    (tmp_path / "solution.py").write_text(SOURCE)
    (tmp_path / "test_solution.py").write_text("from solution import count\ndef test_count():\n    assert count(2)==3\n")
    mutants = [Mutant("K", "AOR", 3, 0, "target exception", SOURCE.replace("n + 1", "1 / 0")),
               Mutant("I", "AOR", 3, 0, "invalid syntax", "def count(:\n")]
    monkeypatch.setattr(metrics, "generate_mutants", lambda *a, **kw: mutants)
    result = run_mutation_tests(tmp_path, SOURCE, "test_solution.py", timeout=3)
    assert [r["status"] for r in result["mutant_results"]] == ["KILLED", "INVALID_MUTANT"]
    assert result["score"] == .5 and result["upper_bound"] == 1 and result["completion_rate"] == .5
    assert result["mutant_results"][0]["failure_nodes"] == ["test_solution.py::test_count"]
    assert (tmp_path / "solution.py").read_text() == SOURCE


def test_collection_failure_without_target_evidence_is_unknown(tmp_path, monkeypatch):
    from eval import metrics
    (tmp_path / "solution.py").write_text(SOURCE)
    monkeypatch.setattr(metrics, "generate_mutants", lambda *a, **kw: [Mutant("M", "AOR", 3, 0, "offset", SOURCE.replace("+ 1", "- 1"))])
    monkeypatch.setattr(metrics, "run_pytest_on", lambda *a, **kw: parse_pytest_result(ProcResult(exit_code=2, stdout="1 error in 0.01s")))
    reference = parse_pytest_result(ProcResult(exit_code=0, stdout="PASSED test_solution.py::test_count\n1 passed in 0.01s"))
    result = run_mutation_tests(tmp_path, SOURCE, "test_solution.py", baseline=reference)
    assert result["mutant_results"][0]["status"] == "INFRA_ERROR"
    assert result["killed"] == 0 and result["total"] == 1 and result["upper_bound"] == 1


@pytest.mark.parametrize("body", [
    "    assert count(2)==count(2)\n",
    "    count(2)\n    assert 1==1\n",
    "    result=count(2)\n    assert result==result\n",
    "    assert count(2)==count(1)+1\n",
    "    n=0\n    assert count(n)==1\n",
    "    count=lambda n: 3\n    assert count(2)==3\n",
    "    for n in range(0,3):\n        assert count(n)==n+1\n",
    "    for n in range(1,1000000001):\n        assert count(n)==n+1\n",
])
def test_bad_candidates_rejected_before_execution(submitter, body):
    row = submit(submitter, body)
    assert row["status"] == "REJECTED" and submitter.subprocess_runs == 0


def test_dynamic_domain_violation_cannot_be_hidden_by_catching_guard(submitter):
    row = submit(submitter, "    try:\n        count(int('0'))\n    except ValueError:\n        pass\n    assert count(2)==3\n")
    assert row["status"] == "CONTRACT_VIOLATION" and not submitter.accepted
    assert row["runtime_contract_checks"]["violations"]


@pytest.mark.parametrize("body", [
    "    r=count(2)\n    assert r-r==0\n",
    "    r=count(2)\n    delta=r-r\n    assert delta==0\n",
    "    r=count(2)\n    assert (r-r)+7==7\n",
    "    r=count(2)\n    assert r*0==0\n",
    "    r=count(2)\n    zero=0\n    scaled=zero*r\n    assert scaled==0\n",
])
def test_canceled_result_cannot_supply_an_output_anchor(submitter, body):
    row = submit(submitter, body)
    assert row["status"] == "REJECTED" and submitter.subprocess_runs == 0
    assert "independent output anchor" in row["diagnostic"]


def test_independent_oracle_survives_cancellation_filter_and_detects_fault(submitter):
    row = submit(submitter, "    r=count(2)\n    assert r==3\n    assert r-r==0\n")
    assert row["status"] == "ACCEPTED"
    measured = run_mutation_tests(submitter.workspace, SOURCE, "test_solution.py", max_mutants=1, timeout=3)
    assert measured["killed"] == measured["total"] == 1
    assert (submitter.workspace / "solution.py").read_text() == SOURCE


def test_dynamic_loop_is_bounded_by_actual_target_calls(submitter):
    row = submit(submitter, "    for _ in range(int('1000')):\n        assert count(2)==3\n")
    assert row["status"] == "RESOURCE_LIMIT" and not submitter.accepted


def test_local_import_and_outer_quotes_work_together(submitter):
    row = submit(submitter, "    from solution import count\n    assert count(2)==3\n", prefix="", quote='"' + QUOTE + '"')
    assert row["status"] == "ACCEPTED"
    assert row["runtime_contract_checks"]["total_calls"] == 1


def test_valid_alias_and_independent_metamorphic_anchor(submitter):
    row = submit(submitter, "    f=count\n    assert f(2)==3\n    assert f(3)==f(2)+1\n")
    assert row["status"] == "ACCEPTED"


def test_annotated_and_updated_constant_cannot_hide_invalid_input(submitter):
    row = submit(submitter, "    n: int=1\n    n-=1\n    assert count(n)==1\n")
    assert row["status"] == "REJECTED" and submitter.subprocess_runs == 0


def test_comprehension_local_does_not_shadow_enclosing_import(submitter):
    row = submit(submitter, "    ignored=[count for count in [1,2]]\n    assert count(2)==3\n")
    assert row["status"] == "ACCEPTED"


def test_function_local_alias_does_not_get_renamed_to_global_math_alias(submitter):
    row = submit(submitter, "    from solution import count as f\n    assert f(2)==3\n", prefix="from math import sqrt as f\n")
    assert row["status"] == "ACCEPTED"
    assert submitter.evaluate(submitter.suite_source(), 3)["status"] == "PASS"


def test_documented_in_place_side_effect_can_supply_assertion_dependency(tmp_path):
    (tmp_path / "solution.py").write_text('def append_one(items):\n    """Append one to the input list in place."""\n    items.append(1)\n')
    tool = Generation(Settings(workspace=tmp_path))
    code = 'from solution import append_one\ndef test_count():\n    items=[]\n    append_one(items)\n    assert items==[1]\n'
    result = json.loads(tool.submit(cases=[proposal(code, quote="Append one to the input list in place.")]).content)
    assert result["results"][0]["status"] == "ACCEPTED"


def test_coverage_error_is_unavailable_not_full(tmp_path, monkeypatch):
    from eval import hooks
    from types import SimpleNamespace
    (tmp_path / "solution.py").write_text(SOURCE)
    (tmp_path / "test_solution.py").write_text("from solution import count\ndef test_count():\n    assert count(2)==3\n")
    monkeypatch.setattr(hooks, "_coverage_missing_lines", lambda w: {"error": "controlled unavailable dependency"})
    messages = []
    agent = SimpleNamespace(state=SimpleNamespace(add_user=messages.append))
    hook = hooks.make_guided_hook(tmp_path, SOURCE, max_coverage_rounds=2)
    decision = hook(agent, SimpleNamespace(turn=1))
    assert decision.end and decision.reason == "coverage_unavailable"
    assert hook.state.actions[0]["coverage"]["error"] and "unavailable" in messages[0]


def test_a5_cannot_naturally_finish_without_development_check(tmp_path):
    from scripts.demo_fault_feedback import SOURCE as interval, candidate
    (tmp_path / "solution.py").write_text(interval)
    registry = build_registry(Settings(workspace=tmp_path), ("submit_tests", "inspect_survivors"))
    llm = ScriptedLLM([tool_response(("submit_tests", {"cases": [candidate("test_inside", 5, 0)]})), text_response("done")])
    tool = registry.get("submit_tests").generation
    agent = Agent(llm=llm, tools=registry, system_prompt="generate", max_turns=5, finish_turn=tool.finish_turn)
    agent.state.add_user("generate tests")
    result = agent.run()
    assert result.status == "stopped" and result.error == "development_no_progress"
    assert len(registry.get("inspect_survivors").generation.snapshot()["fault_feedback"]) == 1
    assert len(llm.requests) == 3 and len(tool.accepted) == 1
    assert tool.quality_actions[0]["decision"] == "development_feedback"


def test_automatic_feedback_records_actual_increment_and_preserves_suite(tmp_path):
    from scripts.demo_fault_feedback import SOURCE as interval, candidate
    (tmp_path / "solution.py").write_text(interval)
    registry = build_registry(Settings(workspace=tmp_path), ("submit_tests", "inspect_survivors"))
    tool = registry.get("submit_tests").generation
    llm = ScriptedLLM([tool_response(("submit_tests", {"cases": [candidate("test_inside", 5, 0)]})),
                      tool_response(("submit_tests", {"cases": [candidate("test_below", 1, -1), candidate("test_above", 9, 1), candidate("test_low", 2, 0), candidate("test_high", 8, 0)]}))])
    agent = Agent(llm=llm, tools=registry, system_prompt="generate", max_turns=4, finish_turn=tool.finish_turn)
    agent.state.add_user("generate")
    result = agent.run()
    reports = registry.get("inspect_survivors").generation.snapshot()["fault_feedback"]
    assert result.status == "stopped" and len(reports) == 2 and len(tool.accepted) == 5
    assert reports[1]["newly_detected_faults"] and not reports[1]["lost_detections"]
    assert reports[1]["detected"] > reports[0]["detected"]
    assert tool.evaluate(tool.suite_source(), 5)["status"] == "PASS"
    assert (tmp_path / "solution.py").read_text() == interval
