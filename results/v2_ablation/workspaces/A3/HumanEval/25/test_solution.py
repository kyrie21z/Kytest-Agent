"""Unit tests for solution.factorize().

The factorize(n) function returns the prime factorization of a positive
integer n as a sorted list of prime factors, each repeated according to
its multiplicity.  Every returned list L satisfies:
    product(L) == n   (with product([]) == 1)
"""

import pytest
from solution import factorize


# ---------------------------------------------------------------------------
# Normal / typical inputs
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with well-defined, typical positive integers."""

    def test_power_of_two(self):
        assert factorize(8) == [2, 2, 2]

    def test_square_of_prime(self):
        assert factorize(25) == [5, 5]

    def test_product_of_distinct_primes(self):
        assert factorize(70) == [2, 5, 7]

    def test_mixed_factors(self):
        # 12 = 2 * 2 * 3
        assert factorize(12) == [2, 2, 3]

    def test_another_mixed(self):
        # 100 = 2 * 2 * 5 * 5
        assert factorize(100) == [2, 2, 5, 5]

    def test_small_composite(self):
        # 6 = 2 * 3
        assert factorize(6) == [2, 3]

    def test_cube_of_prime(self):
        # 27 = 3 * 3 * 3
        assert factorize(27) == [3, 3, 3]

    def test_four_distinct_primes(self):
        # 210 = 2 * 3 * 5 * 7
        assert factorize(210) == [2, 3, 5, 7]

    def test_larger_composite(self):
        # 1000 = 2^3 * 5^3
        assert factorize(1000) == [2, 2, 2, 5, 5, 5]

    def test_prime_squared_times_another(self):
        # 98 = 2 * 7 * 7
        assert factorize(98) == [2, 7, 7]

    def test_single_large_prime(self):
        # 97 is prime
        assert factorize(97) == [97]

    def test_even_number_with_odd_factor(self):
        # 42 = 2 * 3 * 7
        assert factorize(42) == [2, 3, 7]

    def test_highly_composite(self):
        # 72 = 2^3 * 3^2
        assert factorize(72) == [2, 2, 2, 3, 3]


# ---------------------------------------------------------------------------
# Boundary cases
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_one(self):
        # 1 has no prime factors
        assert factorize(1) == []

    def test_smallest_prime(self):
        assert factorize(2) == [2]

    def test_second_prime(self):
        assert factorize(3) == [3]

    def test_smallest_composite(self):
        assert factorize(4) == [2, 2]

    def test_largest_input_in_range(self):
        # A larger number to stress-test the sqrt loop
        assert factorize(9999) == [3, 3, 11, 101]


# ---------------------------------------------------------------------------
# Edge: zero
# ---------------------------------------------------------------------------

class TestZeroInput:
    """Behavior when n == 0."""

    def test_zero_returns_empty_list(self):
        # math.sqrt(0) = 0, loop never runs, n > 1 is False → []
        assert factorize(0) == []


# ---------------------------------------------------------------------------
# Invalid inputs & exceptions
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Negative numbers are invalid for prime factorization."""

    def test_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            factorize(-1)

    def test_negative_two_raises_value_error(self):
        with pytest.raises(ValueError):
            factorize(-10)

    def test_negative_large_raises_value_error(self):
        with pytest.raises(ValueError):
            factorize(-1000)


# ---------------------------------------------------------------------------
# Correctness invariant: product of factors equals original number
# ---------------------------------------------------------------------------

class TestProductInvariant:
    """Every factorization must satisfy product(factors) == n."""

    @staticmethod
    def _product(lst):
        p = 1
        for x in lst:
            p *= x
        return p

    def test_invariant_for_many_numbers(self):
        for n in range(2, 1001):
            factors = factorize(n)
            assert self._product(factors) == n, (
                f"product({factors}) != {n}"
            )
