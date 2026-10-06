"""Unit tests for solution.is_prime().

Test categories:
1. Normal cases – typical prime and composite inputs.
2. Boundary cases at the edges of valid input ranges (0, 1, 2, 3).
3. Zero / negative inputs.
4. Invalid inputs – non-integer types that might be passed.
5. Exception / performance – very large numbers.
"""

import pytest
from solution import is_prime


# ---------------------------------------------------------------------------
# 1. Normal cases – well-known primes
# ---------------------------------------------------------------------------
class TestPrimes:
    """Every value here must return True."""

    @pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23])
    def test_small_primes(self, n):
        assert is_prime(n) is True

    @pytest.mark.parametrize("n", [61, 101, 13441])
    def test_docstring_primes(self, n):
        """Values taken directly from the docstring doctests."""
        assert is_prime(n) is True

    @pytest.mark.parametrize("n", [1009, 1013, 10007, 100003])
    def test_larger_primes(self, n):
        assert is_prime(n) is True


# ---------------------------------------------------------------------------
# 1b. Normal cases – well-known composites
# ---------------------------------------------------------------------------
class TestComposites:
    """Every value here must return False."""

    @pytest.mark.parametrize("n", [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20])
    def test_small_composites(self, n):
        assert is_prime(n) is False

    @pytest.mark.parametrize("n", [100, 121, 49, 81, 125, 27, 1000])
    def test_various_composites(self, n):
        assert is_prime(n) is False

    @pytest.mark.parametrize("n", [2 * p for p in [3, 5, 7, 11, 13]])
    def test_even_composites(self, n):
        assert is_prime(n) is False


# ---------------------------------------------------------------------------
# 2. Boundary cases at the edges of valid input ranges
# ---------------------------------------------------------------------------
class TestBoundaries:
    """Edge values around the smallest positive integers."""

    def test_two_is_prime(self):
        """2 is the smallest prime."""
        assert is_prime(2) is True

    def test_three_is_prime(self):
        """3 is the next prime after 2."""
        assert is_prime(3) is True

    def test_four_is_not_prime(self):
        """4 = 2 × 2, first even composite."""
        assert is_prime(4) is False


# ---------------------------------------------------------------------------
# 3. Zero, one, and negative inputs
# ---------------------------------------------------------------------------
class TestNonPositive:
    """Numbers ≤ 1 are not prime by definition."""

    @pytest.mark.parametrize("n", [0, 1])
    def test_zero_and_one(self, n):
        assert is_prime(n) is False

    @pytest.mark.parametrize("n", [-1, -2, -5, -10, -100])
    def test_negative_numbers(self, n):
        assert is_prime(n) is False


# ---------------------------------------------------------------------------
# 4. Invalid inputs – non-integer types
# ---------------------------------------------------------------------------
class TestInvalidInputs:
    """What happens when non-integer types are passed?"""

    @pytest.mark.parametrize("n", [2.0, 3.5, 4.0, -1.5])
    def test_float_inputs(self, n):
        """Floats may or may not raise; we just record the behaviour."""
        # The implementation does not guard against floats.
        # For float values that represent whole numbers (e.g. 2.0),
        # the result should match the integer equivalent.
        try:
            result = is_prime(n)
            expected = is_prime(int(n))
            assert result == expected
        except TypeError:
            # Acceptable – the function may reject floats outright.
            pass

    @pytest.mark.parametrize("n", ["hello", [], {}, None])
    def test_non_numeric_inputs(self, n):
        """These inputs will likely raise TypeError or ValueError."""
        with pytest.raises((TypeError, ValueError)):
            is_prime(n)

    def test_bool_true(self):
        """In Python, bool is a subclass of int: True == 1, so is_prime(True) == is_prime(1) == False."""
        assert is_prime(True) is False

    def test_bool_false(self):
        """In Python, bool is a subclass of int: False == 0, so is_prime(False) == is_prime(0) == False."""
        assert is_prime(False) is False


# ---------------------------------------------------------------------------
# 5. Exception / performance – very large numbers
# ---------------------------------------------------------------------------
class TestLargeNumbers:
    """Stress-test with larger inputs to ensure correctness and no errors."""

    @pytest.mark.parametrize("n", [999983, 999979, 999961])
    def test_large_primes(self, n):
        """Known large primes near 1 000 000."""
        assert is_prime(n) is True

    @pytest.mark.parametrize("n", [1_000_000, 999_999, 100_000])
    def test_large_composites(self, n):
        assert is_prime(n) is False

    def test_square_of_prime(self):
        """A square of a prime is composite."""
        assert is_prime(49) is False  # 7²
        assert is_prime(121) is False  # 11²
        assert is_prime(289) is False  # 17²

    def test_product_of_two_distinct_primes(self):
        """Product of two distinct primes is composite."""
        assert is_prime(6) is False   # 2 × 3
        assert is_prime(15) is False  # 3 × 5
        assert is_prime(35) is False  # 5 × 7

    def test_power_of_two(self):
        """All powers of 2 greater than 2 are composite."""
        for exp in range(2, 20):
            assert is_prime(2 ** exp) is False

    def test_mersenne_exponents(self):
        """Mersenne numbers 2^p - 1 for small prime p."""
        # 2^2 - 1 = 3  → prime
        assert is_prime(3) is True
        # 2^3 - 1 = 7  → prime
        assert is_prime(7) is True
        # 2^5 - 1 = 31 → prime
        assert is_prime(31) is True
        # 2^7 - 1 = 127 → prime
        assert is_prime(127) is True
