# Accepted by submit_tests; explanations in testgen_report.json.

from solution import get_Inv_Count as _case0_get_Inv_Count

def test_empty_array():
    """Contract: empty input has no pairs, so zero inversions."""
    result = _case0_get_Inv_Count([])
    assert isinstance(result, int), 'Return type must be int'
    assert result == 0, 'Empty array should have zero inversions'

from solution import get_Inv_Count as _case1_get_Inv_Count

def test_single_element():
    """Contract: single element has no pairs, so zero inversions."""
    result = _case1_get_Inv_Count([42])
    assert isinstance(result, int)
    assert result == 0, 'Single-element array should have zero inversions'

from solution import get_Inv_Count as _case2_get_Inv_Count

def test_already_sorted():
    """Contract: sorted ascending means no i<j with arr[i]>arr[j]."""
    result = _case2_get_Inv_Count([1, 2, 3, 4, 5])
    assert isinstance(result, int)
    assert result == 0, 'Sorted array should have zero inversions'

from solution import get_Inv_Count as _case3_get_Inv_Count

def test_reverse_sorted():
    """Contract: reverse-sorted array of length n has n*(n-1)/2 inversions."""
    result = _case3_get_Inv_Count([5, 4, 3, 2, 1])
    assert isinstance(result, int)
    expected = 5 * 4 // 2
    assert result == expected, f'Reverse sorted [5,4,3,2,1] should have {expected} inversions, got {result}'

from solution import get_Inv_Count as _case4_get_Inv_Count

def test_two_elements_inverted():
    """Contract: two-element reversed array has exactly one inversion."""
    result = _case4_get_Inv_Count([2, 1])
    assert isinstance(result, int)
    assert result == 1, '[2,1] should have exactly 1 inversion'

from solution import get_Inv_Count as _case5_get_Inv_Count

def test_with_duplicates():
    """Contract: equal elements do NOT form inversions (strict >)."""
    result = _case5_get_Inv_Count([2, 1, 1])
    assert isinstance(result, int)
    assert result == 2, f'[2,1,1] should have 2 inversions, got {result}'
