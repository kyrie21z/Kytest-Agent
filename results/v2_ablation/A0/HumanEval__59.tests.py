"""Unit tests for solution.py using pytest."""
import math
import pytest
from solution import largest_prime_factor


class TestLargestPrimeFactor:
    """Tests for the largest_prime_factor function."""

    def test_example_from_docstring_1(self):
        """Test case from docstring: 13195 -> 29."""
        assert largest_prime_factor(13195) == 29

    def test_example_from_docstring_2(self):
        """Test case from docstring: 2048 -> 2."""
        assert largest_prime_factor(2048) == 2

    def test_even_number(self):
        """Even composite number: 10 -> 5."""
        assert largest_prime_factor(10) == 5

    def test_even_number_2(self):
        """Another even composite: 14 -> 7."""
        assert largest_prime_factor(14) == 7

    def test_power_of_two(self):
        """Power of two: 16 -> 2."""
        assert largest_prime_factor(16) == 2

    def test_power_of_three(self):
        """Power of three: 27 -> 3."""
        assert largest_prime_factor(27) == 3

    def test_product_of_two_primes(self):
        """Product of two distinct primes: 15 = 3 * 5 -> 5."""
        assert largest_prime_factor(15) == 5

    def test_product_of_two_primes_reversed(self):
        """Product of two distinct primes: 21 = 3 * 7 -> 7."""
        assert largest_prime_factor(21) == 7

    def test_larger_composite(self):
        """Larger composite: 100 = 2^2 * 5^2 -> 5."""
        assert largest_prime_factor(100) == 5

    def test_another_larger_composite(self):
        """Composite with multiple prime factors: 105 = 3 * 5 * 7 -> 7."""
        assert largest_prime_factor(105) == 7

    def test_prime_squared(self):
        """Square of a prime: 49 = 7^2 -> 7."""
        assert largest_prime_factor(49) == 7

    def test_cube_of_a_prime(self):
        """Cube of a prime: 125 = 5^3 -> 5."""
        assert largest_prime_factor(125) == 5

    def test_small_composite(self):
        """Smallest composite: 4 = 2^2 -> 2."""
        assert largest_prime_factor(4) == 2

    def test_medium_composite(self):
        """Medium composite: 99 = 3^2 * 11 -> 11."""
        assert largest_prime_factor(99) == 11

    def test_large_composite(self):
        """Large composite: 9999 = 3^2 * 11 * 101 -> 101."""
        assert largest_prime_factor(9999) == 101

    def test_consistency_with_manual_check(self):
        """Verify result is indeed a prime factor by checking manually."""
        n = 13195
        result = largest_prime_factor(n)
        # The result must divide n
        assert n % result == 0
        # The result must be prime (check no divisors up to sqrt)
        for i in range(2, int(math.isqrt(result)) + 1):
            assert result % i != 0, f"{result} is not prime"

    def test_result_is_always_prime(self):
        """Ensure the returned value is always a prime number."""
        test_values = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]
        for n in test_values:
            result = largest_prime_factor(n)
            assert n % result == 0, f"{result} does not divide {n}"
            for i in range(2, int(math.isqrt(result)) + 1):
                assert result % i != 0, f"{result} is not prime"


# --- Doctest-style tests via pytest --doctest-modules equivalent ---
def test_doctest_examples():
    """Run the doctest examples explicitly."""
    assert largest_prime_factor(13195) == 29
    assert largest_prime_factor(2048) == 2
