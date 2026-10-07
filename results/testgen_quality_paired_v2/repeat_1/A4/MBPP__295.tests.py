# Accepted by submit_tests; explanations in testgen_report.json.

def test_sum_div_composite():
    from solution import sum_div
    assert sum_div(6) == 6
    assert sum_div(12) == 16
    assert sum_div(28) == 28

def test_sum_div_prime():
    from solution import sum_div
    assert sum_div(2) == 1
    assert sum_div(3) == 1
    assert sum_div(7) == 1
    assert sum_div(13) == 1
    assert sum_div(97) == 1

def test_sum_div_one():
    from solution import sum_div
    assert sum_div(1) == 1

def test_sum_div_even_odd():
    from solution import sum_div
    assert sum_div(4) == 3
    assert sum_div(9) == 4
    assert sum_div(10) == 8
    assert sum_div(15) == 9

def test_sum_div_return_type():
    from solution import sum_div
    result = sum_div(6)
    assert isinstance(result, int)
    result = sum_div(1)
    assert isinstance(result, int)
    result = sum_div(100)
    assert isinstance(result, int)

def test_sum_div_perfect_squares():
    from solution import sum_div
    assert sum_div(16) == 15
    assert sum_div(25) == 6
    assert sum_div(36) == 55

def test_sum_div_does_not_include_self():
    from solution import sum_div
    assert sum_div(4) < 4
    assert sum_div(6) == 6
    assert sum_div(8) < 8
    assert sum_div(8) == 7

def test_sum_div_abundant_numbers():
    from solution import sum_div
    assert sum_div(12) == 16
    assert sum_div(18) == 21
    assert sum_div(20) == 22

def test_sum_div_deficient_numbers():
    from solution import sum_div
    assert sum_div(10) == 8
    assert sum_div(14) == 10
    assert sum_div(22) == 14

def test_sum_div_larger_composite():
    from solution import sum_div
    assert sum_div(100) == 117
    assert sum_div(49) == 8
    assert sum_div(50) == 43

def test_sum_div_zero():
    from solution import sum_div
    assert sum_div(0) == 1

def test_sum_div_negative():
    from solution import sum_div
    assert sum_div(-1) == 1
    assert sum_div(-5) == 1

def test_sum_div_small_primes_boundary():
    from solution import sum_div
    assert sum_div(2) == 1
    assert sum_div(3) == 1
    assert sum_div(4) == 3
