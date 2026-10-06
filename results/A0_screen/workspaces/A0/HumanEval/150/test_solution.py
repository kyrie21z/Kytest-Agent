import pytest
from solution import x_or_y


class TestXorYBasicCases:
    """Test basic functionality with positive integers."""

    def test_prime_returns_x(self):
        """When n is prime, return x."""
        assert x_or_y(7, 34, 12) == 34

    def test_non_prime_returns_y(self):
        """When n is not prime, return y."""
        assert x_or_y(15, 8, 5) == 5

    def test_docstring_example_1(self):
        """Example from docstring: x_or_y(7, 34, 12) == 34"""
        assert x_or_y(7, 34, 12) == 34

    def test_docstring_example_2(self):
        """Example from docstring: x_or_y(15, 8, 5) == 5"""
        assert x_or_y(15, 8, 5) == 5


class TestPrimeNumbers:
    """Test that prime numbers correctly return x."""

    @pytest.mark.parametrize("n, x, y", [
        (2, 10, 20),       # smallest prime
        (3, 1, 0),         # small prime
        (5, 100, 200),     # small prime
        (7, 34, 12),       # example from docstring
        (11, -1, -2),      # negative x and y
        (13, 0, 999),      # x is zero
        (17, 5, 5),        # x equals y
        (19, -100, 100),   # mixed signs
        (23, 1, 1),        # single digit prime
        (29, 42, 0),       # larger prime
        (97, 1, 0),        # largest two-digit prime
    ])
    def test_prime_returns_x(self, n, x, y):
        """For various prime numbers, verify x is returned."""
        assert x_or_y(n, x, y) == x


class TestNonPrimeNumbers:
    """Test that non-prime numbers correctly return y."""

    @pytest.mark.parametrize("n, x, y", [
        (0, 10, 20),       # zero is not prime
        (1, 10, 20),       # one is not prime
        (4, 10, 20),       # even composite
        (6, 1, 0),         # even composite
        (8, 100, 200),     # even composite
        (9, 1, 0),         # odd composite (3*3)
        (10, -1, -2),      # even composite
        (12, 0, 999),      # even composite
        (14, 5, 5),        # even composite
        (15, 8, 5),        # example from docstring (3*5)
        (16, -100, 100),   # power of 2
        (21, 42, 0),       # odd composite (3*7)
        (25, 1, 0),        # odd composite (5*5)
        (27, 1, 0),        # odd composite (3*9)
        (100, 1, 0),       # large composite
        (-1, 1, 0),        # negative number (not prime)
        (-5, 1, 0),        # negative number (not prime)
    ])
    def test_non_prime_returns_y(self, n, x, y):
        """For various non-prime numbers, verify y is returned."""
        assert x_or_y(n, x, y) == y


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_n_equals_zero(self):
        """Zero is not prime; should return y."""
        assert x_or_y(0, 1, 0) == 0

    def test_n_equals_one(self):
        """One is not prime; should return y."""
        assert x_or_y(1, 1, 0) == 0

    def test_n_equals_two(self):
        """Two is the smallest prime; should return x."""
        assert x_or_y(2, "prime", "not") == "prime"

    def test_negative_n(self):
        """Negative numbers are not prime; should return y."""
        assert x_or_y(-1, 10, 20) == 20
        assert x_or_y(-7, 10, 20) == 20

    def test_large_prime(self):
        """Test with a large prime number."""
        assert x_or_y(997, 42, 0) == 42

    def test_large_composite(self):
        """Test with a large composite number."""
        assert x_or_y(1000, 42, 0) == 0

    def test_x_and_y_are_same(self):
        """When x equals y, result should be x regardless of primality."""
        assert x_or_y(7, 5, 5) == 5
        assert x_or_y(8, 5, 5) == 5

    def test_x_is_zero(self):
        """When x is zero and n is prime, return zero."""
        assert x_or_y(7, 0, 5) == 0

    def test_y_is_zero(self):
        """When y is zero and n is not prime, return zero."""
        assert x_or_y(8, 5, 0) == 0

    def test_both_zero(self):
        """When both x and y are zero, return zero."""
        assert x_or_y(7, 0, 0) == 0
        assert x_or_y(8, 0, 0) == 0

    def test_with_strings(self):
        """Test with string values for x and y."""
        assert x_or_y(7, "hello", "world") == "hello"
        assert x_or_y(8, "hello", "world") == "world"

    def test_with_floats(self):
        """Test with float values for x and y."""
        assert x_or_y(7, 3.14, 2.71) == 3.14
        assert x_or_y(8, 3.14, 2.71) == 2.71

    def test_with_none(self):
        """Test with None values for x and y."""
        assert x_or_y(7, None, "fallback") is None
        assert x_or_y(8, "value", None) is None

    def test_with_empty_string(self):
        """Test with empty string as x or y."""
        assert x_or_y(7, "", "fallback") == ""
        assert x_or_y(8, "value", "") == ""


class TestSpecificPrimes:
    """Test known prime numbers across different ranges."""

    @pytest.mark.parametrize("n", [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97,
        101, 103, 107, 109, 113,
        997,
    ])
    def test_known_primes_return_x(self, n):
        """All known primes should return x."""
        assert x_or_y(n, "prime", "composite") == "prime"


class TestSpecificComposites:
    """Test known composite numbers across different categories."""

    @pytest.mark.parametrize("n", [
        0, 1,
        4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20,
        21, 22, 24, 25, 26, 27, 28, 30,
        100, 1000, 10000,
    ])
    def test_known_composites_return_y(self, n):
        """All known composites (and 0, 1) should return y."""
        assert x_or_y(n, "prime", "composite") == "composite"
