"""Unit tests for solution.is_multiply_prime.

The function returns True if the given integer `a` is the product of exactly
3 prime numbers (counting multiplicity), and False otherwise.
Known constraints: a < 100.
"""

import pytest
from solution import is_multiply_prime


# ---------------------------------------------------------------------------
# Normal / typical cases – products of exactly 3 primes
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Inputs that are the product of exactly three primes."""

    def test_30(self):
        # 30 = 2 * 3 * 5
        assert is_multiply_prime(30) is True

    def test_8(self):
        # 8 = 2 * 2 * 2  (same prime repeated)
        assert is_multiply_prime(8) is True

    def test_12(self):
        # 12 = 2 * 2 * 3
        assert is_multiply_prime(12) is True

    def test_42(self):
        # 42 = 2 * 3 * 7
        assert is_multiply_prime(42) is True

    def test_18(self):
        # 18 = 2 * 3 * 3
        assert is_multiply_prime(18) is True

    def test_27(self):
        # 27 = 3 * 3 * 3
        assert is_multiply_prime(27) is True

    def test_105(self):
        # 105 = 3 * 5 * 7  (just above the documented bound)
        assert is_multiply_prime(105) is True

    def test_98(self):
        # 98 = 2 * 7 * 7
        assert is_multiply_prime(98) is True

    def test_99(self):
        # 99 = 3 * 3 * 11
        assert is_multiply_prime(99) is True

    def test_50(self):
        # 50 = 2 * 5 * 5
        assert is_multiply_prime(50) is True

    def test_75(self):
        # 75 = 3 * 5 * 5
        assert is_multiply_prime(75) is True

    def test_84(self):
        # 84 = 2 * 2 * 3 * 7  → 4 primes → NOT 3
        assert is_multiply_prime(84) is False


# ---------------------------------------------------------------------------
# Boundary cases – edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Edge-of-range inputs around the documented constraint a < 100."""

    def test_min_valid_product(self):
        # 8 is the smallest number with exactly 3 prime factors
        assert is_multiply_prime(8) is True

    def test_one_below_min(self):
        # 7 has only 1 prime factor
        assert is_multiply_prime(7) is False

    def test_two_below_min(self):
        # 6 = 2 * 3 → 2 prime factors
        assert is_multiply_prime(6) is False

    def test_three_below_min(self):
        # 5 → 1 prime factor
        assert is_multiply_prime(5) is False

    def test_four_below_min(self):
        # 4 = 2 * 2 → 2 prime factors
        assert is_multiply_prime(4) is False

    def test_five_below_min(self):
        # 3 → 1 prime factor
        assert is_multiply_prime(3) is False

    def test_six_below_min(self):
        # 2 → 1 prime factor
        assert is_multiply_prime(2) is False


# ---------------------------------------------------------------------------
# Empty / null / zero-size inputs
# ---------------------------------------------------------------------------

class TestZeroAndNegativeInputs:
    """Inputs at or below 1, which the function explicitly handles."""

    def test_zero(self):
        assert is_multiply_prime(0) is False

    def test_negative_one(self):
        assert is_multiply_prime(-1) is False

    def test_negative_ten(self):
        assert is_multiply_prime(-10) is False

    def test_one(self):
        # 1 has no prime factors
        assert is_multiply_prime(1) is False


# ---------------------------------------------------------------------------
# Invalid inputs – wrong type
# ---------------------------------------------------------------------------

class TestInvalidInputTypes:
    """Inputs that violate the expected integer type."""

    @pytest.mark.parametrize("value", [None, "30", 30.0, 30.5, [], {}])
    def test_non_integer_raises_or_returns_false(self, value):
        """Non-integer inputs may raise TypeError or return False depending
        on implementation; we just ensure no unhandled exception occurs."""
        try:
            result = is_multiply_prime(value)
            # If it returns without error, accept any boolean result
            assert isinstance(result, bool)
        except (TypeError, ValueError):
            pass  # Expected for clearly invalid types


# ---------------------------------------------------------------------------
# Additional edge cases – larger numbers beyond documented range
# ---------------------------------------------------------------------------

class TestLargerNumbers:
    """Numbers outside the documented a < 100 range."""

    def test_1000(self):
        # 1000 = 2^3 * 5^3 → 6 prime factors
        assert is_multiply_prime(1000) is False

    def test_210(self):
        # 210 = 2 * 3 * 5 * 7 → 4 prime factors
        assert is_multiply_prime(210) is False

    def test_217(self):
        # 217 = 7 * 31 → 2 prime factors
        assert is_multiply_prime(217) is False

    def test_221(self):
        # 221 = 13 * 17 → 2 prime factors
        assert is_multiply_prime(221) is False

    def test_273(self):
        # 273 = 3 * 7 * 13 → 3 prime factors
        assert is_multiply_prime(273) is True


# ---------------------------------------------------------------------------
# Parametrized exhaustive-ish sweep for small range
# ---------------------------------------------------------------------------

class TestSweepSmallRange:
    """Check every integer from -5 to 100 against an independent oracle."""

    @staticmethod
    def _prime_factors_with_multiplicity(n):
        """Return list of prime factors of n with multiplicity."""
        if n <= 1:
            return []
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors

    @pytest.mark.parametrize(
        "a, expected",
        [
            (n, len(is_multiply_prime.__code__.co_consts) == 0)  # placeholder
            for n in range(-5, 101)
        ],
    )
    def test_sweep_independent_oracle(self, a, expected):
        """Compare against our own prime-factor-counting oracle."""
        actual_count = len(self._prime_factors_with_multiplicity(a))
        expected_result = actual_count == 3
        assert is_multiply_prime(a) is expected_result
