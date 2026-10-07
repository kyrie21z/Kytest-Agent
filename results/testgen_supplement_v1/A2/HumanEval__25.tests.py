"""Unit tests for factorize() in solution.py."""

import pytest
from solution import factorize


# ---------------------------------------------------------------------------
# Normal / typical cases
# ---------------------------------------------------------------------------

class TestFactorizeNormalCases:
    """Tests with typical positive integers > 1."""

    def test_docstring_example_8(self):
        assert factorize(8) == [2, 2, 2]

    def test_docstring_example_25(self):
        assert factorize(25) == [5, 5]

    def test_docstring_example_70(self):
        assert factorize(70) == [2, 5, 7]

    def test_prime_number(self):
        """A prime number returns itself as the only factor."""
        assert factorize(7) == [7]

    def test_prime_number_97(self):
        assert factorize(97) == [97]

    def test_smallest_prime(self):
        assert factorize(2) == [2]

    def test_two_times_three(self):
        assert factorize(6) == [2, 3]

    def test_twelve(self):
        assert factorize(12) == [2, 2, 3]

    def test_one_hundred(self):
        assert factorize(100) == [2, 2, 5, 5]

    def test_fourty_nine(self):
        assert factorize(49) == [7, 7]

    def test_one_zero_five(self):
        assert factorize(105) == [3, 5, 7]

    def test_product_of_three_distinct_primes(self):
        assert factorize(30) == [2, 3, 5]

    def test_power_of_two_large(self):
        assert factorize(64) == [2, 2, 2, 2, 2, 2]

    def test_square_of_prime(self):
        assert factorize(121) == [11, 11]

    def test_cube_of_prime(self):
        assert factorize(27) == [3, 3, 3]

    def test_even_composite(self):
        assert factorize(50) == [2, 5, 5]

    def test_odd_composite(self):
        assert factorize(81) == [3, 3, 3, 3]

    def test_large_composite(self):
        # 2 * 3 * 5 * 7 * 11 * 13 = 30030
        assert factorize(30030) == [2, 3, 5, 7, 11, 13]

    def test_factorization_product_equals_original(self):
        """Verify that the product of all factors equals the input number."""
        for n in range(2, 1000):
            factors = factorize(n)
            product = 1
            for f in factors:
                product *= f
            assert product == n, f"Product mismatch for {n}: factors={factors}"


# ---------------------------------------------------------------------------
# Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------

class TestFactorizeBoundaryCases:
    """Tests at the boundaries of valid input."""

    def test_one(self):
        """1 has no prime factors — empty list."""
        assert factorize(1) == []

    def test_two(self):
        """Smallest valid input (smallest prime)."""
        assert factorize(2) == [2]

    def test_three(self):
        assert factorize(3) == [3]

    def test_four(self):
        assert factorize(4) == [2, 2]

    def test_max_small_range(self):
        """Check every number from 2 to 100."""
        for n in range(2, 101):
            factors = factorize(n)
            # Verify sorted order
            assert factors == sorted(factors), f"Not sorted for {n}"
            # Verify product
            product = 1
            for f in factors:
                product *= f
            assert product == n, f"Product mismatch for {n}"


# ---------------------------------------------------------------------------
# Empty / zero-size inputs
# ---------------------------------------------------------------------------

class TestFactorizeZeroSizeInputs:
    """Tests for edge-case inputs that produce empty results."""

    def test_zero(self):
        """0: sqrt(0)=0, loop condition fails immediately, returns []."""
        assert factorize(0) == []

    def test_one_empty_factors(self):
        """1: no prime factors exist."""
        assert factorize(1) == []


# ---------------------------------------------------------------------------
# Invalid inputs
# ---------------------------------------------------------------------------

class TestFactorizeInvalidInputs:
    """Tests for inputs outside the documented domain."""

    def test_negative_integer(self):
        """Negative numbers cause math.sqrt to raise ValueError."""
        with pytest.raises(ValueError):
            factorize(-1)

    def test_negative_integer_minus_ten(self):
        with pytest.raises(ValueError):
            factorize(-10)

    def test_negative_integer_minus_one_hundred(self):
        with pytest.raises(ValueError):
            factorize(-100)


# ---------------------------------------------------------------------------
# Exception cases
# ---------------------------------------------------------------------------

class TestFactorizeExceptions:
    """Tests where the function may raise exceptions on bad input types."""

    def test_none_input(self):
        """Passing None should raise TypeError."""
        with pytest.raises(TypeError):
            factorize(None)

    def test_string_input(self):
        """Passing a string should raise TypeError."""
        with pytest.raises(TypeError):
            factorize("abc")

    def test_list_input(self):
        with pytest.raises(TypeError):
            factorize([2, 3])
