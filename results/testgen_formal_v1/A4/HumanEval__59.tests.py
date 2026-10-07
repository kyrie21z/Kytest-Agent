# Accepted by submit_tests; explanations in testgen_report.json.

def test_largest_prime_factor_small_composite():
    """Test smallest composite number 6 = 2 * 3, largest prime factor is 3."""
    from solution import largest_prime_factor
    assert largest_prime_factor(6) == 3

def test_largest_prime_factor_power_of_two():
    """Test 2^10 = 1024, only prime factor is 2."""
    from solution import largest_prime_factor
    assert largest_prime_factor(1024) == 2

def test_largest_prime_factor_product_two_primes():
    """Test 14 = 2 * 7, largest prime factor is 7."""
    from solution import largest_prime_factor
    assert largest_prime_factor(14) == 7

def test_largest_prime_factor_square_of_prime():
    """Test 121 = 11^2, largest prime factor is 11."""
    from solution import largest_prime_factor
    assert largest_prime_factor(121) == 11

def test_largest_prime_factor_three_distinct_primes():
    """Test 1001 = 7 * 11 * 13, largest prime factor is 13."""
    from solution import largest_prime_factor
    assert largest_prime_factor(1001) == 13

def test_largest_prime_factor_return_type():
    """Verify return type is int for known inputs."""
    from solution import largest_prime_factor
    result_6 = largest_prime_factor(6)
    result_14 = largest_prime_factor(14)
    result_1001 = largest_prime_factor(1001)
    assert isinstance(result_6, int)
    assert isinstance(result_14, int)
    assert isinstance(result_1001, int)
    assert result_6 > 0
    assert result_14 > 0
    assert result_1001 > 0
