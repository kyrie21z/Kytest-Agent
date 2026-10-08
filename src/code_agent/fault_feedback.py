"""Development-only fault feedback; disjoint operator families reserved for scoring."""
from __future__ import annotations

import ast
import hashlib

from .faults import generate_mutants

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
