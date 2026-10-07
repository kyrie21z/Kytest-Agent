"""Select a new, structurally eligible MBPP test subset without model outcomes."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import random
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from code_agent.fault_feedback import independent_pools

SEED = 20261007
SAFE_IMPORTS = {"math", "re", "collections", "itertools", "functools", "heapq",
                "bisect", "string", "operator", "typing"}


def adapt(row):
    """Keep the reference code; insert the original task description as docstring."""
    tree = ast.parse(row["code"])
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if len(functions) != 1 or any(not isinstance(n, (ast.FunctionDef, ast.Import, ast.ImportFrom)) for n in tree.body):
        raise ValueError("requires one function and imports only")
    fn = functions[0]
    if fn.decorator_list or fn.args.vararg or fn.args.kwarg or fn.args.kwonlyargs:
        raise ValueError("unsupported target signature")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [(node.module or "").split(".")[0]] if not node.level else [""]
        else:
            continue
        if any(module not in SAFE_IMPORTS for module in modules):
            raise ValueError("requires an unsupported or nondeterministic import")
    if ast.get_docstring(fn):
        raise ValueError("existing docstring needs a different adaptation")
    if fn.body[0].lineno == fn.lineno:
        raise ValueError("single-line function cannot receive an unambiguous docstring")
    lines = row["code"].splitlines(keepends=True)
    indent = " " * fn.body[0].col_offset
    lines.insert(fn.body[0].lineno - 1, indent + repr(row["prompt"]) + "\n")
    source = "".join(lines).rstrip() + "\n"
    adapted = ast.parse(source)
    adapted_fn = next(n for n in adapted.body if isinstance(n, ast.FunctionDef))
    assert ast.get_docstring(adapted_fn) == row["prompt"]
    adapted_fn.body.pop(0)
    assert ast.dump(tree) == ast.dump(adapted), "Adaptation changed executable reference AST"
    tests = [f"def check(candidate):", f"    {fn.name} = candidate"]
    for statement in [*row["test_imports"], *row["test_list"]]:
        tests.extend("    " + line for line in statement.splitlines())
    return {"instance_id": f"MBPP/{row['task_id']}", "prompt": "", "solution": source,
            "entry_point": fn.name, "official_tests": "\n".join(tests) + "\n",
            "contract": row["prompt"], "source_task_id": row["task_id"]}


def select_rows(rows, count=20):
    eligible, exclusions = [], {}
    for row in sorted(rows, key=lambda r: r["task_id"]):
        reason = None
        if not 11 <= row["task_id"] <= 510:
            reason = "outside official test partition"
        else:
            try:
                item = adapt(row)
                # Instance.solution_source appends one newline; same source for pools.
                development, heldout = independent_pools("\n" + item["solution"] + "\n")
                if not heldout or not development:
                    reason = "no structural development or held-out fault"
            except (ValueError, SyntaxError, KeyError) as exc:
                reason = str(exc)
        if reason:
            exclusions[str(row["task_id"])] = reason
        else:
            eligible.append(item)
    random.Random(SEED).shuffle(eligible)
    if len(eligible) < count:
        raise ValueError("Insufficient eligible MBPP test tasks")
    chosen = sorted(eligible[:count], key=lambda r: r["source_task_id"])
    return chosen, {"seed": SEED, "raw_tasks": len(rows), "eligible_tasks": len(eligible),
                    "selected_ids": [r["instance_id"] for r in chosen],
                    "selection_uses_model_outcomes": False, "exclusions": exclusions}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    destination = ROOT / "benchmarks/mbpp_quality_v2"
    if destination.exists():
        raise SystemExit("MBPP freeze already exists; do not overwrite inputs")
    chosen, selection = select_rows(json.loads((args.source / "sanitized-mbpp.json").read_text()))
    destination.mkdir()
    for name in ("sanitized-mbpp.json", "README.md", "LICENSE", "download.json"):
        shutil.copyfile(args.source / name, destination / name)
    dataset = ROOT / "benchmarks/mbpp_quality_v2_20.jsonl"
    if dataset.exists():
        raise SystemExit("Dataset already exists")
    dataset.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in chosen))
    selection["dataset_sha256"] = hashlib.sha256(dataset.read_bytes()).hexdigest()
    selection["adaptation"] = "Original prompt inserted verbatim as docstring; executable AST unchanged; official tests withheld from generation"
    selection["source"] = json.loads((args.source / "download.json").read_text())
    (destination / "selection.json").write_text(json.dumps(selection, indent=2) + "\n")
    print(json.dumps({k:v for k,v in selection.items() if k not in {"source", "exclusions"}}, indent=2))


if __name__ == "__main__":
    main()
