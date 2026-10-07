"""Unit tests for factorize() in solution.py."""

import pytest
from solution import factorize


# ---------------------------------------------------------------------------
# Docstring examples (the canonical reference)
# ---------------------------------------------------------------------------

class TestDocstringExamples:
    def test_factorize_8(self):
        assert factorize(8) == [2, 2, 2]

    def test_factorize_25(self):
        assert factorize(25) == [5, 5]

    def test_factorize_70(self):
        assert factorize(70) == [2, 5, 7]


# ---------------------------------------------------------------------------
# Normal / typical inputs
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Typical composite and prime numbers."""

    def test_prime_number(self):
        """A prime number returns itself as the only factor."""
        assert factorize(7) == [7]

    def test_prime_13(self):
        assert factorize(13) == [13]

    def test_prime_997(self):
        assert factorize(997) == [997]

    def test_two_primes(self):
        assert factorize(6) == [2, 3]

    def test_three_distinct_primes(self):
        assert factorize(30) == [2, 3, 5]

    def test_four_distinct_primes(self):
        assert factorize(210) == [2, 3, 5, 7]

    def test_square_of_prime(self):
        assert factorize(49) == [7, 7]

    def test_cube_of_prime(self):
        assert factorize(27) == [3, 3, 3]

    def test_product_of_two_same_and_one_different(self):
        assert factorize(12) == [2, 2, 3]

    def test_power_of_two(self):
        assert factorize(64) == [2, 2, 2, 2, 2, 2]

    def test_larger_power_of_two(self):
        assert factorize(1024) == [2] * 10

    def test_mixed_factors(self):
        assert factorize(100) == [2, 2, 5, 5]

    def test_another_mixed(self):
        assert factorize(1000) == [2, 2, 2, 5, 5, 5]

    def test_even_composite(self):
        assert factorize(14) == [2, 7]

    def test_odd_composite(self):
        assert factorize(15) == [3, 5]

    def test_large_composite(self):
        assert factorize(12345) == [3, 5, 823]


# ---------------------------------------------------------------------------
# Boundary cases
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Edge-of-range valid inputs."""

    def test_smallest_prime(self):
        assert factorize(2) == [2]

    def test_second_smallest_prime(self):
        assert factorize(3) == [3]

    def test_smallest_composite(self):
        assert factorize(4) == [2, 2]

    def test_perfect_square(self):
        assert factorize(36) == [2, 2, 3, 3]

    def test_perfect_cube(self):
        assert factorize(8) == [2, 2, 2]

    def test_product_of_first_two_primes_squared(self):
        # 2^2 * 3^2 = 36
        assert factorize(36) == [2, 2, 3, 3]

    def test_number_with_many_small_factors(self):
        # 2^5 * 3 = 96
        assert factorize(96) == [2, 2, 2, 2, 2, 3]


# ---------------------------------------------------------------------------
# Empty / zero-size inputs
# ---------------------------------------------------------------------------

class TestZeroAndOne:
    """Inputs that produce empty results or are degenerate."""

    def test_one(self):
        """1 has no prime factors; the product of an empty list is 1."""
        assert factorize(1) == []

    def test_zero(self):
        """0 cannot be factorized into primes; the implementation returns []."""
        assert factorize(0) == []


# ---------------------------------------------------------------------------
# Invalid inputs – should raise exceptions
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Negative numbers cause math.sqrt to raise ValueError."""

    @pytest.mark.parametrize("n", [-1, -2, -5, -100])
    def test_negative_raises_value_error(self, n):
        with pytest.raises(ValueError):
            factorize(n)


# ---------------------------------------------------------------------------
# Correctness invariant: product of factors == original number
# ---------------------------------------------------------------------------

class TestProductInvariant:
    """For every positive integer n > 1, the product of factors must equal n."""

    @pytest.mark.parametrize(
        "n",
        list(range(2, 101))
        + [100, 256, 512, 1000, 1024, 2048, 4096, 8191, 10000],
    )
    def test_product_equals_original(self, n):
        factors = factorize(n)
        product = 1
        for f in factors:
            product *= f
        assert product == n

    @pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31])
    def test_prime_returns_itself(self, n):
        assert factorize(n) == [n]


# ---------------------------------------------------------------------------
# Order invariant: factors must be non-decreasing
# ---------------------------------------------------------------------------

class TestOrderInvariant:
    """Factors should be listed from smallest to largest."""

    @pytest.mark.parametrize(
        "n",
        [2, 4, 6, 8, 12, 30, 60, 100, 210, 1000, 1024, 997],
    )
    def test_factors_are_sorted(self, n):
        factors = factorize(n)
        assert factors == sorted(factors)
