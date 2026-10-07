# Accepted by submit_tests; explanations in testgen_report.json.

"""Test wrap-around when index equals left boundary."""
from solution import find_Element as _case0_find_Element

def test_single_rotation_left_boundary():
    """Quote: 'Write a python function to find element at a given index after number of rotations.'

    Input domain: arr=[1,2,3,4,5], ranges=[[1,3]], rotations=1, index=1
    Oracle: A left rotation on range [1,3] shifts elements left; the element at
    position 1 after rotation comes from position 3 (wraps). Expected: arr[3]=4.
    Fault hypothesis: Function fails to handle the wrap-around case where
    index equals left boundary, returning wrong element instead of arr[right].
    """
    result = _case0_find_Element([1, 2, 3, 4, 5], [[1, 3]], 1, 1)
    assert result == 4

"""Test middle-of-range index shift."""
from solution import find_Element as _case1_find_Element

def test_single_rotation_middle_index():
    """Quote: 'Write a python function to find element at a given index after number of rotations.'

    Input domain: arr=[1,2,3,4,5], ranges=[[1,3]], rotations=1, index=2
    Oracle: After left rotation on [1,3], index 2 is inside range but not at left,
    so index becomes index-1=1. Expected: arr[1]=2.
    Fault hypothesis: Off-by-one error in computing index transformation for
    middle-of-range indices.
    """
    result = _case1_find_Element([1, 2, 3, 4, 5], [[1, 3]], 1, 2)
    assert result == 2

"""Test that index outside range is unaffected."""
from solution import find_Element as _case2_find_Element

def test_index_outside_range_no_effect():
    """Quote: 'Write a python function to find element at a given index after number of rotations.'

    Input domain: arr=[1,2,3,4,5], ranges=[[1,3]], rotations=1, index=0
    Oracle: Index 0 is outside range [1,3], so no rotation applies.
    Expected: arr[0]=1 (unchanged).
    Fault hypothesis: Function incorrectly modifies index even when it falls
    outside the rotation range.
    """
    result = _case2_find_Element([1, 2, 3, 4, 5], [[1, 3]], 1, 0)
    assert result == 1

"""Test zero rotations returns original element."""
from solution import find_Element as _case3_find_Element

def test_zero_rotations_returns_original():
    """Quote: 'Write a python function to find element at a given index after number of rotations.'

    Input domain: arr=[10,20,30,40,50], ranges=[], rotations=0, index=2
    Oracle: With 0 rotations, no transformation occurs. Expected: arr[2]=30.
    Fault hypothesis: Function performs unintended transformations when
    rotations=0, returning wrong element.
    """
    result = _case3_find_Element([10, 20, 30, 40, 50], [], 0, 2)
    assert result == 30

"""Test multiple overlapping rotations processed in reverse order."""
from solution import find_Element as _case4_find_Element

def test_multiple_overlapping_rotations():
    """Quote: 'Write a python function to find element at a given index after number of rotations.'

    Input domain: arr=[1,2,3,4,5], ranges=[[1,3],[2,4]], rotations=2, index=1
    Oracle: Process rotations in reverse order (i=1 then i=0).
      Step i=1: range [2,4], index=1 is outside [2,4], no change. index=1.
      Step i=0: range [1,3], index=1==left=1, so index=right=3.
      Return arr[3]=4.
    Fault hypothesis: Function processes rotations in wrong order (forward
    instead of reverse), producing incorrect result.
    """
    result = _case4_find_Element([1, 2, 3, 4, 5], [[1, 3], [2, 4]], 2, 1)
    assert result == 4

"""Test complex chained rotations with three overlapping ranges."""
from solution import find_Element as _case5_find_Element

def test_chained_rotations_complex():
    """Quote: 'Write a python function to find element at a given index after number of rotations.'

    Input domain: arr=[1,2,3,4,5,6], ranges=[[0,2],[1,4],[3,5]], rotations=3, index=1
    Oracle: Process in reverse order (i=2,1,0).
      Step i=2: range [3,5], index=1 outside [3,5], no change. index=1.
      Step i=1: range [1,4], index=1==left=1, so index=right=4. index=4.
      Step i=0: range [0,2], index=4 outside [0,2], no change. index=4.
      Return arr[4]=5.
    Fault hypothesis: Function processes rotations forward instead of reverse,
    yielding a different (incorrect) chain of index transformations.
    """
    result = _case5_find_Element([1, 2, 3, 4, 5, 6], [[0, 2], [1, 4], [3, 5]], 3, 1)
    assert result == 5
