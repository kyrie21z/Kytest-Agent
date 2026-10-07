# Accepted by submit_tests; explanations in testgen_report.json.

def test_consecutive_positive():
    from solution import check_Consecutive
    assert check_Consecutive([1, 2, 3, 4, 5]) is True

def test_consecutive_unsorted():
    from solution import check_Consecutive
    assert check_Consecutive([3, 1, 2, 5, 4]) is True

def test_consecutive_negative():
    from solution import check_Consecutive
    assert check_Consecutive([-2, -1, 0, 1, 2]) is True

def test_single_element():
    from solution import check_Consecutive
    assert check_Consecutive([42]) is True

def test_not_consecutive_gap():
    from solution import check_Consecutive
    assert check_Consecutive([1, 2, 4, 5]) is False

def test_duplicates_not_consecutive():
    from solution import check_Consecutive
    assert check_Consecutive([1, 2, 2, 3]) is False
