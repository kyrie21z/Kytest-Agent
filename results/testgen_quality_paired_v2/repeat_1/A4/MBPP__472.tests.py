# Accepted by submit_tests; explanations in testgen_report.json.

from solution import check_Consecutive as _case0_check_Consecutive

def test_consecutive_positive():
    """Test basic consecutive positive integers in order."""
    assert _case0_check_Consecutive([1, 2, 3, 4, 5]) is True

from solution import check_Consecutive as _case1_check_Consecutive

def test_non_consecutive():
    """Test list with gaps between elements."""
    assert _case1_check_Consecutive([1, 3, 5]) is False

from solution import check_Consecutive as _case2_check_Consecutive

def test_unsorted_consecutive():
    """Test consecutive numbers given in random order."""
    assert _case2_check_Consecutive([3, 1, 2]) is True

from solution import check_Consecutive as _case3_check_Consecutive

def test_single_element():
    """Test a single-element list is trivially consecutive."""
    assert _case3_check_Consecutive([7]) is True

from solution import check_Consecutive as _case4_check_Consecutive

def test_with_duplicates():
    """Test that duplicate values break consecutiveness."""
    assert _case4_check_Consecutive([1, 2, 2, 3]) is False

from solution import check_Consecutive as _case5_check_Consecutive

def test_negative_consecutive():
    """Test consecutive integers including negatives."""
    assert _case5_check_Consecutive([-2, -1, 0, 1]) is True
