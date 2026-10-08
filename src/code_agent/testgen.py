"""Contract-grounded, additive test generation; no benchmark knowledge in this module.

Quotes and oracle explanations are auditable model claims, not proofs. Only a small
set of explicit input constraints can be checked mechanically. Execution on the
reference implementation establishes compatibility, not specification correctness.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

from .agent import TurnDecision
from .proc import run_capture
from .pytest_result import parse_pytest_result
from .tools.base import Tool, ToolError, ToolResult, resolve_workspace_path

TESTGEN_PROMPT = """You are a coding agent generating useful unit tests for solution.py.
Read its docstring and implementation first. Use submit_tests to create test_solution.py.
For each candidate give a verbatim docstring quote, its valid input domain, an
independent explanation of the expected result, and a concrete faulty behavior
the assertion should detect. Derive the oracle from the contract, worked examples,
or mathematical properties; do not obtain expected values by calling the function
under test or copying its implementation. Include discriminating boundary and
return-type checks when the contract supports them. A passing test is not necessarily
a useful test. Preserve accepted tests and add complementary cases.
Do not assume unspecified invalid inputs must raise: a precondition is not a
promise of input validation. Empty/null inputs need explicit contractual support.
Use small representative inputs and bounded samples, never exhaustive Cartesian
products or huge stress tests. Each candidate is a self-contained Python module
with imports and exactly one test_* function, with no parameters or decorators.
Use assertions or pytest.raises only for documented exceptions. No fixtures,
test classes, module-level execution, or tests that alter solution.py.
Submit up to six candidates at once. The tool checks each separately, returning
the exact rejected test, assertion failure, or timeout, then merges only passing
cases after a regression check. Fix rejected candidates in a later submission.
Accepted names are immutable; use a new name to add a different case. Do not write
test_solution.py directly. Finish with the accepted suite and explain its remaining
limitations; never claim mutation improvement or complete correctness without evidence.
"""


def _normalized(text: str) -> str:
    return " ".join(text.split())


def explicit_constraints(source: str) -> Dict[str, Dict[str, Any]]:
    """Recognize explicit ranges/positive/nonempty preconditions, never invent raises."""
    contracts = {}
    for fn in ast.parse(source).body:
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        doc = ast.get_docstring(fn) or ""
        names = [a.arg for a in fn.args.posonlyargs + fn.args.args]
        operand = r"(?:-?\d+|len\(\w+\)|\b\w+\b)"
        ranges = re.findall(rf"({operand})\s*(<=|<)\s*({operand})\s*(<=|<)\s*({operand})", doc)
        positive = [n for n in names if re.search(rf"positive integer\s+`?{re.escape(n)}\b", doc, re.I)]
        nonempty = []
        if names and re.search(r"non[- ]empty (?:array|list|string)", doc, re.I):
            nonempty.append(names[0])
        contracts[fn.name] = {"doc": doc, "names": names, "ranges": ranges,
                              "positive": positive, "nonempty": nonempty,
                              "positive_elements": names[:1] if re.search(r"(?:array|list) of positive integers", doc, re.I) else [],
                              "types": {a.arg: a.annotation.id for a in fn.args.posonlyargs + fn.args.args if isinstance(a.annotation, ast.Name)},
                              "side_effects": bool(re.search(r"in[- ]place|modif(?:y|ies).*?(?:input|list|array)", doc, re.I)),
                              "permutation_grid": names[0] if names and re.search(r"N rows and N columns.*?N\s*>=\s*2", doc, re.S) and "exactly once" in doc and re.search(r"\[1,\s*N\s*\*\s*N\]", doc) else None}
    return contracts


def check_literal_inputs(tree: ast.Module, contracts: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Resolve bounded constants/aliases; dynamic expressions remain explicitly unknown."""
    from .test_contracts import analyze
    return analyze(tree, contracts)


class SubmitTestsTool(Tool):
    name = "submit_tests"
    description = "Validate contract-grounded test candidates individually, report failures/timeouts, and append accepted tests with a regression check."
    _fields = ("name", "code", "contract_quote", "input_domain", "oracle_reason", "fault_hypothesis")
    parameters = {
        "type": "object", "properties": {"cases": {"type": "array", "maxItems": 6,
            "items": {"type": "object", "properties": {k: {"type": "string"} for k in _fields},
                      "required": list(_fields), "additionalProperties": False}}},
        "required": ["cases"], "additionalProperties": False,
    }

    def __init__(self, settings: Any):
        super().__init__(settings)
        source_path = resolve_workspace_path(self.workspace, "solution.py", must_exist=True)
        if source_path.stat().st_size > settings.max_file_bytes:
            raise ToolError("solution.py exceeds MAX_FILE_BYTES; use a bounded standalone target")
        self.source = source_path.read_text(encoding="utf-8")
        self.contracts = explicit_constraints(self.source)
        self.accepted: Dict[str, Dict[str, str]] = {}
        self.attempts: List[Dict[str, Any]] = []
        self.subprocess_runs = 0
        self.validation_seconds = 0.0
        self.case_timeout = 2.0
        self.suite_timeout = 5.0
        self.max_attempts = 24
        self.max_target_calls = 128
        self.inspector = None
        self.quality_actions: List[Dict[str, Any]] = []
        self.sut_restorations = 0
        tests = resolve_workspace_path(self.workspace, "test_solution.py")
        if tests.exists() and tests.stat().st_size > settings.max_file_bytes:
            raise ToolError("Existing test_solution.py exceeds MAX_FILE_BYTES")
        self.previous_tests = tests.read_text(encoding="utf-8") if tests.exists() else None
        self.seed_names = {n.name for n in ast.parse(self.previous_tests or "").body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}

    def _prepare(self, candidate: Any) -> tuple[Dict[str, Any], ast.Module]:
        if not isinstance(candidate, dict) or set(candidate) != set(self._fields):
            raise ToolError("Each case requires exactly: " + ", ".join(self._fields))
        if any(not isinstance(candidate[k], str) or not candidate[k].strip() for k in self._fields):
            raise ToolError("All case fields must be nonempty strings")
        if len(candidate["code"]) > 5000 or any(len(candidate[k]) > 1200 for k in self._fields if k != "code"):
            raise ToolError("Keep each case small: code <=5000 characters, explanations <=1200")
        name = candidate["name"]
        if len(name) > 120 or not re.fullmatch(r"test_[A-Za-z0-9_]+", name):
            raise ToolError("name must be a test_* Python identifier")
        quote = _normalized(candidate["contract_quote"])
        if not any(quote in _normalized(c["doc"]) for c in self.contracts.values()):
            if len(quote) >= 2 and (quote[0], quote[-1]) in (("\"", "\""), ("'", "'"), ("“", "”"), ("‘", "’"), ("`", "`")):
                quote = quote[1:-1].strip()
        if len(quote) < 12 or not any(quote in _normalized(c["doc"]) for c in self.contracts.values()):
            raise ToolError("contract_quote must quote at least 12 characters verbatim from a solution.py docstring")
        try:
            tree = ast.parse(candidate["code"])
        except SyntaxError as exc:
            raise ToolError(f"Syntax error: {exc}") from exc
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
        if len(functions) != 1 or functions[0].name != name:
            raise ToolError("Provide exactly one top-level function matching name")
        fn = functions[0]
        if fn.decorator_list or fn.args.args or fn.args.posonlyargs or fn.args.kwonlyargs or fn.args.vararg or fn.args.kwarg:
            raise ToolError("Test functions cannot have decorators, parameters, or fixtures")
        if any(not isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef)) and
               not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)) for n in tree.body):
            raise ToolError("Only imports, a docstring, and one test function are allowed at module level")
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and (n.level or n.module not in ("solution", "pytest", "math")):
                raise ToolError("Imports are limited to solution, pytest, math")
            if isinstance(n, ast.ImportFrom) and any(a.name == "*" for a in n.names):
                raise ToolError("Wildcard imports are not supported")
            if isinstance(n, ast.Import) and any(a.name not in ("solution", "pytest", "math") for a in n.names):
                raise ToolError("Imports are limited to solution, pytest, math")
        assertions = [n for n in ast.walk(fn) if isinstance(n, ast.Assert)]
        raises = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "raises" for n in ast.walk(fn))
        if not assertions and not raises:
            raise ToolError("A candidate must contain assertions or a documented pytest.raises check")
        if raises and not re.search(r"rais|exception|error|throw", candidate["contract_quote"], re.I):
            raise ToolError("pytest.raises needs a quoted contractual exception promise; preconditions alone do not promise validation")
        if assertions and all(isinstance(a.test, ast.Constant) for a in assertions):
            raise ToolError("Constant-only assertions do not check function behavior")
        from .test_contracts import analyze
        checks = analyze(tree, self.contracts, assertions=True, max_calls=self.max_target_calls)
        if checks["violations"]:
            raise ToolError("Contract violation: " + "; ".join(checks["violations"]))
        if not checks["sut_calls"]:
            raise ToolError("Candidate must invoke a function imported from solution.py")
        if checks["assertion_errors"]:
            raise ToolError("Oracle check: " + "; ".join(checks["assertion_errors"]))
        return checks, tree

    def _execute(self, code: str, timeout: float, *, source: str | None = None) -> Dict[str, Any]:
        # The child can see only the immutable SUT and proposed tests, never the
        # parent workspace's .env, previous proposals, official tests, or evaluator.
        with tempfile.TemporaryDirectory(prefix="testgen-") as tmp:
            root = Path(tmp)
            sut_source = self.source if source is None else source
            (root / "solution.py").write_text(sut_source, encoding="utf-8")
            (root / "test_solution.py").write_text(code, encoding="utf-8")
            (root / "_testgen_contracts.py").write_bytes(Path(__file__).with_name("test_contracts.py").read_bytes())
            (root / "conftest.py").write_text(
                "import json\nfrom pathlib import Path\nimport solution\n"
                "from _testgen_contracts import install_guards\n"
                f"_checks = install_guards(solution, {self.contracts!r}, {self.max_target_calls})\n"
                "def pytest_runtest_setup(item):\n    _checks['calls'] = 0\n"
                "def pytest_sessionfinish(session, exitstatus):\n"
                "    Path('.testgen_checks.json').write_text(json.dumps(_checks))\n"
                "    if _checks['violations']:\n        session.exitstatus = 1\n", encoding="utf-8")
            result = run_capture([sys.executable, "-m", "pytest", "test_solution.py", "-q",
                                  "--tb=short", "--no-header", "-p", "no:cacheprovider"],
                                 cwd=root, timeout=timeout, execution_mode=self.settings.execution_mode,
                                 env={"PYTHONPATH": str(root), "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"})
            unchanged = (root / "solution.py").exists() and (root / "solution.py").read_text(encoding="utf-8") == sut_source
            guard_file = root / ".testgen_checks.json"
            try:
                runtime_checks = json.loads(guard_file.read_text()) if guard_file.exists() else None
            except (ValueError, OSError):
                runtime_checks = None
        self.subprocess_runs += 1
        self.validation_seconds += result.duration_sec
        output = (result.stdout + result.stderr + (result.error or ""))[-1800:]
        status = "PASS" if parse_pytest_result(result).all_pass and unchanged else "FAIL"
        if result.timed_out:
            status = "TIMEOUT"
        elif runtime_checks is not None and runtime_checks["violations"]:
            status = "RESOURCE_LIMIT" if any("resource limit:" in v for v in runtime_checks["violations"]) else "CONTRACT_VIOLATION"
            output += "\n" + "; ".join(runtime_checks["violations"][:3])
        elif status == "PASS" and (runtime_checks is None or not runtime_checks["total_calls"]):
            status = "NO_TARGET_CALL"
        if not unchanged:
            status = "SUT_MODIFIED"
        return {"status": status, "returncode": result.exit_code,
                "seconds": round(result.duration_sec, 3), "diagnostic": output,
                "timeout_seconds": timeout, "runtime_contract_checks": runtime_checks}

    def suite_source(self, extra: Dict[str, str] | None = None) -> str:
        # Different candidates may use the same imported alias. Rename aliases
        # per case before merging to preserve each test's binding and semantics.
        cases = list(self.accepted.values()) + ([extra] if extra else [])
        chunks = [self.previous_tests] if self.previous_tests else []
        prefix = "_new" + hashlib.sha256(self.previous_tests.encode()).hexdigest()[:8] if self.previous_tests else "_case"
        for index, case in enumerate(cases):
            tree = ast.parse(case["code"])
            aliases = {}
            for node in tree.body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    for alias in node.names:
                        if alias.name == "*":
                            raise ToolError("Wildcard imports are not supported")
                        old = alias.asname or alias.name
                        alias.asname = f"{prefix}{index}_{old}"
                        aliases[old] = alias.asname
            class Rename(ast.NodeTransformer):
                protected = set()
                def visit_FunctionDef(self, node):
                    from .test_contracts import local_bindings
                    previous = self.protected
                    self.protected = local_bindings(node)
                    self.generic_visit(node)
                    self.protected = previous
                    return node
                def visit_ListComp(self, node):
                    previous = self.protected
                    # The outermost iterable evaluates in the enclosing scope.
                    node.generators[0].iter = self.visit(node.generators[0].iter)
                    self.protected = previous | {n.id for g in node.generators for n in ast.walk(g.target) if isinstance(n, ast.Name)}
                    for index, generator in enumerate(node.generators):
                        if index:
                            generator.iter = self.visit(generator.iter)
                        generator.ifs = [self.visit(n) for n in generator.ifs]
                    if isinstance(node, ast.DictComp):
                        node.key, node.value = self.visit(node.key), self.visit(node.value)
                    else:
                        node.elt = self.visit(node.elt)
                    self.protected = previous
                    return node
                visit_SetComp = visit_ListComp
                visit_DictComp = visit_ListComp
                visit_GeneratorExp = visit_ListComp
                def visit_Name(self, node):
                    if node.id in aliases and node.id not in self.protected:
                        node.id = aliases[node.id]
                    return node
            tree = Rename().visit(tree)
            chunks.append(ast.unparse(tree))
        return "# Accepted by submit_tests; explanations in testgen_report.json.\n\n" + "\n\n".join(chunks) + "\n"

    def publish(self) -> Dict[str, bool]:
        sut = resolve_workspace_path(self.workspace, "solution.py")
        tests = resolve_workspace_path(self.workspace, "test_solution.py")
        restored = not sut.exists() or sut.read_text(encoding="utf-8") != self.source
        if restored:
            sut.write_text(self.source, encoding="utf-8")
            self.sut_restorations += 1
        source = self.suite_source() if self.accepted else self.previous_tests
        altered = tests.exists() and tests.read_text(encoding="utf-8") != source
        if source is not None:
            tests.write_text(source, encoding="utf-8")
        elif tests.exists():
            # Preserve a bypassed proposal for inspection, but never score it as
            # an accepted test. A preexisting user suite is restored above.
            resolve_workspace_path(self.workspace, "testgen_unvalidated.py").write_text(tests.read_text(encoding="utf-8"), encoding="utf-8")
            tests.unlink()
        report = {"schema": "testgen-v2", "sut_sha256": hashlib.sha256(self.source.encode()).hexdigest(),
                  "accepted": list(self.accepted.values()), "attempts": self.attempts,
                  "subprocess_runs": self.subprocess_runs, "validation_seconds": round(self.validation_seconds, 3),
                  "limits": {"case_seconds": self.case_timeout, "suite_seconds": self.suite_timeout, "attempts": self.max_attempts, "target_calls_per_test": self.max_target_calls},
                  "quality_actions": self.quality_actions, "sut_restorations": self.sut_restorations,
                  "limitations": "Quotes and complex oracles remain model claims. Known constraints are checked on bounded static and executed paths; unknown contracts and unexecuted paths are not certified. Passing execution is not proof of mutation quality."}
        resolve_workspace_path(self.workspace, "testgen_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"solution_restored": restored, "unvalidated_tests_replaced": altered}

    def run(self, cases: List[Dict[str, str]]) -> ToolResult:
        if not self.settings.allow_write or not self.settings.allow_code_execution or self.settings.execution_mode == "disabled":
            return ToolResult.failure("submit_tests requires ALLOW_WRITE and ALLOW_CODE_EXECUTION, with execution enabled")
        if not isinstance(cases, list) or not 1 <= len(cases) <= 6:
            return ToolResult.failure("Submit between one and six cases")
        results = []
        for candidate in cases:
            name = candidate.get("name", "?") if isinstance(candidate, dict) else "?"
            if len(self.attempts) >= self.max_attempts:
                results.append({"name": name, "status": "BUDGET_EXHAUSTED"})
                continue
            record: Dict[str, Any] = {"name": name}
            try:
                checks, _ = self._prepare(candidate)
                record["contract_checks"] = checks
                if name in self.accepted:
                    record["status"] = "ALREADY_ACCEPTED" if candidate == self.accepted[name] else "NAME_LOCKED"
                elif name in self.seed_names:
                    record["status"] = "NAME_LOCKED"
                else:
                    record.update(self._execute(candidate["code"], self.case_timeout))
                    if record["status"] == "PASS":
                        merged = self._execute(self.suite_source(candidate), self.suite_timeout)
                        if merged["status"] == "PASS":
                            self.accepted[name] = dict(candidate)
                            record["status"] = "ACCEPTED"
                        else:
                            record.update(merged)
                            record["status"] = "REGRESSION_" + merged["status"]
            except (ToolError, SyntaxError) as exc:
                record.update(status="REJECTED", diagnostic=str(exc))
            self.attempts.append(record)
            results.append(record)
        self.publish()
        # Keep a complete structured batch response inside the registry's 6000
        # character limit; the full diagnostics remain in the audit artifact.
        feedback = [{**r, **({"diagnostic": r["diagnostic"][:200] + "\n...\n" + r["diagnostic"][-300:]}
                            if len(r.get("diagnostic", "")) > 500 else {})} for r in results]
        summary = {"accepted_total": len(self.accepted), "attempts_remaining": max(0, self.max_attempts-len(self.attempts)), "results": feedback}
        return ToolResult.success(json.dumps(summary, ensure_ascii=False))


def make_testgen_hook(tool: SubmitTestsTool):
    """Preserve A4 validity; linked A5 also checks development quality before finish."""
    last_feedback_digest = None
    stagnant_turns = 0
    def hook(agent, outcome):
        nonlocal last_feedback_digest, stagnant_turns
        if not tool.settings.allow_write:
            return None
        repaired = tool.publish()
        if repaired["solution_restored"] or repaired["unvalidated_tests_replaced"]:
            agent.state.add_user("[System] Restored the immutable SUT and accepted suite. Submit candidates through submit_tests; direct writes are unvalidated.")
        if not outcome.tool_results and not tool.accepted and len(tool.attempts) < tool.max_attempts:
            agent.state.add_user("[System] No accepted tests yet. Read solution.py and use submit_tests to submit contract-grounded, bounded candidates.")
            return TurnDecision(continue_=True, reason="no_accepted_tests")
        inspector = tool.inspector
        if inspector is not None and (tool.accepted or tool.previous_tests):
            digest = hashlib.sha256(tool.suite_source().encode()).hexdigest()
            # Check before natural completion while the fixed feedback budget
            # permits it. Explicitly record unmeasured versions on exhaustion.
            response = inspector.run()
            reason = "development_feedback"
            if not response.ok:
                reason = "development_budget_exhausted" if len(inspector.actions) >= inspector.max_rounds else "development_unavailable"
            else:
                report = inspector.last_report
                if digest == last_feedback_digest:
                    stagnant_turns += 1
                else:
                    stagnant_turns = 0
                last_feedback_digest = digest
                if not report["survivors"] and not report["uncertain"]:
                    reason = "development_targets_exhausted"
                elif len(inspector.actions) >= inspector.max_rounds:
                    reason = "development_budget_exhausted"
                elif stagnant_turns >= 2:
                    reason = "development_no_progress"
            end = reason != "development_feedback"
            action = {"turn": outcome.turn, "decision": reason, "suite_sha256": digest,
                      "current_suite_checked": bool(response.ok),
                      "feedback_rounds": len(inspector.actions), "stagnant_turns": stagnant_turns,
                      "newly_detected_faults": inspector.last_report.get("newly_detected_faults", []) if response.ok and not json.loads(response.content).get("cached") else []}
            tool.quality_actions.append(action)
            tool.publish()
            agent.state.add_user("[System] Development quality check: " + response.content +
                                 f"\nDecision: {reason}. Candidate attempts remaining: {max(0, tool.max_attempts-len(tool.attempts))}. "
                                 f"Feedback rounds remaining: {max(0, inspector.max_rounds-len(inspector.actions))}. "
                                 f"Model turns remaining: {max(0, agent.max_turns-agent.state.turn_index)}. "
                                 "Add one or two contract-valid tests for a surviving development target; preserve accepted tests. "
                                 "Survivors may be equivalent and uncertainty is not a detected fault.")
            return TurnDecision(end=end, continue_=not end, reason=reason)
        return None
    return hook
