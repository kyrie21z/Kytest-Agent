# Accepted by submit_tests; explanations in testgen_report.json.

"""Unit tests for solution.pancake_sort."""
from solution import pancake_sort as _case0_pancake_sort

def test_pancake_sort_empty_list():
    result = _case0_pancake_sort([])
    assert isinstance(result, list), 'Return value must be a list'
    assert result == [], 'Sorting an empty list should yield an empty list'

"""Unit tests for solution.pancake_sort."""
from solution import pancake_sort as _case1_pancake_sort

def test_pancake_sort_single_element():
    result = _case1_pancake_sort([42])
    assert isinstance(result, list), 'Return value must be a list'
    assert result == [42], 'A single-element list is already sorted'

"""Unit tests for solution.pancake_sort."""
from solution import pancake_sort as _case2_pancake_sort

def test_pancake_sort_two_elements_unsorted():
    result = _case2_pancake_sort([2, 1])
    assert isinstance(result, list), 'Return value must be a list'
    assert result == [1, 2], 'Two-element list [2,1] should sort to [1,2]'

"""Unit tests for solution.pancake_sort."""
from solution import pancake_sort as _case3_pancake_sort

def test_pancake_sort_already_sorted():
    result = _case3_pancake_sort([1, 2, 3, 4, 5])
    assert isinstance(result, list), 'Return value must be a list'
    assert result == [1, 2, 3, 4, 5], 'Already-sorted list should remain unchanged after sorting'

"""Unit tests for solution.pancake_sort."""
from solution import pancake_sort as _case4_pancake_sort

def test_pancake_sort_reverse_sorted():
    result = _case4_pancake_sort([5, 4, 3, 2, 1])
    assert isinstance(result, list), 'Return value must be a list'
    assert result == [1, 2, 3, 4, 5], 'Reverse-sorted list [5,4,3,2,1] should sort to [1,2,3,4,5]'

"""Unit tests for solution.pancake_sort."""
from solution import pancake_sort as _case5_pancake_sort

def test_pancake_sort_duplicates():
    result = _case5_pancake_sort([3, 1, 4, 1, 5, 9, 2, 6, 5])
    assert isinstance(result, list), 'Return value must be a list'
    assert result == [1, 1, 2, 3, 4, 5, 5, 6, 9], 'List with duplicates must be correctly sorted'

"""Unit tests for solution.pancake_sort."""
from solution import pancake_sort as _case6_pancake_sort

def test_pancake_sort_negative_numbers():
    result = _case6_pancake_sort([-3, -1, -4, -1, -5])
    assert isinstance(result, list), 'Return value must be a list'
    assert result == [-5, -4, -3, -1, -1], 'List with negative values must be correctly sorted'
