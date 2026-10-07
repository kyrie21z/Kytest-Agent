# Accepted by submit_tests; explanations in testgen_report.json.

def test_multiply_prime_basic_true():
    from solution import is_multiply_prime
    assert is_multiply_prime(30) == True
    assert is_multiply_prime(8) == True
    assert is_multiply_prime(12) == True
    assert is_multiply_prime(27) == True
    assert is_multiply_prime(42) == True
    assert is_multiply_prime(50) == True

def test_multiply_prime_le_one():
    from solution import is_multiply_prime
    assert is_multiply_prime(1) == False
    assert is_multiply_prime(0) == False
    assert is_multiply_prime(-1) == False
    assert is_multiply_prime(-5) == False

def test_multiply_prime_two_factors():
    from solution import is_multiply_prime
    assert is_multiply_prime(4) == False
    assert is_multiply_prime(6) == False
    assert is_multiply_prime(9) == False
    assert is_multiply_prime(10) == False
    assert is_multiply_prime(14) == False
    assert is_multiply_prime(49) == False

def test_multiply_prime_four_or_more_factors():
    from solution import is_multiply_prime
    assert is_multiply_prime(16) == False
    assert is_multiply_prime(24) == False
    assert is_multiply_prime(36) == False
    assert is_multiply_prime(64) == False
    assert is_multiply_prime(210) == False

def test_multiply_prime_primes_and_boundary():
    from solution import is_multiply_prime
    assert is_multiply_prime(2) == False
    assert is_multiply_prime(3) == False
    assert is_multiply_prime(5) == False
    assert is_multiply_prime(7) == False
    assert is_multiply_prime(11) == False
    assert is_multiply_prime(98) == True
    assert is_multiply_prime(99) == True
    assert is_multiply_prime(96) == False
