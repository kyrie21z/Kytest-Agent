# Accepted by submit_tests; explanations in testgen_report.json.

"""Test that an empty array returns 0 inversions."""
from solution import get_Inv_Count as _case0_get_Inv_Count

def test_empty_array():
    result = _case0_get_Inv_Count([])
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 0, f'Expected 0 inversions for empty array, got {result}'

"""Test that a single-element array returns 0 inversions."""
from solution import get_Inv_Count as _case1_get_Inv_Count

def test_single_element():
    result = _case1_get_Inv_Count([5])
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 0, f'Expected 0 inversions for single element, got {result}'

"""Test that a sorted array returns 0 inversions."""
from solution import get_Inv_Count as _case2_get_Inv_Count

def test_already_sorted():
    result = _case2_get_Inv_Count([1, 2, 3, 4, 5])
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 0, f'Expected 0 inversions for sorted array, got {result}'

"""Test that a reverse-sorted array of length 5 returns 10 inversions."""
from solution import get_Inv_Count as _case3_get_Inv_Count

def test_reverse_sorted():
    result = _case3_get_Inv_Count([5, 4, 3, 2, 1])
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 10, f'Expected 10 inversions for reverse-sorted array, got {result}'

"""Test that an array of all identical elements returns 0 inversions."""
from solution import get_Inv_Count as _case4_get_Inv_Count

def test_all_same_elements():
    result = _case4_get_Inv_Count([4, 4, 4, 4])
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 0, f'Expected 0 inversions for all-same array, got {result}'

"""Test that equal elements are not counted as inversions."""
from solution import get_Inv_Count as _case5_get_Inv_Count

def test_with_duplicates():
    result = _case5_get_Inv_Count([3, 1, 3, 2, 1])
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 6, f'Expected 6 inversions, got {result}'
