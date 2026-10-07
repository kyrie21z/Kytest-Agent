# Accepted by submit_tests; explanations in testgen_report.json.

from solution import largest_neg as _case0_largest_neg

def test_largest_neg_single_negative():
    '''Contract: "find the largest negative number from the given list."'''
    result = _case0_largest_neg([-7])
    assert isinstance(result, int)
    assert result == -7

from solution import largest_neg as _case1_largest_neg

def test_largest_neg_all_positive():
    '''Contract: "find the largest negative number from the given list."'''
    result = _case1_largest_neg([1, 2, 3, 4])
    assert isinstance(result, int)

from solution import largest_neg as _case2_largest_neg

def test_largest_neg_duplicates():
    '''Contract: "find the largest negative number from the given list."'''
    result = _case2_largest_neg([-4, -4, -4])
    assert isinstance(result, int)
    assert result == -4
