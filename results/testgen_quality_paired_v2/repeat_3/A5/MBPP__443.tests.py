# Accepted by submit_tests; explanations in testgen_report.json.

import pytest as _case0_pytest

def test_largest_neg_single_element():
    """Contract: find the largest negative number from the given list.
    Input domain: list with exactly one negative element.
    Oracle: That single negative number must be returned."""
    from solution import largest_neg
    result = largest_neg([-42])
    assert result == -42

import pytest as _case1_pytest

def test_largest_neg_return_type():
    """Contract: find the largest negative number from the given list.
    Input domain: list of integers.
    Oracle: The return type must be an int (same as input element type)."""
    from solution import largest_neg
    result = largest_neg([-5, -1, 3])
    assert isinstance(result, int)
