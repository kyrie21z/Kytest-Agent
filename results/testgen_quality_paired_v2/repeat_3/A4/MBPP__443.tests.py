# Accepted by submit_tests; explanations in testgen_report.json.

import solution as _case0_solution

def test_largest_neg_single_negative():
    """Contract: "find the largest negative number from the given list."
Input domain: list with exactly one negative number.
Oracle: That single negative number should be returned.
Fault hypothesis: With a single element, min and max-negative coincide, so this tests basic functionality."""
    result = _case0_solution.largest_neg([-42])
    assert result == -42

import solution as _case1_solution

def test_largest_neg_two_negatives_equal():
    """Contract: "find the largest negative number from the given list."
Input domain: list with duplicate negative values.
Oracle: Any occurrence of the largest negative value is acceptable.
Fault hypothesis: Duplicate handling should not affect correctness."""
    result = _case1_solution.largest_neg([-3, -3, -3])
    assert result == -3
