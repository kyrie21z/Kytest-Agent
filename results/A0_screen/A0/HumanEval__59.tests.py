"""Unit tests for solution.largest_prime_factor."""

import pytest
from solution import largest_prime_factor


class TestLargestPrimeFactor:
    """Tests for the largest_prime_factor function."""

    # ------------------------------------------------------------------
    # Doctest examples from the docstring
    # ------------------------------------------------------------------

    def test_docstring_example_1(self):
        assert largest_prime_factor(13195) == 29

    def test_docstring_example_2(self):
        assert largest_prime_factor(2048) == 2

    # ------------------------------------------------------------------
    # Small composite numbers
    # ------------------------------------------------------------------

    @pytest.mark.parametrize(
        "n, expected",
        [
            (4, 2),          # 2 × 2
            (6, 3),          # 2 × 3
            (8, 2),          # 2³
            (9, 3),          # 3²
            (10, 5),         # 2 × 5
            (12, 3),         # 2² × 3
            (14, 7),         # 2 × 7
            (15, 5),         # 3 × 5
            (16, 2),         # 2⁴
            (21, 7),         # 3 × 7
            (22, 11),        # 2 × 11
            (25, 5),         # 5²
            (26, 13),        # 2 × 13
            (27, 3),         # 3³
            (35, 7),         # 5 × 7
            (49, 7),         # 7²
            (100, 5),        # 2² × 5²
            (121, 11),       # 11²
            (143, 13),       # 11 × 13
            (169, 13),       # 13²
        ],
    )
    def test_small_composites(self, n, expected):
        assert largest_prime_factor(n) == expected

    # ------------------------------------------------------------------
    # Larger / more interesting cases
    # ------------------------------------------------------------------

    def test_product_of_two_primes(self):
        # 101 × 103 = 10403 → largest prime factor is 103
        assert largest_prime_factor(10403) == 103

    def test_power_of_a_prime(self):
        # 3¹⁰ = 59049 → largest prime factor is 3
        assert largest_prime_factor(3 ** 10) == 3

    def test_larger_number(self):
        # 99991 = 99991 (prime) but assumption says n is NOT prime,
        # so pick a known composite: 99999 = 3 × 3 × 41 × 271
        assert largest_prime_factor(99999) == 271

    def test_even_number_with_large_prime_factor(self):
        # 2 × 997 = 1994 → largest prime factor is 997
        assert largest_prime_factor(1994) == 997

    def test_odd_number_with_large_prime_factor(self):
        # 3 × 997 = 2991 → largest prime factor is 997
        assert largest_prime_factor(2991) == 997

    # ------------------------------------------------------------------
    # Edge-case boundaries
    # ------------------------------------------------------------------

    def test_minimum_input(self):
        # Smallest composite per problem constraints: 4
        assert largest_prime_factor(4) == 2

    def test_square_of_a_prime(self):
        assert largest_prime_factor(4 ** 2) == 2   # 16 → 2
        assert largest_prime_factor(7 ** 2) == 7   # 49 → 7

    def test_cube_of_a_prime(self):
        assert largest_prime_factor(2 ** 3) == 2   # 8 → 2
        assert largest_prime_factor(5 ** 3) == 5   # 125 → 5

    # ------------------------------------------------------------------
    # Property-based sanity checks
    # ------------------------------------------------------------------

    @pytest.mark.parametrize("n", [6, 10, 14, 15, 21, 22, 26, 33, 34, 35])
    def test_returns_divisor(self, n):
        """The result must divide n evenly."""
        assert n % largest_prime_factor(n) == 0

    @pytest.mark.parametrize("n", [6, 10, 14, 15, 21, 22, 26, 33, 34, 35])
    def test_result_is_prime(self, n):
        """The result must itself be a prime number."""
        result = largest_prime_factor(n)
        assert all(result % i != 0 for i in range(2, int(result ** 0.5) + 1))

    @pytest.mark.parametrize("n", [6, 10, 14, 15, 21, 22, 26, 33, 34, 35])
    def test_no_larger_prime_factor(self, n):
        """No prime larger than the returned value should divide n."""
        result = largest_prime_factor(n)
        for p in range(result + 1, n):
            if all(p % i != 0 for i in range(2, int(p ** 0.5) + 1)):
                assert n % p != 0, f"{p} is a larger prime factor of {n}"
