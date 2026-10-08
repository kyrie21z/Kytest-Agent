"""Post-hoc reference failures and grid-domain sensitivity; primary data stay intact."""
import ast
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from code_agent.proc import run_capture
from code_agent.testgen import check_literal_inputs, explicit_constraints
from eval.dataset import load_dataset
from eval.metrics import child_env, run_mutation_tests, run_pytest_on
from scripts.audit_formal_minpath import audit


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    output = ROOT / "results/testgen_supplement_v1"
    summary = json.loads((output / "supplement_summary.json").read_text())
    if not summary["complete"]:
        raise SystemExit("Finish all supplementary jobs before post-hoc replay")
    instances = {x.instance_id:x for x in load_dataset(output / "source/benchmarks/humaneval_plus_v2_20.jsonl")}
    baseline = ROOT / json.loads((output / "manifest.json").read_text())["baseline_directory"]
    before = {}
    failures, literal_audit, grid_sensitivity = [], [], {}
    for variant in ("A0", "A1", "A2", "A3", "A4"):
        folder = baseline if variant in ("A0", "A4") else output
        for path in sorted((folder / variant).glob("*.json")):
            d=json.loads(path.read_text()); suite_path=path.with_suffix(".tests.py")
            before[str(path.relative_to(ROOT))]=sha(path)
            if not suite_path.exists():
                continue
            before[str(suite_path.relative_to(ROOT))]=sha(suite_path)
            instance=instances[d["instance_id"]]; suite=suite_path.read_text()
            row={"variant":variant,"instance_id":d["instance_id"],"suite_sha256":sha(suite_path)}
            try:
                row.update(check_literal_inputs(ast.parse(suite),explicit_constraints(instance.solution_source)))
            except SyntaxError as error:
                row["syntax_error"]=str(error)
            literal_audit.append(row)
            if variant in ("A1", "A2", "A3") and not d.get("final",{}).get("all_pass"):
                with tempfile.TemporaryDirectory(prefix="supplement-failure-") as tmp:
                    w=Path(tmp); (w/"solution.py").write_text(instance.solution_source); (w/"test_solution.py").write_text(suite)
                    result=run_capture([sys.executable,"-m","pytest","test_solution.py","-q","--tb=short","--no-header","-p","no:cacheprovider"],
                                       cwd=w,timeout=10,env=child_env(w),execution_mode="sandbox")
                failures.append({**row,"original_status":d["status"],"original_reference_timed_out":d.get("final",{}).get("pytest_timed_out"),
                                 "replay_timed_out":result.timed_out,"replay_returncode":result.exit_code,
                                 "output":(result.stdout+result.stderr+(result.error or ""))[-6000:]})
                print(f"Failure replay {variant}/{d['instance_id']}: timeout={result.timed_out}, exit={result.exit_code}",flush=True)
    instance=instances["HumanEval/129"]
    for variant in ("A1", "A2", "A3"):
        path=output/variant/"HumanEval__129.tests.py"
        tree, findings, checked, unknown=audit(path.read_text())
        bad={r["test"] for r in findings}
        for node in ast.walk(tree):
            if isinstance(node,(ast.Module,ast.ClassDef)):
                node.body=[n for n in node.body if not isinstance(n,ast.FunctionDef) or n.name not in bad]
        filtered=ast.unparse(tree)+"\n"
        with tempfile.TemporaryDirectory(prefix="supplement-grid-") as tmp:
            w=Path(tmp); (w/"solution.py").write_text(instance.solution_source); (w/"test_solution.py").write_text(filtered)
            reference=run_pytest_on("test_solution.py",w,timeout=10)
            mutation=run_mutation_tests(w,instance.solution_source,"test_solution.py",timeout=5)
        grid_sensitivity[variant]={"suite_sha256":sha(path),"literal_calls_checked":checked,"calls_unknown":unknown,
            "invalid_inputs":findings,"removed_test_functions":sorted(bad),"filtered_suite_sha256":hashlib.sha256(filtered.encode()).hexdigest(),
            "filtered_reference_passed":reference.all_pass,"filtered_reference_summary":reference.summary_line,
            "filtered_mutants_total":mutation["total"],"filtered_mutants_killed":mutation["killed"],
            "filtered_mutation_score":mutation["score"],"filtered_mutants_errors":mutation["errors"]}
        print(f"Filtered grid audit {variant}: reference={reference.all_pass}, killed={mutation['killed']}/{mutation['total']}",flush=True)
    assert all(sha(ROOT/name)==expected for name,expected in before.items())
    receipt={"scope":"Post-hoc diagnostic only; raw generated suites and preregistered primary scores are not replaced",
             "tool_sha256":{str(p.relative_to(ROOT)):sha(p) for p in (Path(__file__),ROOT/"scripts/audit_formal_minpath.py")},
             "original_records_and_suites_unchanged":True,"files_verified":len(before),
             "limitation":"Literal checker recognizes only selected explicit constraints. Grid sensitivity removes whole functions containing invalid literal grids, may remove valid co-cases, and does not certify k, unknown expressions or all oracles.",
             "reference_failures":failures,"literal_input_audit":literal_audit,"minpath_grid_sensitivity":grid_sensitivity}
    destination=ROOT/"verification/testgen-supplement-v1/diagnostics.json"
    destination.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")


if __name__=="__main__":
    main()
