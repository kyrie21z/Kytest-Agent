# Accepted by submit_tests; explanations in testgen_report.json.

from solution import get_Inv_Count as _case0_get_Inv_Count

def test_empty_array():
    """Contract: count inversions in an array.
    An empty array has no pairs, so inversions must be 0."""
    result = _case0_get_Inv_Count([])
    assert isinstance(result, int), 'Return value should be an integer'
    assert result == 0, 'Empty array should have zero inversions'

from solution import get_Inv_Count as _case1_get_Inv_Count

def test_single_element():
    """A single-element array has no pairs, hence zero inversions."""
    result = _case1_get_Inv_Count([42])
    assert isinstance(result, int), 'Return value should be an integer'
    assert result == 0, 'Single element array should have zero inversions'

from solution import get_Inv_Count as _case2_get_Inv_Count

def test_sorted_array():
    """A strictly increasing array has no inversions because every
    earlier element is smaller than every later element."""
    result = _case2_get_Inv_Count([1, 2, 3, 4, 5])
    assert isinstance(result, int), 'Return value should be an integer'
    assert result == 0, 'Sorted array should have zero inversions'

from solution import get_Inv_Count as _case3_get_Inv_Count

def test_reverse_sorted():
    """A strictly decreasing array of length n has n*(n-1)//2 inversions,
    since every pair (i, j) with i < j satisfies arr[i] > arr[j]."""
    arr = [5, 4, 3, 2, 1]
    n = len(arr)
    expected = n * (n - 1) // 2
    result = _case3_get_Inv_Count(arr)
    assert isinstance(result, int), 'Return value should be an integer'
    assert result == expected, f'Reverse sorted {arr} should have {expected} inversions, got {result}'

from solution import get_Inv_Count as _case4_get_Inv_Count

def test_with_duplicates():
    """Duplicates do not form inversions because the condition is strict:
    arr[i] > arr[j]. Equal values are not counted."""
    arr = [3, 3, 3]
    result = _case4_get_Inv_Count(arr)
    assert isinstance(result, int), 'Return value should be an integer'
    assert result == 0, 'Array of identical elements should have zero inversions'
    arr2 = [2, 1, 2, 1]
    result2 = _case4_get_Inv_Count(arr2)
    assert result2 == 3, f'Expected 3 inversions for {arr2}, got {result2}'

from solution import get_Inv_Count as _case5_get_Inv_Count

def test_mixed_case():
    """Manual enumeration of inversions for a non-trivial array."""
    arr = [1, 3, 5, 2, 4, 6]
    result = _case5_get_Inv_Count(arr)
    assert isinstance(result, int), 'Return value should be an integer'
    assert result == 3, f'Expected 3 inversions for {arr}, got {result}'
