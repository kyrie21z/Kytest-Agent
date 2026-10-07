# Accepted by submit_tests; explanations in testgen_report.json.

from solution import check_Consecutive as _case0_check_Consecutive

def test_consecutive_basic():
    """Test basic consecutive positive integers."""
    assert _case0_check_Consecutive([1, 2, 3]) is True

from solution import check_Consecutive as _case1_check_Consecutive

def test_consecutive_unsorted():
    """Test that unsorted consecutive integers are detected as consecutive."""
    assert _case1_check_Consecutive([3, 1, 2]) is True

from solution import check_Consecutive as _case2_check_Consecutive

def test_non_consecutive_gap():
    """Test that a gap in sequence is detected as non-consecutive."""
    assert _case2_check_Consecutive([1, 3, 4]) is False

from solution import check_Consecutive as _case3_check_Consecutive

def test_single_element():
    """Test that a single-element list is considered consecutive."""
    assert _case3_check_Consecutive([42]) is True

from solution import check_Consecutive as _case4_check_Consecutive

def test_negative_consecutive():
    """Test consecutive negative integers including zero."""
    assert _case4_check_Consecutive([-2, -1, 0, 1]) is True

from solution import check_Consecutive as _case5_check_Consecutive

def test_duplicates_not_consecutive():
    """Test that duplicate values make the list non-consecutive."""
    assert _case5_check_Consecutive([1, 2, 2, 3]) is False
