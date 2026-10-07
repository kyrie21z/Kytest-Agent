# Accepted by submit_tests; explanations in testgen_report.json.

from solution import frequency as _case0_frequency

def test_frequency_basic():
    """Test basic counting of an element appearing multiple times.
    Contract quote: "count the number of occurrences of a number in a given list."
    Input domain: a=[1,2,3,2,4,2], x=2
    Oracle: 2 appears 3 times in the list, so result must be 3.
    Fault hypothesis: If the loop or comparison is broken, count will be wrong."""
    result = _case0_frequency([1, 2, 3, 2, 4, 2], 2)
    assert result == 3

from solution import frequency as _case1_frequency

def test_frequency_empty_list():
    """Test that an empty list returns 0 for any search value.
    Contract quote: "count the number of occurrences of a number in a given list."
    Input domain: a=[], x=5
    Oracle: An empty list has no elements, so count must be 0.
    Fault hypothesis: A bug that doesn't handle empty lists could raise or return non-zero."""
    result = _case1_frequency([], 5)
    assert result == 0

from solution import frequency as _case2_frequency

def test_frequency_not_found():
    """Test that an element not in the list returns 0.
    Contract quote: "count the number of occurrences of a number in a given list."
    Input domain: a=[1, 3, 5, 7], x=99
    Oracle: 99 does not appear in the list, so count must be 0.
    Fault hypothesis: Off-by-one or wrong comparison would yield non-zero."""
    result = _case2_frequency([1, 3, 5, 7], 99)
    assert result == 0

from solution import frequency as _case3_frequency

def test_frequency_all_match():
    """Test when every element matches the search value.
    Contract quote: "count the number of occurrences of a number in a given list."
    Input domain: a=[4, 4, 4, 4], x=4
    Oracle: All 4 elements equal x, so count must be 4.
    Fault hypothesis: Early exit or skipped iterations would undercount."""
    result = _case3_frequency([4, 4, 4, 4], 4)
    assert result == 4

from solution import frequency as _case4_frequency

def test_frequency_single_element_match():
    """Test a single-element list where the element matches.
    Contract quote: "count the number of occurrences of a number in a given list."
    Input domain: a=[7], x=7
    Oracle: One element equals x, so count must be 1.
    Fault hypothesis: Boundary issue on length-1 lists could return 0 or 2."""
    result = _case4_frequency([7], 7)
    assert result == 1

from solution import frequency as _case5_frequency

def test_frequency_negative_numbers():
    """Test counting with negative numbers.
    Contract quote: "count the number of occurrences of a number in a given list."
    Input domain: a=[-1, -2, -1, 0, -1], x=-1
    Oracle: -1 appears 3 times, so count must be 3.
    Fault hypothesis: Sign handling bugs could miscompare negatives."""
    result = _case5_frequency([-1, -2, -1, 0, -1], -1)
    assert result == 3
