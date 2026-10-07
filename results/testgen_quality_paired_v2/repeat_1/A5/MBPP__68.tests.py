# Accepted by submit_tests; explanations in testgen_report.json.

from solution import is_Monotonic as _case0_is_Monotonic

def test_strictly_increasing():
    """A strictly increasing sequence is monotonic (non-decreasing)."""
    assert _case0_is_Monotonic([1, 2, 3, 4, 5]) is True

from solution import is_Monotonic as _case1_is_Monotonic

def test_strictly_decreasing():
    """A strictly decreasing sequence is monotonic (non-increasing)."""
    assert _case1_is_Monotonic([5, 4, 3, 2, 1]) is True

from solution import is_Monotonic as _case2_is_Monotonic

def test_not_monotonic():
    """A sequence that goes up then down is not monotonic."""
    assert _case2_is_Monotonic([1, 3, 2, 4]) is False

from solution import is_Monotonic as _case3_is_Monotonic

def test_empty_list():
    """An empty list is vacuously monotonic since all() on empty iterable is True."""
    assert _case3_is_Monotonic([]) is True

from solution import is_Monotonic as _case4_is_Monotonic

def test_single_element():
    """A single-element list is trivially monotonic."""
    assert _case4_is_Monotonic([42]) is True

from solution import is_Monotonic as _case5_is_Monotonic

def test_constant_sequence():
    """A constant sequence is both non-decreasing and non-increasing."""
    assert _case5_is_Monotonic([7, 7, 7, 7]) is True
