"""Development-only fault feedback; disjoint operator families reserved for scoring."""
from __future__ import annotations

import ast
import difflib
import hashlib
import json
from typing import Any

from .faults import generate_mutants
from .tools.base import Tool, ToolResult, resolve_workspace_path

FEEDBACK_OPERATORS = ("AOR", "CRP")
HELDOUT_OPERATORS = ("ROR", "LCR", "BCR")
FAULT_PROMPT = """
After you have an accepted suite, call inspect_survivors. It runs a bounded set
of development fault candidates and returns changes that existing assertions
did not detect. Use the contract to devise a small valid input and independent
oracle that distinguish these faulty behaviors, then submit complementary tests.
Cover adjacent boundaries of the same behavior, not just the exact shown edit.
Some surviving edits are equivalent to the original on the valid input domain;
do not invent invalid-input requirements or break passing tests to kill them.
State this uncertainty. Feedback faults are not the independent scoring faults;
never present the development kill count as a final quality score. Inspect at
most twice, after changing the accepted suite. Preserve all accepted tests.
"""


def fingerprint(mutant):
    return hashlib.sha256(ast.dump(ast.parse(mutant.source)).encode()).hexdigest()


def independent_pools(source: str, limit: int = 8, scoring_limit: int = 20):
    """Reject any accidental AST overlap rather than scoring on feedback faults."""
    feedback = generate_mutants(source, max_mutants=limit, operators=FEEDBACK_OPERATORS)
    heldout = generate_mutants(source, max_mutants=scoring_limit, operators=HELDOUT_OPERATORS)
    if {fingerprint(m) for m in feedback} & {fingerprint(m) for m in heldout}:
        raise ValueError("Feedback and scoring fault ASTs overlap")
    return feedback, heldout


class InspectSurvivorsTool(Tool):
    name = "inspect_survivors"
    description = "Inspect bounded DEVELOPMENT faults that the accepted suite misses, for targeted additional tests. Not the final scoring pool. Equivalent faults and timeouts remain uncertain."
    parameters = {"type": "object", "properties": {}, "required": [], "additionalProperties": False}

    def __init__(self, settings: Any):
        super().__init__(settings)
        self.submitter = None  # linked by registry assembly; never infer trust from public files
        self.actions = []
        self.last_hash = None
        self.last_report = None
        self.max_rounds = 2
        self.detected_fingerprints = set()

    @staticmethod
    def _public(report):
        # Keep a complete JSON response within the registry's output limit. All
        # development findings are retained in the report, never scoring faults.
        return {**report, "survivors": report["survivors"][:3],
                "survivors_total": len(report["survivors"]),
                "report_file": "fault_feedback.json"}

    def run(self) -> ToolResult:
        tool = self.submitter
        if tool is None:
            return ToolResult.failure("inspect_survivors requires submit_tests in the same registry")
        if not tool.settings.allow_write or not tool.settings.allow_code_execution or tool.settings.execution_mode == "disabled":
            return ToolResult.failure("Fault execution is disabled")
        if not tool.accepted and not tool.previous_tests:
            return ToolResult.failure("Submit a valid suite before inspecting development faults")
        suite = tool.suite_source()
        digest = hashlib.sha256(suite.encode()).hexdigest()
        if digest == self.last_hash:
            return ToolResult.success(json.dumps({"cached": True, **self._public(self.last_report)}, ensure_ascii=False))
        if len(self.actions) >= self.max_rounds:
            return ToolResult.failure("Development feedback budget exhausted (two changed-suite rounds)")
        started_seconds, started_runs = tool.validation_seconds, tool.subprocess_runs
        compatibility = tool._execute(suite, tool.suite_timeout)
        if compatibility["status"] != "PASS":
            return ToolResult.failure("Accepted suite unavailable on the reference: " + json.dumps(compatibility))
        feedback, _ = independent_pools(tool.source)
        # Assert separation here, but never expose held-out IDs, source or counts
        # in the model's feedback or the workspace report.
        killed, survivors, uncertain = [], [], []
        canonical = ast.unparse(ast.parse(tool.source)).splitlines()
        for mutant in feedback:
            outcome = tool._execute(suite, tool.case_timeout, source=mutant.source)
            details = {"mutant_id": mutant.mutant_id, "operator": mutant.operator, "line": mutant.line,
                       "description": mutant.description, "fingerprint": fingerprint(mutant),
                       "status": outcome["status"], "seconds": outcome.get("seconds", 0)}
            if outcome["status"] == "PASS":
                change = "\n".join(difflib.unified_diff(canonical, mutant.source.splitlines(), n=1, lineterm=""))
                survivors.append({**details, "change": change[:600]})
            elif outcome["status"] == "FAIL" and outcome["returncode"] == 1:
                killed.append(details)
            else:
                uncertain.append({**details, "status": outcome["status"]})
        detected = {d["fingerprint"] for d in killed}
        newly_detected = [d for d in killed if d["fingerprint"] not in self.detected_fingerprints]
        lost = sorted(self.detected_fingerprints - detected)
        report = {"scope": "development-only", "round": len(self.actions)+1,
                  "suite_sha256": digest, "detected_faults": killed,
                  "newly_detected_faults": newly_detected, "lost_detections": lost,
                  "validation_seconds": round(tool.validation_seconds-started_seconds, 3),
                  "subprocess_runs": tool.subprocess_runs-started_runs,
                  "reference_passed": True, "total": len(feedback), "detected": len(killed),
                  "survivors": survivors, "uncertain": uncertain,
                  "warning": "Survivors can be equivalent; timeouts are inconclusive. These counts are not the held-out quality score."}
        self.actions.append(report)
        self.detected_fingerprints = detected
        self.last_hash, self.last_report = digest, report
        path = resolve_workspace_path(self.workspace, "fault_feedback.json")
        path.write_text(json.dumps(self.actions, ensure_ascii=False, indent=2), encoding="utf-8")
        return ToolResult.success(json.dumps(self._public(report), ensure_ascii=False))
