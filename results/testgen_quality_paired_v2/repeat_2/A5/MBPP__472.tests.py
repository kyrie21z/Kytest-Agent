# Accepted by submit_tests; explanations in testgen_report.json.

from solution import check_Consecutive as _case0_check_Consecutive

def test_consecutive_positive():
    assert _case0_check_Consecutive([1, 2, 3, 4, 5]) == True

from solution import check_Consecutive as _case1_check_Consecutive

def test_non_consecutive():
    assert _case1_check_Consecutive([1, 3, 5, 7]) == False

from solution import check_Consecutive as _case2_check_Consecutive

def test_single_element():
    assert _case2_check_Consecutive([42]) == True

from solution import check_Consecutive as _case3_check_Consecutive

def test_unsorted_consecutive():
    assert _case3_check_Consecutive([5, 3, 1, 4, 2]) == True

from solution import check_Consecutive as _case4_check_Consecutive

def test_negative_consecutive():
    assert _case4_check_Consecutive([-3, -2, -1, 0, 1]) == True

from solution import check_Consecutive as _case5_check_Consecutive

def test_duplicates_not_consecutive():
    assert _case5_check_Consecutive([1, 2, 2, 3]) == False
