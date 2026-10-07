# Accepted by submit_tests; explanations in testgen_report.json.

"""Test basic counting of element in tuple."""
from solution import count_X as _case0_count_X

def test_count_X_basic():
    assert _case0_count_X((1, 2, 3, 2, 4, 2), 2) == 3

"""Test when element is not in tuple."""
from solution import count_X as _case1_count_X

def test_count_X_not_present():
    assert _case1_count_X((1, 2, 3, 4, 5), 6) == 0

"""Test empty tuple input."""
from solution import count_X as _case2_count_X

def test_count_X_empty_tuple():
    assert _case2_count_X((), 1) == 0

"""Test when all elements match the target."""
from solution import count_X as _case3_count_X

def test_count_X_all_match():
    assert _case3_count_X((7, 7, 7, 7), 7) == 4

"""Test single-element tuple boundary."""
from solution import count_X as _case4_count_X

def test_count_X_single_element():
    assert _case4_count_X((42,), 42) == 1

"""Test return type is int."""
from solution import count_X as _case5_count_X

def test_count_X_return_type():
    result = _case5_count_X(('a', 'b', 'a'), 'a')
    assert isinstance(result, int)
    assert result == 2
