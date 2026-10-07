"""Explain the one stochastic replay difference without altering frozen results."""
import hashlib
import json
from pathlib import Path
import random
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from eval.dataset import load_dataset
from eval.metrics import run_pytest_on

output = ROOT / "results/testgen_quality_paired_v2"
instance = next(x for x in load_dataset(output / "source/benchmarks/mbpp_quality_v2_20.jsonl")
                if x.instance_id == "MBPP/71")
suite = (output / "repeat_1/A0/MBPP__71.tests.py").read_text()
namespace = {}
exec(instance.solution_source, namespace)
direct = []
for seed in range(1000):
    numbers = list(range(100))
    random.Random(seed).shuffle(numbers)
    before = numbers[:]
    actual = namespace["comb_sort"](numbers)
    direct.append({"seed": seed, "sorted": actual == list(range(100)),
                   "input_sha256": hashlib.sha256(json.dumps(before).encode()).hexdigest()})
passing = [x["seed"] for x in direct if x["sorted"]]
assert passing and len(passing) < len(direct)
# These are diagnostic witnesses selected from the explicit search, not new samples
# for the quality comparison. The original measurement remains unchanged.
seeds = list(range(20)) + passing[:2]
pytest_runs = []
for seed in seeds:
    with tempfile.TemporaryDirectory(prefix="comb-sort-seeded-audit-") as directory:
        workspace = Path(directory)
        (workspace / "solution.py").write_text(instance.solution_source)
        (workspace / "test_solution.py").write_text(suite)
        (workspace / "conftest.py").write_text(
            f"import random\ndef pytest_sessionstart(session):\n    random.seed({seed})\n")
        result = run_pytest_on("test_solution.py", workspace, timeout=10)
        pytest_runs.append({"seed": seed, "all_pass": result.all_pass,
            "summary": result.summary_line, "failure_nodes": result.failure_nodes,
            "reference_preserved": (workspace / "solution.py").read_text() == instance.solution_source})
    assert result.all_pass == direct[seed]["sorted"]
    print(seed, result.all_pass, result.summary_line, flush=True)
receipt = {
    "scope": "Post-generation diagnostic, no model calls or score replacement; original suite and reference unchanged; seed set only in temporary conftest.py",
    "record": "repeat_1/A0/MBPP__71.json", "original_status": "partial_pass",
    "original_primary_score": 0, "independent_replay_reference_passed": True,
    "suite_sha256": hashlib.sha256(suite.encode()).hexdigest(),
    "reference_sha256": hashlib.sha256(instance.solution_source.encode()).hexdigest(),
    "direct_search_seeds": [0, 999], "direct_passed": len(passing),
    "direct_failed": len(direct) - len(passing), "pytest": pytest_runs,
    "direct_reference": direct,
    "conclusion": "Unseeded shuffled inputs expose a reference sorting defect on some inputs. Official examples passing do not prove correctness on all inputs. Preserve original failed run and ITT score 0; strict replay verdict remains false. Diagnostic witness selection is not used for scoring or superiority claims."
}
Path(__file__).with_name("stochastic-reference-diagnostic.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print({"direct_passed": len(passing), "direct_failed": len(direct) - len(passing),
       "pytest_passed": sum(x["all_pass"] for x in pytest_runs),
       "pytest_failed": sum(not x["all_pass"] for x in pytest_runs)}, flush=True)
