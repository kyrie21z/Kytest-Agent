"""Read-only audit of the historical 80 records; no model calls or scoring changes."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit(root=ROOT / "results/v2_ablation"):
    rows = {v: {d["instance_id"]: d for p in (root / v).glob("*.json") for d in [json.loads(p.read_text())]}
            for v in ("A0", "A1", "A2", "A3")}
    if any(len(r) != 20 for r in rows.values()) or any(set(r) != set(rows["A0"]) for r in rows.values()):
        raise ValueError("Expected identical 20-instance sets for A0-A3")
    result = {}
    for v in ("A2", "A3"):
        actions = [a for d in rows[v].values() for a in d["agent"]["system_actions"]]
        result[v] = {"action_count": len(actions), "status_counts": dict(Counter(a["status"] for a in actions)),
                     "decision_counts": dict(Counter(a["decision"] for a in actions)),
                     "coverage_calls": sum(max([a["coverage_rounds"] for a in d["agent"]["system_actions"]] + [0]) for d in rows[v].values())}
    non_timeout = [(a, rows["A3"][iid]) for iid, a in rows["A2"].items()
                   if a["status"] != "timeout" and rows["A3"][iid]["status"] != "timeout"]
    result["non_timeout_pairs"] = len(non_timeout)
    result["non_timeout_all_tied"] = all(a["final"]["mutation_score"] == b["final"]["mutation_score"] for a, b in non_timeout)
    return result


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
