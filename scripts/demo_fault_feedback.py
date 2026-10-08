"""Scripted production-loop demo; held-out scoring happens after generation."""
import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from code_agent.assembly import AgentPolicy, create_agent
from code_agent.config import Settings
from code_agent.fault_feedback import fingerprint, independent_pools
from code_agent.llm import LLMResponse, MockLLM, ToolCall
from code_agent.tools.factories import build_registry

SOURCE = '''def classify(value, low, high):
    """For low <= high, return -1 below low, 1 above high, and 0 inside the inclusive interval."""
    if value < low:
        return -1
    if value > high:
        return 1
    return 0
'''
QUOTE = "return -1 below low, 1 above high, and 0 inside the inclusive interval."


def candidate(name, value, expected):
    return {"name": name,
            "code": f"from solution import classify\ndef {name}():\n    assert classify({value}, 2, 8) == {expected}\n",
            "contract_quote": QUOTE, "input_domain": "ordered endpoints 2 <= 8",
            "oracle_reason": f"Compare {value} with the two endpoints, including equality, per the contract",
            "fault_hypothesis": "Incorrect outside result or exclusive rather than inclusive boundary"}


def response(name, args):
    return LLMResponse(tool_calls=[ToolCall("demo", name, json.dumps(args))])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or Path(tempfile.mkdtemp(prefix="fault-demo-"))
    workspace = output / "agent_workspace"
    workspace.mkdir(parents=True, exist_ok=False)
    (workspace / "solution.py").write_text(SOURCE, encoding="utf-8")
    settings = Settings(workspace=workspace, max_steps=6)
    policy = AgentPolicy.test_generation(feedback=True, tool_names=())
    registry = build_registry(settings, policy.tool_names)
    submitter = registry.get("submit_tests").generation
    stages = {}
    def event(e):
        if getattr(e, "name", None) == "submit_tests" and hasattr(e, "content"):
            if len(submitter.snapshot()["accepted"]) == 1:
                stages["before"] = submitter.suite_source()
    llm = MockLLM(responses=[
        response("submit_tests", {"cases": [candidate("test_inside", 5, 0)]}),
        response("inspect_survivors", {}),
        response("submit_tests", {"cases": [candidate("test_below", 1, -1), candidate("test_above", 9, 1),
                                             candidate("test_low_inclusive", 2, 0), candidate("test_high_inclusive", 8, 0)]}),
        response("inspect_survivors", {}),
        LLMResponse(content="Preserved the accepted test and added contract-based outside and adjacent boundary checks.")])
    agent = create_agent(settings, policy, llm=llm, registry=registry, on_event=event)
    agent.state.add_user("Generate tests for solution.py")
    result = agent.run()
    if result.status not in ("completed", "stopped") or len(submitter.snapshot()["accepted"]) != 5 or "before" not in stages:
        raise SystemExit("Production-loop demo failed")
    stages["after"] = submitter.suite_source()
    development, heldout = independent_pools(SOURCE)
    measurements = {}
    # The model has finished. It never receives these candidates or scores.
    for stage, suite in stages.items():
        rows = []
        for mutant in heldout:
            outcome = submitter.evaluate(suite, 2, source=mutant.source)
            rows.append({**mutant.to_dict(), "fingerprint": fingerprint(mutant),
                         "status": outcome["status"],
                         "detected": outcome["status"] == "FAIL" and outcome["returncode"] == 1})
        measurements[stage] = {"reference_passed": submitter.evaluate(suite, 5)["status"] == "PASS",
                               "total": len(rows), "detected": sum(r["detected"] for r in rows), "faults": rows}
        (output / f"{stage}.tests.py").write_text(suite, encoding="utf-8")
    receipt = {"evidence_scope": "controlled scripted demonstration, not real-model quality evidence",
               "design_sha256": hashlib.sha256((ROOT / "Design.md").read_bytes()).hexdigest(),
               "scoring_after_generation": True,
               "feedback_fingerprints": [fingerprint(m) for m in development],
               "heldout_fingerprints": [fingerprint(m) for m in heldout],
               "measurements": measurements, "agent_status": result.status,
               "accepted": len(submitter.snapshot()["accepted"]),
               "development_feedback": submitter.snapshot()["fault_feedback"],
               "quality_actions": submitter.snapshot()["quality_actions"], "stop_reason": result.error,
               "reference_unchanged": (workspace / "solution.py").read_text() == SOURCE}
    (output / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    if not receipt["reference_unchanged"] or not all(m["reference_passed"] for m in measurements.values()):
        raise SystemExit("Reference compatibility failed")
    if not heldout or measurements["after"]["detected"] <= measurements["before"]["detected"]:
        raise SystemExit("Controlled transfer acceptance failed")
    print(json.dumps({"scope": receipt["evidence_scope"], "measurements": {
        k: {"detected": v["detected"], "total": v["total"]} for k, v in measurements.items()},
        "output": str(output)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
