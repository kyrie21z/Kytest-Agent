"""Unit tests for is_multiply_prime in solution.py.

The function returns True if the given number is the multiplication of
exactly 3 prime numbers (counting multiplicity), and False otherwise.
Known constraint: a < 100.
"""

import pytest
from solution import is_multiply_prime


# ---------------------------------------------------------------------------
# 1. Normal / typical positive cases – should return True
# ---------------------------------------------------------------------------
class TestTrueCases:
    """Numbers that are the product of exactly 3 primes (with multiplicity)."""

    # Three distinct primes
    def test_30(self):
        assert is_multiply_prime(30) is True  # 2 * 3 * 5

    def test_42(self):
        assert is_multiply_prime(42) is True  # 2 * 3 * 7

    def test_66(self):
        assert is_multiply_prime(66) is True  # 2 * 3 * 11

    def test_70(self):
        assert is_multiply_prime(70) is True  # 2 * 5 * 7

    def test_78(self):
        assert is_multiply_prime(78) is True  # 2 * 3 * 13

    # Two identical primes × one different
    def test_12(self):
        assert is_multiply_prime(12) is True  # 2 * 2 * 3

    def test_18(self):
        assert is_multiply_prime(18) is True  # 2 * 3 * 3

    def test_20(self):
        assert is_multiply_prime(20) is True  # 2 * 2 * 5

    def test_28(self):
        assert is_multiply_prime(28) is True  # 2 * 2 * 7

    def test_44(self):
        assert is_multiply_prime(44) is True  # 2 * 2 * 11

    def test_50(self):
        assert is_multiply_prime(50) is True  # 2 * 5 * 5

    def test_63(self):
        assert is_multiply_prime(63) is True  # 3 * 3 * 7

    def test_75(self):
        assert is_multiply_prime(75) is True  # 3 * 5 * 5

    def test_98(self):
        assert is_multiply_prime(98) is True  # 2 * 7 * 7

    def test_99(self):
        assert is_multiply_prime(99) is True  # 3 * 3 * 11

    # All three primes identical
    def test_8(self):
        assert is_multiply_prime(8) is True  # 2 * 2 * 2

    def test_27(self):
        assert is_multiply_prime(27) is True  # 3 * 3 * 3

    def test_125(self):
        assert is_multiply_prime(125) is True  # 5 * 5 * 5 (outside <100 but valid logic)

    # Edge near upper bound (< 100)
    def test_92(self):
        assert is_multiply_prime(92) is True  # 2 * 2 * 23

    def test_68(self):
        assert is_multiply_prime(68) is True  # 2 * 2 * 17

    def test_76(self):
        assert is_multiply_prime(76) is True  # 2 * 2 * 19


# ---------------------------------------------------------------------------
# 2. Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------
class TestBoundaryCases:
    """Edge values within and just outside the documented range."""

    # Smallest possible inputs
    def test_zero(self):
        assert is_multiply_prime(0) is False

    def test_one(self):
        assert is_multiply_prime(1) is False

    # Single primes (only 1 factor)
    def test_two(self):
        assert is_multiply_prime(2) is False  # prime itself

    def test_three(self):
        assert is_multiply_prime(3) is False

    def test_five(self):
        assert is_multiply_prime(5) is False

    def test_seven(self):
        assert is_multiply_prime(7) is False

    # Products of exactly 2 primes (should be False)
    def test_four(self):
        assert is_multiply_prime(4) is False  # 2 * 2

    def test_nine(self):
        assert is_multiply_prime(9) is False  # 3 * 3

    def test_six(self):
        assert is_multiply_prime(6) is False  # 2 * 3

    def test_ten(self):
        assert is_multiply_prime(10) is False  # 2 * 5

    def test_fifteen(self):
        assert is_multiply_prime(15) is False  # 3 * 5

    def test_fourteen(self):
        assert is_multiply_prime(14) is False  # 2 * 7

    # Product of 4 primes (should be False)
    def test_sixty(self):
        assert is_multiply_prime(60) is False  # 2 * 2 * 3 * 5

    def test_sixteen(self):
        assert is_multiply_prime(16) is False  # 2 * 2 * 2 * 2

    def test_54(self):
        assert is_multiply_prime(54) is False  # 2 * 3 * 3 * 3

    def test_100(self):
        assert is_multiply_prime(100) is False  # 2 * 2 * 5 * 5

    # Largest value under the documented constraint
    def test_97(self):
        assert is_multiply_prime(97) is False  # prime itself

    def test_96(self):
        assert is_multiply_prime(96) is False  # 2^5 * 3 → 6 primes


# ---------------------------------------------------------------------------
# 3. Empty, null, or zero-size inputs
# ---------------------------------------------------------------------------
class TestNullAndZeroInputs:
    """Edge cases with unusual input types/values."""

    def test_negative(self):
        assert is_multiply_prime(-1) is False

    def test_negative_large(self):
        assert is_multiply_prime(-100) is False

    def test_float_input(self):
        # Floats cause TypeError because [True] * (a + 1) requires an int.
        with pytest.raises(TypeError):
            is_multiply_prime(30.0)

    def test_float_not_whole(self):
        with pytest.raises(TypeError):
            is_multiply_prime(30.5)


# ---------------------------------------------------------------------------
# 4. Invalid / unexpected inputs
# ---------------------------------------------------------------------------
class TestInvalidInputs:
    """Inputs that don't fit normal numeric expectations."""

    def test_none_input(self):
        with pytest.raises(TypeError):
            is_multiply_prime(None)

    def test_string_input(self):
        with pytest.raises(TypeError):
            is_multiply_prime("30")

    def test_list_input(self):
        with pytest.raises(TypeError):
            is_multiply_prime([30])

    def test_dict_input(self):
        with pytest.raises(TypeError):
            is_multiply_prime({"a": 30})


# ---------------------------------------------------------------------------
# 5. Exhaustive check for all integers 0..99
# ---------------------------------------------------------------------------
class TestExhaustiveRange:
    """Verify every integer from 0 to 99 against a brute-force oracle."""

    @staticmethod
    def _prime_factors_with_multiplicity(n):
        """Return list of prime factors of n, with multiplicity."""
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

    @pytest.mark.parametrize("a", range(100))
    def test_all_values_under_100(self, a):
        expected = len(self._prime_factors_with_multiplicity(a)) == 3
        actual = is_multiply_prime(a)
        assert actual is expected, (
            f"is_multiply_prime({a}) returned {actual}, "
            f"expected {expected} (factors={self._prime_factors_with_multiplicity(a)})"
        )
