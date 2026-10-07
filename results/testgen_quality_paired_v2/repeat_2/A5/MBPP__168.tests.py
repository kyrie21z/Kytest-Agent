# Accepted by submit_tests; explanations in testgen_report.json.

from solution import frequency as _case0_frequency

def test_frequency_basic():
    """Contract: count occurrences of x in list a.
    Oracle: [1,2,3,2,4,2] contains three 2s."""
    result = _case0_frequency([1, 2, 3, 2, 4, 2], 2)
    assert result == 3

from solution import frequency as _case1_frequency

def test_frequency_zero_occurrences():
    """Contract: count occurrences of x in list a.
    Oracle: 7 does not appear in [1,2,3,4]."""
    result = _case1_frequency([1, 2, 3, 4], 7)
    assert result == 0

from solution import frequency as _case2_frequency

def test_frequency_empty_list():
    """Contract: count occurrences of x in list a.
    Oracle: empty list has no elements, so any target yields 0."""
    result = _case2_frequency([], 5)
    assert result == 0

from solution import frequency as _case3_frequency

def test_frequency_all_match():
    """Contract: count occurrences of x in list a.
    Oracle: every element is 3, so count equals length."""
    result = _case3_frequency([3, 3, 3, 3], 3)
    assert result == 4

from solution import frequency as _case4_frequency

def test_frequency_single_element_match():
    """Contract: count occurrences of x in list a.
    Oracle: single-element list with matching value yields 1."""
    result = _case4_frequency([42], 42)
    assert result == 1

from solution import frequency as _case5_frequency

def test_frequency_negative_numbers():
    """Contract: count occurrences of x in list a.
    Oracle: -1 appears twice in the mixed list."""
    result = _case5_frequency([-1, 0, -1, 5, -1, 3], -1)
    assert result == 3
