# Accepted by submit_tests; explanations in testgen_report.json.

def test_basic_increasing():
    from solution import max_product
    assert max_product([1, 2, 3]) == 6

def test_single_element():
    from solution import max_product
    assert max_product([7]) == 7

def test_decreasing_sequence():
    from solution import max_product
    assert max_product([5, 3, 1]) == 5

def test_mixed_with_local_increase():
    from solution import max_product
    assert max_product([2, 1, 4, 3, 5]) == 15

def test_negative_numbers():
    from solution import max_product
    assert max_product([-2, -3, -1]) == 3

def test_all_same_elements():
    from solution import max_product
    assert max_product([4, 4, 4]) == 64
