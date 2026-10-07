# Accepted by submit_tests; explanations in testgen_report.json.

from solution import get_Inv_Count as _case0_get_Inv_Count

def test_empty_array():
    """Contract: an empty array has no pairs, so zero inversions."""
    result = _case0_get_Inv_Count([])
    assert result == 0
    assert isinstance(result, int)

from solution import get_Inv_Count as _case1_get_Inv_Count

def test_single_element():
    """A one-element array has no pairs, so zero inversions."""
    result = _case1_get_Inv_Count([42])
    assert result == 0
    assert isinstance(result, int)

from solution import get_Inv_Count as _case2_get_Inv_Count

def test_sorted_array():
    """An already-sorted ascending array has no inversions."""
    result = _case2_get_Inv_Count([1, 2, 3, 4, 5])
    assert result == 0
    assert isinstance(result, int)

from solution import get_Inv_Count as _case3_get_Inv_Count

def test_reverse_sorted():
    """A fully reversed array has maximum inversions: n*(n-1)/2."""
    result = _case3_get_Inv_Count([3, 2, 1])
    assert result == 3
    assert isinstance(result, int)
    result2 = _case3_get_Inv_Count([5, 4, 3, 2, 1])
    assert result2 == 10

from solution import get_Inv_Count as _case4_get_Inv_Count

def test_two_elements_inverted():
    """Two-element array with inversion: [2,1] has exactly 1 inversion."""
    result = _case4_get_Inv_Count([2, 1])
    assert result == 1
    assert isinstance(result, int)
    result2 = _case4_get_Inv_Count([1, 2])
    assert result2 == 0

from solution import get_Inv_Count as _case5_get_Inv_Count

def test_mixed_with_duplicates():
    """Mixed array: [3,1,2] has inversions (3,1) and (3,2) = 2.
       Duplicates do NOT count: [2,2,1] has (0,2) and (1,2) = 2 inversions."""
    result = _case5_get_Inv_Count([3, 1, 2])
    assert result == 2
    assert isinstance(result, int)
    result2 = _case5_get_Inv_Count([2, 2, 1])
    assert result2 == 2
    result3 = _case5_get_Inv_Count([5, 5, 5, 5])
    assert result3 == 0
