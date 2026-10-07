# Accepted by submit_tests; explanations in testgen_report.json.

from solution import is_Monotonic as _case0_is_Monotonic

def test_empty_list():
    """An empty list is trivially monotonic since all() over an empty range yields True."""
    assert _case0_is_Monotonic([]) is True

from solution import is_Monotonic as _case1_is_Monotonic

def test_single_element():
    """A single-element list has no pairs to compare, so it is trivially monotonic."""
    assert _case1_is_Monotonic([42]) is True

from solution import is_Monotonic as _case2_is_Monotonic

def test_strictly_increasing():
    """Strictly increasing sequences satisfy the non-decreasing condition."""
    assert _case2_is_Monotonic([1, 2, 3, 4, 5]) is True

from solution import is_Monotonic as _case3_is_Monotonic

def test_strictly_decreasing():
    """Strictly decreasing sequences satisfy the non-increasing condition."""
    assert _case3_is_Monotonic([5, 4, 3, 2, 1]) is True

from solution import is_Monotonic as _case4_is_Monotonic

def test_constant_list():
    """A constant list is both non-decreasing and non-increasing simultaneously."""
    assert _case4_is_Monotonic([7, 7, 7, 7]) is True

from solution import is_Monotonic as _case5_is_Monotonic

def test_not_monotonic():
    """A zigzag pattern like [1, 3, 2] is neither non-decreasing nor non-increasing."""
    assert _case5_is_Monotonic([1, 3, 2]) is False
