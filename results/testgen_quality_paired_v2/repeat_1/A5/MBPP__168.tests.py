# Accepted by submit_tests; explanations in testgen_report.json.

from solution import frequency as _case0_frequency

def test_frequency_basic():
    """Test basic counting of an element present in the list."""
    result = _case0_frequency([1, 2, 3, 2, 2], 2)
    assert result == 3

from solution import frequency as _case1_frequency

def test_frequency_empty_list():
    """Test that empty list returns 0 for any target."""
    result = _case1_frequency([], 5)
    assert result == 0

from solution import frequency as _case2_frequency

def test_frequency_not_present():
    """Test that a missing element returns 0."""
    result = _case2_frequency([1, 3, 5, 9], 7)
    assert result == 0

from solution import frequency as _case3_frequency

def test_frequency_all_match():
    """Test when every element equals the target."""
    result = _case3_frequency([4, 4, 4], 4)
    assert result == 3

from solution import frequency as _case4_frequency

def test_frequency_single_element_match():
    """Test single-element list where element matches target."""
    result = _case4_frequency([42], 42)
    assert result == 1

from solution import frequency as _case5_frequency

def test_frequency_negative_numbers():
    """Test counting with negative numbers."""
    result = _case5_frequency([-1, -2, -1, 0, -1], -1)
    assert result == 3
