# Accepted by submit_tests; explanations in testgen_report.json.

from solution import get_Inv_Count as _case0_get_Inv_Count

def test_empty_array():
    """Verify that an empty array returns zero inversions."""
    result = _case0_get_Inv_Count([])
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 0, f'Expected 0 inversions for empty array, got {result}'

from solution import get_Inv_Count as _case1_get_Inv_Count

def test_single_element():
    """A single-element array has no pairs, hence zero inversions."""
    result = _case1_get_Inv_Count([42])
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 0, f'Expected 0 inversions for single element, got {result}'

from solution import get_Inv_Count as _case2_get_Inv_Count

def test_sorted_array():
    """An already-sorted ascending array has zero inversions."""
    result = _case2_get_Inv_Count([1, 2, 3, 4, 5])
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 0, f'Expected 0 inversions for sorted array, got {result}'

from solution import get_Inv_Count as _case3_get_Inv_Count

def test_reverse_sorted():
    """A fully reversed array has n*(n-1)/2 inversions."""
    arr = [5, 4, 3, 2, 1]
    result = _case3_get_Inv_Count(arr)
    expected = 5 * 4 // 2
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == expected, f'Expected {expected} inversions for reverse-sorted, got {result}'

from solution import get_Inv_Count as _case4_get_Inv_Count

def test_with_duplicates():
    """Duplicates do not form inversions since the condition is strict >."""
    arr = [3, 3, 3]
    result = _case4_get_Inv_Count(arr)
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 0, f'Expected 0 inversions for all-equal array, got {result}'
    arr2 = [2, 1, 3, 1, 2]
    result2 = _case4_get_Inv_Count(arr2)
    expected2 = 4
    assert result2 == expected2, f'Expected {expected2} inversions, got {result2}'
