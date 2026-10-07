# Accepted by submit_tests; explanations in testgen_report.json.

def test_basic_positive_odds():
    from solution import double_the_difference
    assert double_the_difference([1, 3, 2, 0]) == 10

def test_empty_list():
    from solution import double_the_difference
    assert double_the_difference([]) == 0

def test_negative_numbers_excluded():
    from solution import double_the_difference
    assert double_the_difference([-1, -2, 0]) == 0

def test_float_values_excluded():
    from solution import double_the_difference
    assert double_the_difference([1, 2.0, 3]) == 10

def test_single_large_odd():
    from solution import double_the_difference
    assert double_the_difference([9]) == 81

def test_all_evens_return_zero():
    from solution import double_the_difference
    assert double_the_difference([2, 4, 6, 8]) == 0
