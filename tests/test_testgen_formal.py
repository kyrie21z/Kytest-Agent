"""Formal admission and ITT reporting; no live model calls."""
import json
from pathlib import Path

import pytest

from scripts.run_testgen_formal import summarize


def fixture_output(tmp_path, count=20):
    source = Path(__file__).resolve().parents[1] / "benchmarks/humaneval_plus_v2_20.jsonl"
    target = tmp_path / "source/benchmarks" / source.name
    target.parent.mkdir(parents=True)
    target.write_bytes(source.read_bytes())
    ids = [json.loads(x)["task_id"] if "task_id" in json.loads(x) else json.loads(x)["instance_id"] for x in source.read_text().splitlines()][:count]
    (tmp_path / "manifest.json").write_text(json.dumps({"dataset": "benchmarks/"+source.name,
        "jobs": [(v, iid) for v in ("A0", "A4") for iid in ids]}))
    return ids


def record(output, variant, iid, final=None, **extra):
    folder = output / variant
    folder.mkdir(exist_ok=True)
    (folder / (iid.replace("/", "__")+".json")).write_text(json.dumps({
        "variant": variant, "instance_id": iid, "status": "no_tests",
        "final": final or {}, "agent": {}, **extra}))


def test_formal_missing_suite_and_measurement_failures_keep_all_pairs(tmp_path):
    ids = fixture_output(tmp_path)
    for v in ("A0", "A4"):
        for iid in ids:
            record(tmp_path, v, iid)
    s = summarize(tmp_path)
    assert s["complete"] and s["completed_jobs"] == 40
    assert s["variants"]["A4"]["valid_mutation"] == 0
    assert s["comparison"]["n"] == 20 and s["comparison"]["wilcoxon_p"] == 1
    assert s["comparison"]["all_pairs_tied"]


def test_formal_sut_modification_cannot_inflate_valid_score(tmp_path):
    from eval.dataset import load_dataset
    from eval.mutation import generate_mutants
    ids = fixture_output(tmp_path)
    totals = {x.instance_id: len(generate_mutants(x.solution_source)) for x in load_dataset(tmp_path/'source/benchmarks/humaneval_plus_v2_20.jsonl')}
    for v in ("A0", "A4"):
        for iid in ids:
            record(tmp_path, v, iid, {"all_pass": True, "mutation_score": 1,
                "mutants_total": totals[iid], "mutants_killed": totals[iid]}, solution_modified=(v=="A4"))
    s = summarize(tmp_path)
    assert s["variants"]["A0"]["valid_mutation"] == 1
    assert s["variants"]["A4"]["raw_mutation"] == 1
    assert s["variants"]["A4"]["valid_mutation"] == 0
    assert s["comparison"]["worse"] == 20


def test_formal_unexpected_job_is_rejected(tmp_path):
    fixture_output(tmp_path)
    record(tmp_path, "A4", "HumanEval/1")
    with pytest.raises(ValueError, match="Unexpected"):
        summarize(tmp_path)


def test_mutant_timeout_is_persisted_and_does_not_count_as_detection(tmp_path, monkeypatch):
    from eval import metrics
    from eval.dataset import Instance
    from eval.mutation import Mutant
    source = 'def count(n):\n    """Return n plus one."""\n    return n+1\n'
    instance = Instance("D/1", "", source, "count", "")
    (tmp_path/'solution.py').write_text(instance.solution_source)
    (tmp_path/'test_solution.py').write_text('from solution import count\ndef test_two():\n    assert count(2)==3\n')
    monkeypatch.setattr(metrics, "generate_mutants", lambda *a, **kw:
        [Mutant("H", "AOR", 1, 0, "hang", 'def count(n):\n    while True:\n        pass\n')])
    result = metrics.collect_metrics(instance, tmp_path, checkpoint=0, include_mutation=True,
                                     pytest_timeout=3, coverage_timeout=10, mutant_timeout=.5)
    assert result.all_pass
    assert result.to_dict()["mutants_errors"] == 1
    assert result.to_dict()["mutants_killed"] == 0 and result.mutation_score == 0
    assert (tmp_path/'solution.py').read_text() == instance.solution_source
