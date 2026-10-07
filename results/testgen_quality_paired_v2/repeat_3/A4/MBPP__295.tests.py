# Accepted by submit_tests; explanations in testgen_report.json.

def test_sum_div_composite():
    from solution import sum_div
    assert sum_div(12) == 16

def test_sum_div_prime():
    from solution import sum_div
    assert sum_div(7) == 1
    assert sum_div(13) == 1

def test_sum_div_perfect_number():
    from solution import sum_div
    assert sum_div(6) == 6
    assert sum_div(28) == 28

def test_sum_div_edge_cases():
    from solution import sum_div
    assert sum_div(1) == 1
    assert sum_div(0) == 1
    assert sum_div(-5) == 1

def test_sum_div_return_type():
    from solution import sum_div
    assert isinstance(sum_div(12), int)
    assert isinstance(sum_div(7), int)
    assert isinstance(sum_div(1), int)

def test_sum_div_square_number():
    from solution import sum_div
    assert sum_div(9) == 4
    assert sum_div(16) == 15
