"""Independent offline replay of the formal jobs, frozen sources and scoring pools."""
import argparse
import hashlib
import json
import math
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from eval.dataset import load_dataset
from eval.metrics import run_mutation_tests, run_pytest_on
from eval.mutation import generate_mutants


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=ROOT / "results/testgen_formal_v1")
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(); output = args.results.resolve()
    manifest = json.loads((output / "manifest.json").read_text())
    for name, expected in manifest["files_sha256"].items():
        actual = hashlib.sha256((output / "source" / name).read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit("Frozen input mismatch: " + name)
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise SystemExit("Live engine/config differs from frozen run: " + name)
    instances = {x.instance_id: x for x in load_dataset(output / "source" / manifest["dataset"])}
    expected = {output / v / (iid.replace("/", "__")+".json") for v, iid in manifest["jobs"]}
    if set(output.glob("A[04]/*.json")) != expected or len(expected) != 40:
        raise SystemExit("Incomplete or unexpected formal job membership")
    timeouts = manifest["measurement_seconds"]
    def replay(path):
        d = json.loads(path.read_text()); f = d.get("final", {})
        suite_path = path.with_suffix(".tests.py")
        instance = instances[d["instance_id"]]
        row = {"record": str(path.relative_to(output)), "variant": d["variant"], "instance_id": d["instance_id"],
               "record_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        expected_mutants = len(generate_mutants(instance.solution_source))
        if not d["tests_chars"]:
            if suite_path.exists() and suite_path.read_text():
                raise ValueError("Unexpected saved suite: " + str(path))
            row.update({"suite_present": False, "expected_mutants": expected_mutants, "reference_matches": not f.get("all_pass", False),
                        "scoring_matches": not f.get("mutants_total", 0), "mutation_errors": 0})
            return row
        suite = suite_path.read_text()
        if len(suite) != d["tests_chars"]:
            raise ValueError("Saved suite length mismatch: " + str(path))
        row["suite_sha256"] = hashlib.sha256(suite_path.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory(prefix="formal-replay-") as tmp:
            w = Path(tmp)
            (w/"solution.py").write_text(instance.solution_source)
            (w/"test_solution.py").write_text(suite)
            reference = run_pytest_on("test_solution.py", w, timeout=timeouts["pytest"])
            mutation = run_mutation_tests(w, instance.solution_source, "test_solution.py", timeout=timeouts["per_mutant"])
            restored = (w/"solution.py").read_text() == instance.solution_source
        row.update({"suite_present": True, "expected_mutants": expected_mutants, "reference_passed": reference.all_pass,
                    "reference_timed_out": reference.process.timed_out, "reference_matches": reference.all_pass == f.get("all_pass", False),
                    "mutants_total": mutation["total"], "mutants_killed": mutation["killed"], "mutation_errors": mutation["errors"],
                    "scoring_matches": mutation["total"] == f.get("mutants_total") and mutation["killed"] == f.get("mutants_killed")
                        and mutation["errors"] == f.get("mutants_errors", 0), "reference_restored": restored})
        return row
    rows = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for row in pool.map(replay, sorted(expected)):
            rows.append(row)
            print(f"[{len(rows)}/40] {row['record']} reference={row['reference_matches']} scoring={row['scoring_matches']}", flush=True)
    receipt = {"scope": "Offline replay only; original model records are preserved, not replaced by replay",
               "frozen_files_verified": len(manifest["files_sha256"]), "jobs_verified": len(rows),
               "reference_matches": sum(r["reference_matches"] for r in rows),
               "scoring_matches": sum(r["scoring_matches"] for r in rows),
               "all_match": all(r["reference_matches"] and r["scoring_matches"] and r.get("reference_restored", True) for r in rows),
               "records": rows}
    # Independently audit the primary aggregation from original records. Replay
    # never overwrites an observed score or substitutes for a failed model run.
    derived = {}
    for variant in ("A0", "A4"):
        records = [json.loads(p.read_text()) for p in sorted(expected) if p.parent.name == variant]
        scores = []
        for d in records:
            f = d.get("final", {})
            total = len(generate_mutants(instances[d["instance_id"]].solution_source))
            if not total:
                continue
            valid = f.get("all_pass", False) and not (d.get("solution_modified", False) or f.get("solution_modified", False))
            measured = f.get("mutants_total") == total and f.get("mutation_score") is not None
            scores.append(f.get("mutants_killed", 0)/total if valid and measured else 0)
        derived[variant] = {"runs": len(records), "valid_mutation": sum(scores)/len(scores) if scores else None,
                            "all_pass_rate": sum(bool(d.get("final", {}).get("all_pass")) for d in records)/len(records),
                            "tokens": sum(d.get("agent", {}).get("input_tokens", 0)+d.get("agent", {}).get("output_tokens", 0) for d in records)/len(records)}
    summary = json.loads((output/"formal_summary.json").read_text())
    summary_matches = all(math.isclose(value, summary["variants"][variant][key], abs_tol=1e-12)
                          for variant, fields in derived.items() for key, value in fields.items())
    receipt.update({"independent_primary_summary": derived, "summary_matches": summary_matches,
                    "all_match": receipt["all_match"] and summary_matches})
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(json.dumps({k:v for k,v in receipt.items() if k!="records"}, ensure_ascii=False), flush=True)
    if not receipt["all_match"]:
        raise SystemExit("Replay differences require inspection; original results unchanged")


if __name__ == "__main__":
    main()
