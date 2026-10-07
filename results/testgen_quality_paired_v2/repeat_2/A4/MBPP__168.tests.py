# Accepted by submit_tests; explanations in testgen_report.json.

from solution import frequency as _case0_frequency

def test_frequency_basic():
    """Count occurrences of a number appearing multiple times in a list."""
    result = _case0_frequency([1, 2, 3, 2, 4, 2], 2)
    assert result == 3

from solution import frequency as _case1_frequency

def test_frequency_not_present():
    """Count returns zero when x does not appear in the list."""
    result = _case1_frequency([1, 2, 3, 4, 5], 6)
    assert result == 0

from solution import frequency as _case2_frequency

def test_frequency_empty_list():
    """Count on an empty list always returns zero regardless of x."""
    result = _case2_frequency([], 5)
    assert result == 0

from solution import frequency as _case3_frequency

def test_frequency_all_match():
    """When every element equals x, count equals the length of the list."""
    result = _case3_frequency([7, 7, 7, 7], 7)
    assert result == 4

from solution import frequency as _case4_frequency

def test_frequency_negative_numbers():
    """Count works correctly with negative numbers."""
    result = _case4_frequency([-1, -2, -1, -3, -1], -1)
    assert result == 3

from solution import frequency as _case5_frequency

def test_frequency_single_element():
    """A single-element list returns 1 if it matches, 0 otherwise."""
    assert _case5_frequency([42], 42) == 1
    assert _case5_frequency([42], 99) == 0
