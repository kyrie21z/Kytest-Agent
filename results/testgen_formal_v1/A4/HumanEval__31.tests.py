# Accepted by submit_tests; explanations in testgen_report.json.

from solution import is_prime as _case0_is_prime

def test_small_primes():
    """Verify that the smallest primes (2, 3, 5, 7) are correctly identified."""
    contract_quote = 'Return true if a given number is prime, and false otherwise.'
    assert _case0_is_prime(2) is True
    assert _case0_is_prime(3) is True
    assert _case0_is_prime(5) is True
    assert _case0_is_prime(7) is True

from solution import is_prime as _case1_is_prime

def test_non_primes_small():
    """Verify that small composite numbers and 0, 1 return False."""
    contract_quote = 'Return true if a given number is prime, and false otherwise.'
    assert _case1_is_prime(0) is False
    assert _case1_is_prime(1) is False
    assert _case1_is_prime(4) is False
    assert _case1_is_prime(6) is False
    assert _case1_is_prime(8) is False
    assert _case1_is_prime(9) is False
    assert _case1_is_prime(10) is False
    assert _case1_is_prime(15) is False

from solution import is_prime as _case2_is_prime

def test_negative_numbers():
    """Negative numbers are not prime."""
    contract_quote = 'Return true if a given number is prime, and false otherwise.'
    assert _case2_is_prime(-1) is False
    assert _case2_is_prime(-2) is False
    assert _case2_is_prime(-100) is False

from solution import is_prime as _case3_is_prime

def test_perfect_squares_of_primes():
    """Perfect squares of primes (4, 9, 25, 49, 121) must return False."""
    contract_quote = 'Return true if a given number is prime, and false otherwise.'
    assert _case3_is_prime(4) is False
    assert _case3_is_prime(9) is False
    assert _case3_is_prime(25) is False
    assert _case3_is_prime(49) is False
    assert _case3_is_prime(121) is False

from solution import is_prime as _case4_is_prime

def test_larger_primes_from_docstring():
    """Test the larger primes cited in the docstring examples."""
    contract_quote = 'Return true if a given number is prime, and false otherwise.'
    assert _case4_is_prime(61) is True
    assert _case4_is_prime(101) is True
    assert _case4_is_prime(13441) is True

from solution import is_prime as _case5_is_prime

def test_even_composites():
    """All even numbers greater than 2 are composite."""
    contract_quote = 'Return true if a given number is prime, and false otherwise.'
    assert _case5_is_prime(2) is True
    assert _case5_is_prime(4) is False
    assert _case5_is_prime(12) is False
    assert _case5_is_prime(100) is False
    assert _case5_is_prime(1000) is False
