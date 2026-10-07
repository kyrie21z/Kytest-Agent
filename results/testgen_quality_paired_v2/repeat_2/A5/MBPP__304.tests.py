# Accepted by submit_tests; explanations in testgen_report.json.

"""Unit tests for solution.find_Element."""

def test_no_rotations_returns_original():
    """Contract quote: 'find element at a given index after number of rotations'
    
    Input domain: arr=[10,20,30,40,50], ranges=[], rotations=0, index=2
    
    Independent oracle: With zero rotations, the element at any valid index
    should be unchanged from the original array.
    
    Fault hypothesis: Function might incorrectly modify index even when
    rotations=0, or fail to handle empty ranges list.
    """
    from solution import find_Element
    result = find_Element([10, 20, 30, 40, 50], [], 0, 2)
    assert result == 30

def test_single_rotation_index_at_left_boundary():
    """Contract quote: 'find element at a given index after number of rotations'
    
    Input domain: arr=[1,2,3,4,5], ranges=[[1,3]], rotations=1, index=1
    
    Independent oracle: A right rotation on range [1,3] shifts elements:
    pos 1<-pos3, pos2<-pos1, pos3<-pos2. So original element at index 3
    (value 4) moves to index 1. Expected result: 4.
    
    Fault hypothesis: The left-boundary branch (index==left -> index=right)
    might be missing or use wrong value.
    """
    from solution import find_Element
    result = find_Element([1, 2, 3, 4, 5], [[1, 3]], 1, 1)
    assert result == 4

def test_single_rotation_index_inside_range():
    """Contract quote: 'find element at a given index after number of rotations'
    
    Input domain: arr=[1,2,3,4,5], ranges=[[1,3]], rotations=1, index=2
    
    Independent oracle: Right rotation on [1,3]: element at index 2 comes
    from original index 1 (since index!=left, index=index-1=1). arr[1]=2.
    Expected result: 2.
    
    Fault hypothesis: The else branch (index=index-1) might be off-by-one
    or not execute when it should.
    """
    from solution import find_Element
    result = find_Element([1, 2, 3, 4, 5], [[1, 3]], 1, 2)
    assert result == 2

def test_index_outside_rotation_range():
    """Contract quote: 'find element at a given index after number of rotations'
    
    Input domain: arr=[1,2,3,4,5], ranges=[[1,3]], rotations=1, index=0
    
    Independent oracle: Index 0 is not in range [1,3], so no transformation
    applies. Element remains arr[0]=1. Expected result: 1.
    
    Fault hypothesis: Condition (left<=index and right>=index) might be
    inverted or missing, causing spurious transformations.
    """
    from solution import find_Element
    result = find_Element([1, 2, 3, 4, 5], [[1, 3]], 1, 0)
    assert result == 1

def test_multiple_rotations_chained():
    """Contract quote: 'find element at a given index after number of rotations'
    
    Input domain: arr=[1,2,3,4,5], ranges=[[0,2],[1,4]], rotations=2, index=0
    
    Independent oracle: Process rotations in reverse order (i=1 then i=0):
      i=1: range [1,4], index=0 -> not in range, index stays 0
      i=0: range [0,2], index=0 -> in range, index==left, index=2
    Result: arr[2]=3.
    
    Manual forward check: Apply rot0 [0,2] first -> [3,1,2,4,5]; then rot1 [1,4] -> [3,5,1,2,4]. Index 0 has value 3.
    
    Fault hypothesis: Iteration order might be wrong (forward instead of
    reverse), producing incorrect chained results.
    """
    from solution import find_Element
    result = find_Element([1, 2, 3, 4, 5], [[0, 2], [1, 4]], 2, 0)
    assert result == 3

def test_single_element_array():
    """Contract quote: 'find element at a given index after number of rotations'
    
    Input domain: arr=[42], ranges=[[0,0]], rotations=1, index=0
    
    Independent oracle: Range [0,0] contains only index 0. Since index==left==0,
    index becomes right=0. Result: arr[0]=42. Expected result: 42.
    
    Fault hypothesis: Edge case where left==right might cause infinite loop
    or incorrect handling.
    """
    from solution import find_Element
    result = find_Element([42], [[0, 0]], 1, 0)
    assert result == 42
