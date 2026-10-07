# Accepted by submit_tests; explanations in testgen_report.json.

def test_sum_div_six():
    from solution import sum_div
    result = sum_div(6)
    assert result == 6

def test_sum_div_twelve():
    from solution import sum_div
    result = sum_div(12)
    assert result == 16

def test_sum_div_return_type():
    from solution import sum_div
    result = sum_div(6)
    assert isinstance(result, int)

def test_sum_div_prime():
    from solution import sum_div
    result = sum_div(7)
    assert result == 1

def test_sum_div_perfect_number():
    from solution import sum_div
    result = sum_div(28)
    assert result == 28

def test_sum_div_square():
    from solution import sum_div
    result = sum_div(9)
    assert result == 4
