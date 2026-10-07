# Accepted by submit_tests; explanations in testgen_report.json.

def test_sum_div_perfect_number():
    """Test sum_div with a perfect number (6).
    Contract quote: "return the sum of all divisors of a number"
    Input domain: number = 6 (positive integer)
    Oracle: Proper divisors of 6 are 1, 2, 3. Their sum is 6.
    Fault hypothesis: If the function incorrectly includes the number itself
    or misses a divisor, the result would differ from 6."""
    from solution import sum_div
    result = sum_div(6)
    assert result == 6

def test_sum_div_prime():
    """Test sum_div with a prime number (7).
    Contract quote: "return the sum of all divisors of a number"
    Input domain: number = 7 (prime)
    Oracle: A prime number has only one proper divisor: 1. Sum = 1.
    Fault hypothesis: If the function fails to handle primes correctly,
    e.g., returns 0 or includes the number itself, assertion fails."""
    from solution import sum_div
    result = sum_div(7)
    assert result == 1

def test_sum_div_composite():
    """Test sum_div with a composite number (12).
    Contract quote: "return the sum of all divisors of a number"
    Input domain: number = 12
    Oracle: Proper divisors of 12 are 1, 2, 3, 4, 6. Sum = 16.
    Fault hypothesis: Missing any divisor or including 12 itself
    would produce an incorrect sum."""
    from solution import sum_div
    result = sum_div(12)
    assert result == 16

def test_sum_div_return_type():
    """Test that sum_div returns an integer for valid inputs.
    Contract quote: "return the sum of all divisors of a number"
    Input domain: number = 10 (positive integer)
    Oracle: The sum of integer divisors must be an integer.
    Fault hypothesis: If the function returns a float or None,
    the type check catches it."""
    from solution import sum_div
    result = sum_div(10)
    assert isinstance(result, int)
