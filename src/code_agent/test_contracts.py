"""Bounded candidate analysis and executed-path guards; neither proves an oracle."""
from __future__ import annotations

import ast
import functools
import inspect
import operator

UNKNOWN = object()
MAX_TARGET_CALLS = 128


def check_values(contract, values):
    violations, applied = [], 0
    def operand(text):
        if text.lstrip("-").isdigit():
            return int(text)
        return len(values[text[4:-1]]) if text.startswith("len(") else values[text]
    for low, op1, middle, op2, high in contract["ranges"]:
        try:
            a, b, c = (operand(x) for x in (low, middle, high))
            valid = (a <= b if op1 == "<=" else a < b) and (b <= c if op2 == "<=" else b < c)
        except (KeyError, TypeError, ValueError):
            continue
        applied += 1
        if not valid:
            violations.append(f"violates documented {low} {op1} {middle} {op2} {high}")
    for name in contract["positive"]:
        if name in values:
            applied += 1
            value = values[name]
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                violations.append(f"{name} must be a positive integer")
    for name in contract["nonempty"]:
        if name in values:
            applied += 1
            try:
                valid = len(values[name]) > 0
            except TypeError:
                valid = False
            if not valid:
                violations.append(f"{name} must be non-empty")
    for name in contract["positive_elements"]:
        if name in values:
            applied += 1
            value = values[name]
            if not isinstance(value, (list, tuple)) or not all(isinstance(x, int) and not isinstance(x, bool) and x > 0 for x in value):
                violations.append(f"{name} must contain positive integers")
    types = {"int": int, "float": (int, float), "str": str, "list": list, "tuple": tuple}
    for name, kind in contract.get("types", {}).items():
        if name in values and kind in types:
            applied += 1
            if not isinstance(values[name], types[kind]) or kind == "int" and isinstance(values[name], bool):
                violations.append(f"{name} must satisfy the explicit {kind} annotation")
    name = contract.get("permutation_grid")
    if name in values:
        applied += 1
        grid = values[name]
        valid = isinstance(grid, list) and len(grid) >= 2 and all(isinstance(r, list) and len(r) == len(grid) for r in grid)
        if valid:
            flat = [x for row in grid for x in row]
            valid = all(type(x) is int for x in flat) and sorted(flat) == list(range(1, len(grid)**2 + 1))
        if not valid:
            violations.append(f"{name} must be an N>=2 square permutation of 1..N*N")
    return bool(applied), violations


def constant(node, values):
    """Evaluate a small expression language without executing candidate code."""
    if isinstance(node, ast.Name):
        return values.get(node.id, UNKNOWN)
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError):
        pass
    if isinstance(node, (ast.List, ast.Tuple)) and len(node.elts) <= MAX_TARGET_CALLS:
        parts = [constant(n, values) for n in node.elts]
        if all(x is not UNKNOWN for x in parts):
            return tuple(parts) if isinstance(node, ast.Tuple) else parts
    if isinstance(node, ast.BinOp) and type(node.op) in (ast.Add, ast.Sub, ast.Mult):
        left, right = constant(node.left, values), constant(node.right, values)
        if type(left) in (int, float) and type(right) in (int, float):
            return {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul}[type(node.op)](left, right)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("range", "len"):
        args = [constant(x, values) for x in node.args]
        try:
            if node.func.id == "range" and all(type(x) is int for x in args):
                return range(*args)
            if node.func.id == "len" and len(args) == 1 and args[0] is not UNKNOWN:
                return len(args[0])
        except (ValueError, TypeError, OverflowError):
            pass
    return UNKNOWN


def local_bindings(node):
    """Bindings of this function, excluding nested functions and comprehensions."""
    class Locals(ast.NodeVisitor):
        def __init__(self):
            self.names, self.globals = set(), set()
        def visit_Name(self, child):
            if isinstance(child.ctx, ast.Store):
                self.names.add(child.id)
        def visit_ImportFrom(self, child):
            self.names.update(a.asname or a.name for a in child.names)
        visit_Import = visit_ImportFrom
        def visit_FunctionDef(self, child):
            self.names.add(child.name)
        def visit_Global(self, child):
            self.globals.update(child.names)
        def visit_Lambda(self, child):
            pass
        visit_ListComp = visit_Lambda
        visit_SetComp = visit_Lambda
        visit_DictComp = visit_Lambda
        visit_GeneratorExp = visit_Lambda
    visitor = Locals()
    for child in node.body:
        visitor.visit(child)
    return visitor.names - visitor.globals


class CandidateAnalysis(ast.NodeVisitor):
    def __init__(self, contracts, *, assertions=False, max_calls=MAX_TARGET_CALLS):
        self.contracts, self.assertions, self.max_calls = contracts, assertions, max_calls
        self.bindings, self.values, self.dependent = {}, {}, set()
        self.effective_dependent = set()
        self.canceled_assertions = 0
        self.calls = self.checked = self.unknown = 0
        self.violations, self.assertion_errors = [], []
        self.relevant_assertions = self.anchors = 0

    def target(self, call):
        if isinstance(call.func, ast.Name):
            name = self.bindings.get(call.func.id)
            return name if name in self.contracts else None
        if isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name) and self.bindings.get(call.func.value.id) == "@solution":
            return call.func.attr if call.func.attr in self.contracts else None
        return None

    def depends(self, node):
        return any(isinstance(n, ast.Call) and self.target(n) or isinstance(n, ast.Name) and n.id in self.dependent for n in ast.walk(node))

    def effective_depends(self, node):
        """Ignore simple output cancellation, without simplifying arbitrary Python.

        Only repeated reads of one name are canceled; two function calls can
        produce different results. This is an anchor policy for ordinary
        arithmetic, not a proof about floats or overloaded operators.
        """
        if isinstance(node, ast.BinOp):
            repeated_name = (isinstance(node.left, ast.Name) and
                             isinstance(node.right, ast.Name) and
                             node.left.id == node.right.id)
            if isinstance(node.op, ast.Sub) and repeated_name:
                return False
            if isinstance(node.op, ast.Mult):
                operands = (constant(node.left, self.values), constant(node.right, self.values))
                if any(type(value) in (int, float) and value == 0 for value in operands):
                    return False
        if isinstance(node, ast.Name):
            return node.id in self.effective_dependent
        if isinstance(node, ast.Call) and self.target(node):
            return True
        return any(self.effective_depends(child) for child in ast.iter_child_nodes(node))

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.bindings[alias.asname or alias.name] = alias.name if node.module == "solution" else "@other"

    def visit_Import(self, node):
        for alias in node.names:
            self.bindings[alias.asname or alias.name] = "@solution" if alias.name == "solution" else "@other"

    def visit_FunctionDef(self, node):
        original = self.bindings.copy(), self.values.copy(), self.dependent.copy(), self.effective_dependent.copy()
        # Python local binding applies throughout the function, including uses
        # before an assignment/import. Nested scopes are handled separately.
        for name in local_bindings(node):
            self.bindings[name] = "@local"
            self.values.pop(name, None)
            self.dependent.discard(name)
            self.effective_dependent.discard(name)
        for child in node.body:
            self.visit(child)
        self.bindings, self.values, self.dependent, self.effective_dependent = original

    def visit_Assign(self, node):
        self.visit(node.value)
        value, dependent = constant(node.value, self.values), self.depends(node.value)
        effective = self.effective_depends(node.value)
        binding = self.bindings.get(node.value.id) if isinstance(node.value, ast.Name) else None
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.values[target.id] = value
                self.bindings[target.id] = binding or "@local"
                if dependent:
                    self.dependent.add(target.id)
                else:
                    self.dependent.discard(target.id)
                if effective:
                    self.effective_dependent.add(target.id)
                else:
                    self.effective_dependent.discard(target.id)

    def visit_AnnAssign(self, node):
        if node.value is not None:
            self.visit_Assign(ast.Assign(targets=[node.target], value=node.value))

    def visit_AugAssign(self, node):
        if isinstance(node.target, ast.Name):
            self.visit_Assign(ast.Assign(targets=[node.target], value=ast.BinOp(left=ast.Name(id=node.target.id, ctx=ast.Load()), op=node.op, right=node.value)))
        else:
            self.generic_visit(node)

    def visit_If(self, node):
        value = constant(node.test, self.values)
        if value is not UNKNOWN:
            for child in node.body if value else node.orelse:
                self.visit(child)
            return
        original = self.bindings.copy(), self.values.copy(), self.dependent.copy(), self.effective_dependent.copy()
        self.visit(node.test)
        for child in node.body:
            self.visit(child)
        left = self.bindings.copy(), self.values.copy(), self.dependent.copy(), self.effective_dependent.copy()
        self.bindings, self.values, self.dependent, self.effective_dependent = original
        for child in node.orelse:
            self.visit(child)
        self.bindings = {k: v if self.bindings.get(k) == v else "@unknown" for k, v in left[0].items()}
        self.values = {k: v if v is not UNKNOWN and self.values.get(k, UNKNOWN) is not UNKNOWN and self.values[k] == v else UNKNOWN for k, v in left[1].items()}
        self.dependent |= left[2]
        self.effective_dependent |= left[3]

    def visit_Call(self, node):
        target = self.target(node)
        if target:
            self.calls += 1
            contract = self.contracts[target]
            values = {name: constant(value, self.values) for name, value in zip(contract["names"], node.args)}
            values.update({kw.arg: constant(kw.value, self.values) for kw in node.keywords if kw.arg})
            known = {name: value for name, value in values.items() if value is not UNKNOWN}
            applied, violations = check_values(contract, known)
            self.checked += applied
            self.unknown += not applied or len(known) != len(values)
            self.violations.extend(f"{target}: {v}" for v in violations)
        self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            target = self.target(node.value)
            if target and self.contracts[target].get("side_effects"):
                names = {n.id for value in node.value.args for n in ast.walk(value) if isinstance(n, ast.Name)}
                self.dependent.update(names)
                self.effective_dependent.update(names)
        self.generic_visit(node)

    def visit_For(self, node):
        values = constant(node.iter, self.values)
        try:
            size = len(values)
        except (TypeError, OverflowError):
            size = None
        calls = sum(isinstance(n, ast.Call) and bool(self.target(n)) for child in node.body for n in ast.walk(child))
        if size is not None and calls and size * calls > self.max_calls:
            self.violations.append(f"resource limit: loop plans at least {size * calls} target calls; maximum {self.max_calls}")
            return
        if isinstance(node.target, ast.Name) and size is not None and size <= self.max_calls:
            before = self.values.copy()
            for value in values:
                self.values[node.target.id] = value
                for child in node.body:
                    self.visit(child)
            self.values = before
        else:
            self.generic_visit(node)

    def visit_Assert(self, node):
        if self.assertions:
            related = self.depends(node.test)
            if related:
                self.relevant_assertions += 1
                effective = self.effective_depends(node.test)
                if not effective:
                    self.canceled_assertions += 1
                if isinstance(node.test, ast.Compare):
                    operands = [node.test.left, *node.test.comparators]
                    for left, right in zip(operands, operands[1:]):
                        if ast.dump(left) == ast.dump(right):
                            self.assertion_errors.append("Self-comparison cannot distinguish faulty behavior")
                        if effective and self.effective_depends(left) != self.effective_depends(right):
                            self.anchors += 1
                elif effective:
                    self.anchors += 1  # an independent truth predicate
            else:
                self.assertion_errors.append("Assertion does not depend on a target result")
        self.generic_visit(node)

    def report(self):
        if self.calls > self.max_calls:
            self.violations.append(f"resource limit: maximum {self.max_calls} target calls per candidate")
        if self.assertions and self.relevant_assertions and not self.anchors:
            prefix = "Algebraically canceled output: " if self.canceled_assertions else ""
            self.assertion_errors.append(prefix + "Target-derived comparisons require an independent output anchor")
        return {"sut_calls": self.calls, "checked_calls": self.checked, "unchecked_calls": self.unknown,
                "violations": list(dict.fromkeys(self.violations)), "assertion_errors": list(dict.fromkeys(self.assertion_errors))}


def analyze(tree, contracts, *, assertions=False, max_calls=MAX_TARGET_CALLS):
    visitor = CandidateAnalysis(contracts, assertions=assertions, max_calls=max_calls)
    visitor.visit(tree)
    return visitor.report()


def install_guards(module, contracts, max_calls=MAX_TARGET_CALLS):
    """Check actual calls on executed paths, even when a guard exception is caught."""
    state = {"calls": 0, "total_calls": 0, "unchecked_calls": 0, "violations": []}
    for name, contract in contracts.items():
        function = getattr(module, name, None)
        if not callable(function):
            continue
        signature = inspect.signature(function)
        def wrap(function=function, contract=contract, signature=signature, name=name):
            @functools.wraps(function)
            def guarded(*args, **kwargs):
                state["calls"] += 1
                state["total_calls"] += 1
                if state["calls"] > max_calls:
                    message = f"resource limit: maximum {max_calls} target calls per test"
                    if len(state["violations"]) < 5:
                        state["violations"].append(message)
                    raise ValueError(message)
                bound = signature.bind(*args, **kwargs)
                bound.apply_defaults()
                checked, violations = check_values(contract, bound.arguments)
                state["unchecked_calls"] += not checked
                if violations:
                    state["violations"].extend(f"{name}: {v}" for v in violations[:max(0, 5-len(state["violations"]))])
                    raise ValueError("Contract violation: " + "; ".join(violations))
                return function(*args, **kwargs)
            return guarded
        setattr(module, name, wrap())
    return state
