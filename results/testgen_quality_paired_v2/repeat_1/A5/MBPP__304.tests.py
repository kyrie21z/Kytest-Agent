# Accepted by submit_tests; explanations in testgen_report.json.

import solution as _case0_solution

def test_single_rotation_within_range():
    """Right rotation of subarray, index strictly inside range.

    Contract quote: 'Write a python function to find element at a given index
    after number of rotations.'

    Input domain: arr=[1,2,3,4,5], ranges=[(1,3)], rotations=1, index=2.
    The subarray arr[1..3] = [2,3,4] undergoes a right rotation → [4,2,3].
    The full array becomes [1,4,2,3,5]. Element at index 2 is 2.
    Fault hypothesis: detects off-by-one errors in the backward-tracing logic
    (e.g., returning arr[2]=3 instead of arr[1]=2).
    """
    result = _case0_solution.find_Element([1, 2, 3, 4, 5], [(1, 3)], 1, 2)
    assert result == 2

import solution as _case1_solution

def test_single_rotation_at_left_boundary():
    """Index equals left boundary — element wraps from right end.

    Contract quote: 'Write a python function to find element at a given index
    after number of rotations.'

    Input domain: arr=[1,2,3,4,5], ranges=[(1,3)], rotations=1, index=1.
    Right rotation of [2,3,4] → [4,2,3]. Full array: [1,4,2,3,5].
    Element at index 1 is 4 (the former last element of the subarray).
    Fault hypothesis: detects failure to handle index==left specially
    (e.g., decrementing to 0 and returning arr[0]=1 instead of arr[3]=4).
    """
    result = _case1_solution.find_Element([1, 2, 3, 4, 5], [(1, 3)], 1, 1)
    assert result == 4

import solution as _case2_solution

def test_index_outside_rotated_range():
    """Index outside the rotation range should be unaffected.

    Contract quote: 'Write a python function to find element at a given index
    after number of rotations.'

    Input domain: arr=[1,2,3,4,5], ranges=[(1,3)], rotations=1, index=0.
    Index 0 is not in [1,3], so no transformation applies. Returns arr[0]=1.
    Fault hypothesis: detects spurious modification of indices outside range.
    """
    result = _case2_solution.find_Element([1, 2, 3, 4, 5], [(1, 3)], 1, 0)
    assert result == 1

import solution as _case3_solution

def test_zero_rotations():
    """Zero rotations means no changes; return arr[index] directly.

    Contract quote: 'Write a python function to find element at a given index
    after number of rotations.'

    Input domain: arr=[10,20,30,40,50], ranges=[], rotations=0, index=3.
    Loop range(-1,-1,-1) is empty. Returns arr[3]=40.
    Fault hypothesis: detects incorrect handling of rotations=0 (e.g.,
    iterating over empty ranges or raising an error).
    """
    result = _case3_solution.find_Element([10, 20, 30, 40, 50], [], 0, 3)
    assert result == 40

import solution as _case4_solution

def test_two_overlapping_rotations():
    """Two overlapping rotation ranges processed in reverse order.

    Contract quote: 'Write a python function to find element at a given index
    after number of rotations.'

    Input domain: arr=[1,2,3,4,5], ranges=[(0,2),(2,4)], rotations=2, index=1.
    Forward simulation:
      Step 0: rotate [1,2,3]->[3,1,2], array=[3,1,2,4,5]
      Step 1: rotate [2,4,5]->[5,2,4], array=[3,1,5,2,4]
    Element at index 1 is 1.
    Backward trace: index=1; i=1: [2,4] doesn't cover 1; i=0: [0,2] covers 1,
    index!=0 -> index=0. Return arr[0]=1.
    Fault hypothesis: detects incorrect reverse-order processing or overlap logic.
    """
    result = _case4_solution.find_Element([1, 2, 3, 4, 5], [(0, 2), (2, 4)], 2, 1)
    assert result == 1

import solution as _case5_solution

def test_single_element_array():
    """Single-element array: rotation of length-1 range is identity.

    Contract quote: 'Write a python function to find element at a given index
    after number of rotations.'

    Input domain: arr=[42], ranges=[(0,0)], rotations=1, index=0.
    left=0, right=0, index=0. index==left, so index=right=0. Returns arr[0]=42.
    Fault hypothesis: detects degenerate range [k,k] producing wrong result.
    """
    result = _case5_solution.find_Element([42], [(0, 0)], 1, 0)
    assert result == 42
