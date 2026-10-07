"""Replay controlled-demo artifacts using the evaluator, after generation is finished."""
import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from code_agent.fault_feedback import HELDOUT_OPERATORS, fingerprint, independent_pools
from eval.metrics import MEASUREMENT_VERSION, run_mutation_tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    saved = json.loads((args.demo / "receipt.json").read_text())
    source = (args.demo / "agent_workspace/solution.py").read_text()
    development, heldout = independent_pools(source)
    assert not {fingerprint(m) for m in development} & {fingerprint(m) for m in heldout}
    stages = {}
    for stage in ("before", "after"):
        suite = (args.demo / (stage + ".tests.py")).read_bytes()
        with tempfile.TemporaryDirectory(prefix="quality-v2-independent-") as temp:
            workspace = Path(temp)
            (workspace / "solution.py").write_text(source)
            (workspace / "test_solution.py").write_bytes(suite)
            result = run_mutation_tests(workspace, source, "test_solution.py", operators=HELDOUT_OPERATORS, timeout=3)
            assert (workspace / "solution.py").read_text() == source
        assert result["baseline"]["all_pass"]
        assert result["total"] == saved["measurements"][stage]["total"]
        assert result["killed"] == saved["measurements"][stage]["detected"]
        stages[stage] = {"suite_sha256": hashlib.sha256(suite).hexdigest(), **result}
    assert stages["before"]["killed"] == 0 and stages["after"]["killed"] == 2
    reports = saved["development_feedback"]
    assert len(reports) == 2 and reports[1]["newly_detected_faults"]
    assert all(a["current_suite_checked"] for a in saved["quality_actions"])
    receipt = {"scope": "Independent controlled-artifact replay, no model requests or population quality claim",
               "measurement_version": MEASUREMENT_VERSION, "scoring_after_generation": True,
               "demo_receipt_sha256": hashlib.sha256((args.demo / "receipt.json").read_bytes()).hexdigest(),
               "operator_families": list(HELDOUT_OPERATORS), "pools_disjoint": True,
               "development_detected_before": reports[0]["detected"], "development_detected_after": reports[1]["detected"],
               "newly_detected_fault_ids": [m["mutant_id"] for m in reports[1]["newly_detected_faults"]],
               "all_stages_match": True, "stages": stages}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if k != "stages"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
