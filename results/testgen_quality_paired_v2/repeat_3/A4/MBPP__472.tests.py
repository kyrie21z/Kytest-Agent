# Accepted by submit_tests; explanations in testgen_report.json.

from solution import check_Consecutive as _case0_check_Consecutive

def test_consecutive_positive():
    """Test that a straightforward consecutive positive integer list returns True.
    
    Contract quote: "Write a python function to check whether the given list
    contains consecutive numbers or not."
    Input domain: l = [1, 2, 3, 4, 5]
    Oracle: sorted([1,2,3,4,5]) == [1,2,3,4,5]; range(1,6) == [1,2,3,4,5]; match -> True.
    Fault hypothesis: If the function incorrectly handles basic consecutive sequences,
    e.g., by checking adjacency instead of full range coverage, it would fail here."""
    assert _case0_check_Consecutive([1, 2, 3, 4, 5]) is True

from solution import check_Consecutive as _case1_check_Consecutive

def test_non_consecutive_gaps():
    """Test that a list with gaps between values returns False.
    
    Contract quote: "Write a python function to check whether the given list
    contains consecutive numbers or not."
    Input domain: l = [1, 3, 5, 7]
    Oracle: sorted([1,3,5,7]) == [1,3,5,7]; range(1,8) == [1,2,3,4,5,6,7]; mismatch -> False.
    Fault hypothesis: If the function uses a wrong comparison like len-based check,
    it might incorrectly classify sparse sequences."""
    assert _case1_check_Consecutive([1, 3, 5, 7]) is False

from solution import check_Consecutive as _case2_check_Consecutive

def test_two_elements_consecutive():
    """Test two-element consecutive pair returns True.
    
    Contract quote: "Write a python function to check whether the given list
    contains consecutive numbers or not."
    Input domain: l = [10, 11]
    Oracle: sorted([10,11]) == [10,11]; range(10,12) == [10,11]; match -> True.
    Fault hypothesis: Off-by-one error in range upper bound (using max(l) instead of max(l)+1)
    would produce range(10,11)=[10] which mismatches."""
    assert _case2_check_Consecutive([10, 11]) is True

from solution import check_Consecutive as _case3_check_Consecutive

def test_single_element():
    """Test that a single-element list is trivially consecutive.
    
    Contract quote: "Write a python function to check whether the given list
    contains consecutive numbers or not."
    Input domain: l = [42]
    Oracle: sorted([42]) == [42]; range(42,43) == [42]; match -> True.
    Fault hypothesis: Function might require at least 2 elements and return False
    for single-element lists."""
    assert _case3_check_Consecutive([42]) is True

from solution import check_Consecutive as _case4_check_Consecutive

def test_duplicates_in_range():
    """Test that duplicate values within a consecutive range return False.
    
    Contract quote: "Write a python function to check whether the given list
    contains consecutive numbers or not."
    Input domain: l = [1, 2, 2, 3]
    Oracle: sorted([1,2,2,3]) == [1,2,2,3]; range(1,4) == [1,2,3]; mismatch -> False.
    Fault hypothesis: Function might ignore duplicates and only check min/max span."""
    assert _case4_check_Consecutive([1, 2, 2, 3]) is False

from solution import check_Consecutive as _case5_check_Consecutive

def test_negative_consecutive():
    """Test negative consecutive integers work correctly.
    
    Contract quote: "Write a python function to check whether the given list
    contains consecutive numbers or not."
    Input domain: l = [-3, -2, -1, 0, 1]
    Oracle: sorted([-3,-2,-1,0,1]) == [-3,-2,-1,0,1]; range(-3,2) == [-3,-2,-1,0,1]; match -> True.
    Fault hypothesis: Function might mishandle negative numbers in sorting or range generation."""
    assert _case5_check_Consecutive([-3, -2, -1, 0, 1]) is True
