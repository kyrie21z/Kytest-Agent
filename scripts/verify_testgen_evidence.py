"""Offline independent replay of frozen pilot suites and immutable inputs."""
import argparse
import hashlib
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from eval.dataset import load_dataset
from eval.metrics import run_mutation_tests, run_pytest_on


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", type=Path, default=ROOT / "results/testgen_pilot_v2")
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    pilot = args.pilot.resolve()
    manifest = json.loads((pilot / "manifest.json").read_text())
    for name, expected in manifest["files_sha256"].items():
        if hashlib.sha256((pilot / "source" / name).read_bytes()).hexdigest() != expected:
            raise SystemExit(f"Frozen source changed: {name}")
    instances = {x.instance_id: x for x in load_dataset(pilot / "source/benchmarks/smoke_pool_5.jsonl")}
    expected_paths = {pilot / f"repeat_{r}" / v / (iid.replace("/", "__") + ".json")
                      for r, v, iid in manifest["jobs"]}
    actual_paths = set(pilot.glob("repeat_*/*/*.json"))
    if actual_paths != expected_paths or len(actual_paths) != 30:
        raise SystemExit("Pilot job membership mismatch")
    def replay(path):
        d = json.loads(path.read_text())
        tests_path = path.with_suffix(".tests.py")
        suite = tests_path.read_text()
        if len(suite) != d["tests_chars"]:
            raise ValueError(f"Saved suite length mismatch: {path}")
        with tempfile.TemporaryDirectory(prefix="pilot-replay-") as tmp:
            workspace = Path(tmp)
            source = instances[d["instance_id"]].solution_source
            (workspace / "solution.py").write_text(source)
            (workspace / "test_solution.py").write_text(suite)
            reference = run_pytest_on("test_solution.py", workspace, timeout=3)
            mutation = run_mutation_tests(workspace, source, "test_solution.py", timeout=3)
            restored = (workspace / "solution.py").read_text() == source
        final = d["final"]
        same = (reference.all_pass == final["all_pass"] and mutation["total"] == final["mutants_total"]
                and mutation["killed"] == final["mutants_killed"] and restored and mutation["errors"] == 0)
        return {"record": str(path.relative_to(pilot)), "variant": d["variant"], "matches": same,
                "reference_passed": reference.all_pass, "mutants_total": mutation["total"],
                "mutants_killed": mutation["killed"], "mutation_errors": mutation["errors"],
                "suite_sha256": hashlib.sha256(tests_path.read_bytes()).hexdigest(),
                "record_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "tokens": d["agent"]["input_tokens"] + d["agent"]["output_tokens"],
                "generation_seconds": d["agent"]["generation_seconds"]}
    with ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(replay, sorted(actual_paths)))
    derived = {}
    for variant in ("A0", "A4"):
        selected = [r for r in rows if r["variant"] == variant]
        derived[variant] = {"runs": len(selected), "all_pass_rate": mean(r["reference_passed"] for r in selected),
                            "valid_mutation": mean(r["mutants_killed"] / r["mutants_total"] if r["reference_passed"] else 0 for r in selected),
                            "tokens": mean(r["tokens"] for r in selected),
                            "generation_seconds": mean(r["generation_seconds"] for r in selected)}
    summary = json.loads((pilot / "pilot_summary.json").read_text())
    same_summary = derived == summary["variants"]
    receipt = {"scope": "Offline replay, no model requests; reference and all scoring faults per saved suite",
               "frozen_files_verified": len(manifest["files_sha256"]), "runs_verified": len(rows),
               "all_match": all(r["matches"] for r in rows) and same_summary,
               "derived_summary_matches": same_summary, "variants": derived, "records": rows}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in receipt.items() if k != "records"}, ensure_ascii=False, indent=2))
    if not receipt["all_match"]:
        raise SystemExit("Pilot replay mismatch")


if __name__ == "__main__":
    main()
