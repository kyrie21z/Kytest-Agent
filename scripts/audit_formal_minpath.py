"""Post-hoc input-domain sensitivity audit; never changes primary model records."""
import ast
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from eval.dataset import load_dataset
from eval.metrics import run_mutation_tests, run_pytest_on


def audit(source):
    tree = ast.parse(source)
    aliases = {a.asname or a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module == "solution"
               for a in n.names if a.name == "minPath"}
    findings, checked, unknown = [], 0, 0
    for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")):
        values = {}
        for n in ast.walk(fn):
            if isinstance(n, ast.Assign):
                try:
                    value = ast.literal_eval(n.value)
                except (ValueError, TypeError):
                    continue
                for name in n.targets:
                    if isinstance(name, ast.Name): values[name.id] = value
        for call in (n for n in ast.walk(fn) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in aliases):
            if not call.args: unknown += 1; continue
            try:
                arg = call.args[0]
                grid = values[arg.id] if isinstance(arg, ast.Name) else ast.literal_eval(arg)
                size = len(grid)
                square = isinstance(grid, list) and size >= 2 and all(isinstance(row, list) and len(row) == size for row in grid)
                flat = [x for row in grid for x in row] if square else []
                valid = square and all(type(x) is int for x in flat) and sorted(flat) == list(range(1, size*size+1))
            except (KeyError, TypeError, ValueError):
                unknown += 1; continue
            checked += 1
            if not valid:
                findings.append({"test": fn.name, "line": call.lineno, "grid": grid,
                                 "reason": "Contract requires N>=2 square grid and each integer 1..N*N exactly once"})
    return tree, findings, checked, unknown


def main():
    output = ROOT / "results/testgen_formal_v1"
    instances = load_dataset(output / "source/benchmarks/humaneval_plus_v2_20.jsonl")
    instance = next(x for x in instances if x.instance_id == "HumanEval/129")
    reports = {}
    for variant in ("A0", "A4"):
        path = output / variant / "HumanEval__129.tests.py"
        original = path.read_text(); tree, findings, checked, unknown = audit(original)
        bad = {row["test"] for row in findings}
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef)):
                node.body = [n for n in node.body if not isinstance(n, ast.FunctionDef) or n.name not in bad]
        filtered = ast.unparse(tree)+"\n"
        with tempfile.TemporaryDirectory(prefix="minpath-audit-") as tmp:
            workspace = Path(tmp)
            (workspace/"solution.py").write_text(instance.solution_source)
            (workspace/"test_solution.py").write_text(filtered)
            reference = run_pytest_on("test_solution.py", workspace, timeout=10)
            mutation = run_mutation_tests(workspace, instance.solution_source, "test_solution.py", timeout=5)
        reports[variant] = {"suite_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                            "literal_calls_checked": checked, "calls_unknown": unknown,
                            "invalid_inputs": findings, "removed_test_functions": sorted(bad),
                            "filtered_reference_passed": reference.all_pass,
                            "filtered_mutants_total": mutation["total"], "filtered_mutants_killed": mutation["killed"],
                            "filtered_mutation_score": mutation["score"], "filtered_mutants_errors": mutation["errors"]}
    receipt = {"scope": "Post-hoc single-case sensitivity audit, not the preregistered primary score",
               "instance_id": instance.instance_id, "original_records_unchanged": True,
               "limitation": "Literal grids and simple local assignments only; unknown expressions remain unchecked. Does not certify all input domains or all oracles.",
               "variants": reports}
    destination = ROOT/"verification/testgen-formal-v1/minpath-domain-audit.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
