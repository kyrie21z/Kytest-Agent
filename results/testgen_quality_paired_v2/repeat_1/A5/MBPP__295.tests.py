# Accepted by submit_tests; explanations in testgen_report.json.

def test_sum_div_perfect_number():
    """Test that sum_div(6) returns 6, since 6 is a perfect number
    whose proper divisors are 1, 2, 3 and their sum is 6."""
    from solution import sum_div
    result = sum_div(6)
    assert result == 6, f'Expected 6 for perfect number 6, got {result}'

def test_sum_div_prime_number():
    """Test that sum_div(7) returns 1, since 7 is prime and its only
    proper divisor is 1."""
    from solution import sum_div
    result = sum_div(7)
    assert result == 1, f'Expected 1 for prime 7, got {result}'

def test_sum_div_composite_multiple_divisors():
    """Test that sum_div(12) returns 16. Proper divisors of 12 are
    1, 2, 3, 4, 6. Sum = 1 + 2 + 3 + 4 + 6 = 16."""
    from solution import sum_div
    result = sum_div(12)
    assert result == 16, f'Expected 16 for 12, got {result}'

def test_sum_div_return_type_int():
    """Verify that sum_div returns an int for valid inputs."""
    from solution import sum_div
    result = sum_div(12)
    assert isinstance(result, int), f'Expected int, got {type(result).__name__}'

def test_sum_div_small_numbers():
    """Test boundary values near 1.
    sum_div(1) -> 1 (loop range(2,1) is empty, divisors=[1])
    sum_div(2) -> 1 (only proper divisor is 1)
    sum_div(4) -> 3 (proper divisors: 1, 2; sum = 3)"""
    from solution import sum_div
    assert sum_div(1) == 1, 'sum_div(1) should be 1'
    assert sum_div(2) == 1, 'sum_div(2) should be 1 (prime)'
    assert sum_div(4) == 3, 'sum_div(4) should be 3 (divisors 1+2)'

def test_sum_div_larger_composite():
    """Test sum_div(28) returns 28. 28 is also a perfect number.
    Proper divisors: 1, 2, 4, 7, 14. Sum = 1+2+4+7+14 = 28."""
    from solution import sum_div
    result = sum_div(28)
    assert result == 28, f'Expected 28 for perfect number 28, got {result}'
