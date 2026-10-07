# Accepted by submit_tests; explanations in testgen_report.json.

from solution import check_Consecutive as _case0_check_Consecutive

def test_consecutive_sorted_positive():
    """Verify basic consecutive positive integers return True.
    
    Contract quote: "check whether the given list contains consecutive numbers or not."
    Input domain: l = [1, 2, 3, 4, 5] — five distinct consecutive positive integers.
    Oracle: sorted([1,2,3,4,5]) == [1,2,3,4,5] and range(1,6) == [1,2,3,4,5], so equal.
    Fault hypothesis: A bug that only checks adjacent pairs without verifying full coverage
    would miss this case; also catches off-by-one errors in range bounds."""
    result = _case0_check_Consecutive([1, 2, 3, 4, 5])
    assert isinstance(result, bool)
    assert result is True

from solution import check_Consecutive as _case1_check_Consecutive

def test_consecutive_unsorted():
    """Verify that order does not matter for consecutive detection.
    
    Contract quote: "check whether the given list contains consecutive numbers or not."
    Input domain: l = [3, 1, 2, 5, 4] — same set as above but shuffled.
    Oracle: After sorting -> [1,2,3,4,5]; range(1,6) -> [1,2,3,4,5]; equal => True.
    Fault hypothesis: If the function checked adjacency without sorting first,
    it would incorrectly return False for unsorted consecutive sequences."""
    result = _case1_check_Consecutive([3, 1, 2, 5, 4])
    assert isinstance(result, bool)
    assert result is True

from solution import check_Consecutive as _case2_check_Consecutive

def test_not_consecutive_gap():
    """Verify that a gap in the sequence returns False.
    
    Contract quote: "check whether the given list contains consecutive numbers or not."
    Input domain: l = [1, 2, 4, 5] — missing 3 between 2 and 4.
    Oracle: sorted -> [1,2,4,5]; range(1,6) -> [1,2,3,4,5]; lengths differ => False.
    Fault hypothesis: A function that only checks pairwise differences might miss
    the gap if it doesn't verify the full range covers all expected values."""
    result = _case2_check_Consecutive([1, 2, 4, 5])
    assert isinstance(result, bool)
    assert result is False

from solution import check_Consecutive as _case3_check_Consecutive

def test_single_element():
    """Verify a single-element list is considered consecutive.
    
    Contract quote: "check whether the given list contains consecutive numbers or not."
    Input domain: l = [42] — one element.
    Oracle: sorted([42])=[42]; range(42,43)=[42]; equal => True.
    Fault hypothesis: An implementation requiring len>=2 would incorrectly reject singles."""
    result = _case3_check_Consecutive([42])
    assert isinstance(result, bool)
    assert result is True

from solution import check_Consecutive as _case4_check_Consecutive

def test_with_duplicates():
    """Verify duplicates break consecutiveness.
    
    Contract quote: "check whether the given list contains consecutive numbers or not."
    Input domain: l = [1, 2, 2, 3] — duplicate 2.
    Oracle: sorted -> [1,2,2,3]; range(1,4) -> [1,2,3]; lengths differ (4 vs 3) => False.
    Fault hypothesis: Using a set-based approach without checking count would miss duplicates."""
    result = _case4_check_Consecutive([1, 2, 2, 3])
    assert isinstance(result, bool)
    assert result is False

from solution import check_Consecutive as _case5_check_Consecutive

def test_negative_consecutive():
    """Verify consecutive detection works with negative numbers.
    
    Contract quote: "check whether the given list contains consecutive numbers or not."
    Input domain: l = [-3, -2, -1, 0, 1] — consecutive across zero.
    Oracle: sorted -> [-3,-2,-1,0,1]; range(-3,2) -> [-3,-2,-1,0,1]; equal => True.
    Fault hypothesis: Some implementations may mishandle negative ranges or sign flipping."""
    result = _case5_check_Consecutive([-3, -2, -1, 0, 1])
    assert isinstance(result, bool)
    assert result is True
