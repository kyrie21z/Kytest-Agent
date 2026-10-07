# Accepted by submit_tests; explanations in testgen_report.json.

from solution import is_Monotonic as _case0_is_Monotonic

def test_empty_list():
    """An empty list has no violating pairs, so it is vacuously monotonic."""
    assert _case0_is_Monotonic([]) == True

from solution import is_Monotonic as _case1_is_Monotonic

def test_single_element():
    """A single-element list is vacuously monotonic since there are no adjacent pairs."""
    assert _case1_is_Monotonic([5]) == True

from solution import is_Monotonic as _case2_is_Monotonic

def test_strictly_increasing():
    """A strictly increasing sequence is monotonic (non-decreasing)."""
    assert _case2_is_Monotonic([1, 2, 3, 4, 5]) == True

from solution import is_Monotonic as _case3_is_Monotonic

def test_strictly_decreasing():
    """A strictly decreasing sequence is monotonic (non-increasing)."""
    assert _case3_is_Monotonic([5, 4, 3, 2, 1]) == True

from solution import is_Monotonic as _case4_is_Monotonic

def test_non_monotonic_zigzag():
    """A zigzag pattern violates both non-decreasing and non-increasing orders."""
    assert _case4_is_Monotonic([1, 3, 2]) == False

from solution import is_Monotonic as _case5_is_Monotonic

def test_all_equal_elements():
    """A constant sequence is both non-decreasing and non-increasing simultaneously."""
    assert _case5_is_Monotonic([7, 7, 7, 7]) == True
