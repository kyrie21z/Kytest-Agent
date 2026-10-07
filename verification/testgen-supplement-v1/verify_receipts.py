"""Verify saved evidence without model requests or replacing original scores."""
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from eval.dataset import load_dataset
from eval.mutation import generate_mutants


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def verify():
    evidence = Path(__file__).resolve().parent
    output = ROOT / "results/testgen_supplement_v1"
    manifest = read(output / "manifest.json")
    protected = read(evidence / "protected-files.json")
    for name, expected in protected["files_sha256"].items():
        assert sha(ROOT / name) == expected, name
    for name, expected in manifest["files_sha256"].items():
        assert sha(ROOT / name) == sha(output / "source" / name) == expected, name
    baseline = ROOT / manifest["baseline_directory"]
    for name, expected in manifest["baseline_sha256"].items():
        assert sha(baseline / name) == expected, name
    instances = load_dataset(output / "source" / manifest["dataset"])
    totals = {x.instance_id: len(generate_mutants(x.solution_source)) for x in instances}
    assert all(totals.values())
    replay = read(evidence / "replay.json")
    saved_effective = read(evidence / "effective-replay.json")
    expected_jobs = {(v, iid.replace("/", "__") + ".json") for v, iid in manifest["jobs"]}
    assert {(p.parent.name, p.name) for p in output.glob("A*/*.json")} == expected_jobs
    assert len(replay["records"]) == len(expected_jobs) == 60
    assert {tuple(Path(r["record"]).parts) for r in replay["records"]} == expected_jobs
    effective = []
    for row in replay["records"]:
        path = output / row["record"]
        record = read(path)
        assert sha(path) == row["record_sha256"]
        assert sha(path.with_suffix(".tests.py")) == row["suite_sha256"]
        final = record["final"]
        actions = record["agent"].get("system_actions", [])
        modified = record.get("solution_modified") or final.get("solution_modified") or any(a.get("solution_restored") for a in actions)
        total = totals[record["instance_id"]]
        original = final["mutants_killed"] / total if final["all_pass"] and not modified else 0
        reproduced = row["mutants_killed"] / total if row["reference_passed"] and not modified else 0
        assert row["reference_restored"] and row["mutants_total"] == final["mutants_total"] == total
        effective.append({"record": row["record"], "original_effective_score": original,
                          "replayed_effective_score": reproduced, "match": original == reproduced})
    assert effective == saved_effective["per_run"]
    assert sum(r["match"] for r in effective) == saved_effective["effective_scores_match"] == 60
    assert replay["reference_matches"] == sum(r["reference_matches"] for r in replay["records"]) == 60
    assert replay["scoring_matches"] == sum(r["scoring_matches"] for r in replay["records"]) == 59
    assert replay["summary_matches"] and not replay["all_match"]
    summary = read(output / "supplement_summary.json")
    assert summary["complete"] and summary["completed_jobs"] == 100
    for v in ("A0", "A1", "A2", "A3", "A4"):
        folder = baseline if v in ("A0", "A4") else output
        records = [read(p) for p in sorted((folder / v).glob("*.json"))]
        assert len(records) == 20
        scores = []
        for d in records:
            f = d["final"]
            actions = d["agent"].get("system_actions", [])
            modified = d.get("solution_modified") or f.get("solution_modified") or any(a.get("solution_restored") for a in actions)
            scores.append(f["mutants_killed"] / totals[d["instance_id"]] if f["all_pass"] and not modified else 0)
        derived = {"runs": 20, "valid_mutation": sum(scores) / 20,
                   "all_pass_rate": sum(d["final"]["all_pass"] for d in records) / 20,
                   "tokens": sum(d["agent"]["input_tokens"] + d["agent"]["output_tokens"] for d in records) / 20,
                   "system_pytest_runs": sum(len(d["agent"].get("system_actions", [])) for d in records)}
        for k, value in derived.items():
            assert math.isclose(value, summary["variants"][v][k], abs_tol=1e-12)
            assert math.isclose(value, replay["independent_primary_summary"][v][k], abs_tol=1e-12)
    diagnostics = read(evidence / "diagnostics.json")
    for row in diagnostics["literal_input_audit"]:
        folder = baseline if row["variant"] in ("A0", "A4") else output
        name = row["instance_id"].replace("/", "__")
        assert sha(folder / row["variant"] / (name + ".tests.py")) == row["suite_sha256"]
        stored = next(r for r in summary["per_run"] if (r["variant"], r["instance_id"]) == (row["variant"], row["instance_id"]))
        assert sha(folder / row["variant"] / (name + ".json")) == stored["record_sha256"]
    assert len(diagnostics["literal_input_audit"]) == 100
    for name, expected in diagnostics["tool_sha256"].items():
        assert sha(ROOT / name) == expected, name
    control = read(evidence / "prime-fib-variability.json")
    assert sha(ROOT / "scripts/audit_prime_fib_variability.py") == control["tool_sha256"]
    assert control["different_mutants_between_seeds"] == ["M18"]
    assert [(t["seed"], t["mutants_killed"], t["mutants_errors"]) for t in control["seed_controls"]] == [(0, 13, 7), (1, 12, 8)]
    assert "37 passed" in (evidence / "admission-tests.log").read_text()
    assert "268 passed, 4 skipped" in (evidence / "pytest.log").read_text()
    return {"status": "ACCEPTED_WITH_DISCLOSED_RAW_VARIABILITY", "new_model_runs": 60, "reused_model_runs": 40,
            "protected_files_verified": len(protected["files_sha256"]), "frozen_files_verified": len(manifest["files_sha256"]),
            "baseline_files_verified": len(manifest["baseline_sha256"]), "original_records_and_suites_verified": 200,
            "admission_tests_passed": 37, "project_tests_passed": 268, "windows_tests_skipped": 4,
            "reference_matches": 60, "effective_primary_matches": 60, "raw_mutation_matches": 59,
            "all_raw_counts_match": False, "independent_five_variant_summary_matches": True,
            "raw_mismatch": {"record": "A1/HumanEval__39.json", "original_killed_timeouts": [12, 8],
                             "replay_killed_timeouts": [13, 7], "effective_primary_score": 0,
                             "seed_0_killed_timeouts": [13, 7], "seed_1_killed_timeouts": [12, 8], "different_mutant": "M18"},
            "all_three_holm_p_above_005": all(c["holm_p"] > .05 for c in summary["comparisons"].values()),
            "a3_coverage_incomplete_instances": summary["variants"]["A3"]["coverage_incomplete_instances"],
            "solution_modifications": sum(v["solution_modifications"] for v in summary["variants"].values()),
            "observed_network_attempts": sum(v["network_attempts"] for v in summary["variants"].values()),
            "receipt_sha256": {p.name: sha(p) for p in sorted(evidence.glob("*")) if p.is_file() and p.name != "acceptance.json"},
            "claim_boundary": "Two sampling batches, one generation per condition and case, previously evaluated cases and possible equivalent mutants; no significance does not establish equivalence. Seed controls are post-hoc diagnostics and never replace primary data."}


if __name__ == "__main__":
    result = verify()
    previous = Path(__file__).resolve().with_name("acceptance.json")
    if previous.exists():
        assert result == read(previous), "Acceptance receipt changed"
    print(json.dumps(result, ensure_ascii=False, indent=2))
