# Accepted by submit_tests; explanations in testgen_report.json.

from solution import frequency as _case0_frequency

def test_frequency_basic():
    """Test basic counting of occurrences in a non-trivial list."""
    result = _case0_frequency([1, 2, 3, 2, 4, 2, 5], 2)
    assert result == 3

from solution import frequency as _case1_frequency

def test_frequency_empty_list():
    """Test that an empty list returns 0 for any search value."""
    result = _case1_frequency([], 5)
    assert result == 0

from solution import frequency as _case2_frequency

def test_frequency_not_present():
    """Test that searching for a value not in the list returns 0."""
    result = _case2_frequency([1, 3, 5, 7], 4)
    assert result == 0

from solution import frequency as _case3_frequency

def test_frequency_all_match():
    """Test when every element matches the search value."""
    result = _case3_frequency([7, 7, 7, 7], 7)
    assert result == 4

from solution import frequency as _case4_frequency

def test_frequency_single_element():
    """Test boundary case of a single-element list matching."""
    result = _case4_frequency([42], 42)
    assert result == 1

from solution import frequency as _case5_frequency

def test_frequency_negative_values():
    """Test counting with negative numbers in the list."""
    result = _case5_frequency([-1, -2, -1, -3, -1], -1)
    assert result == 3
