"""Unit tests for solution.largest_prime_factor."""

import pytest
from solution import largest_prime_factor


class TestLargestPrimeFactor:
    """Tests for the largest_prime_factor function."""

    # ---- Docstring examples ----

    def test_docstring_example_1(self):
        """Example from docstring: 13195 -> 29."""
        assert largest_prime_factor(13195) == 29

    def test_docstring_example_2(self):
        """Example from docstring: 2048 -> 2."""
        assert largest_prime_factor(2048) == 2

    # ---- Powers of small primes ----

    def test_power_of_2(self):
        """n = 2^k has largest prime factor 2."""
        assert largest_prime_factor(4) == 2
        assert largest_prime_factor(8) == 2
        assert largest_prime_factor(16) == 2
        assert largest_prime_factor(32) == 2
        assert largest_prime_factor(1024) == 2

    def test_power_of_3(self):
        """n = 3^k has largest prime factor 3."""
        assert largest_prime_factor(9) == 3
        assert largest_prime_factor(27) == 3
        assert largest_prime_factor(81) == 3

    def test_power_of_5(self):
        """n = 5^k has largest prime factor 5."""
        assert largest_prime_factor(25) == 5
        assert largest_prime_factor(125) == 5

    def test_power_of_7(self):
        """n = 7^k has largest prime factor 7."""
        assert largest_prime_factor(49) == 7
        assert largest_prime_factor(343) == 7

    # ---- Products of distinct primes ----

    def test_two_distinct_primes_smaller_first(self):
        """n = p * q where p < q."""
        assert largest_prime_factor(6) == 3       # 2 * 3
        assert largest_prime_factor(10) == 5       # 2 * 5
        assert largest_prime_factor(15) == 5       # 3 * 5
        assert largest_prime_factor(35) == 7       # 5 * 7
        assert largest_prime_factor(77) == 11      # 7 * 11
        assert largest_prime_factor(143) == 13     # 11 * 13

    def test_two_distinct_primes_larger(self):
        """n = p * q with larger primes."""
        assert largest_prime_factor(1009 * 1013) == 1013

    def test_three_distinct_primes(self):
        """n = p * q * r."""
        assert largest_prime_factor(30) == 5       # 2 * 3 * 5
        assert largest_prime_factor(105) == 7      # 3 * 5 * 7
        assert largest_prime_factor(231) == 11     # 3 * 7 * 11

    # ---- Mixed composite numbers ----

    def test_mixed_factors(self):
        """Various composite numbers with mixed prime factors."""
        assert largest_prime_factor(12) == 3       # 2^2 * 3
        assert largest_prime_factor(18) == 3       # 2 * 3^2
        assert largest_prime_factor(20) == 5       # 2^2 * 5
        assert largest_prime_factor(50) == 5       # 2 * 5^2
        assert largest_prime_factor(100) == 5      # 2^2 * 5^2
        assert largest_prime_factor(60) == 5       # 2^2 * 3 * 5
        assert largest_prime_factor(84) == 7       # 2^2 * 3 * 7
        assert largest_prime_factor(90) == 5       # 2 * 3^2 * 5
        assert largest_prime_factor(210) == 7      # 2 * 3 * 5 * 7

    def test_large_composite(self):
        """A larger composite number: 9999 = 3^2 * 11 * 101."""
        assert largest_prime_factor(9999) == 101

    # ---- Boundary / edge values ----

    def test_minimal_input(self):
        """Smallest composite number: 4 = 2 * 2."""
        assert largest_prime_factor(4) == 2

    def test_even_number(self):
        """Even composites."""
        assert largest_prime_factor(14) == 7       # 2 * 7
        assert largest_prime_factor(22) == 11      # 2 * 11
        assert largest_prime_factor(26) == 13      # 2 * 13
        assert largest_prime_factor(34) == 17      # 2 * 17

    def test_odd_composite(self):
        """Odd composites."""
        assert largest_prime_factor(9) == 3
        assert largest_prime_factor(21) == 7       # 3 * 7
        assert largest_prime_factor(25) == 5
        assert largest_prime_factor(27) == 3
        assert largest_prime_factor(33) == 11      # 3 * 11

    # ---- Type checking ----

    def test_returns_int(self):
        """Result should be an integer."""
        result = largest_prime_factor(12)
        assert isinstance(result, int)

    # ---- Doctest-style verification ----

    def test_doctest_examples(self):
        """Verify all doctest examples match expected outputs."""
        assert largest_prime_factor(13195) == 29
        assert largest_prime_factor(2048) == 2
