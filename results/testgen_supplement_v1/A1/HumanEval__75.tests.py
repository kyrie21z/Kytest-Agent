"""Unit tests for solution.is_multiply_prime."""

import pytest
from solution import is_multiply_prime


# ---------------------------------------------------------------------------
# Normal cases – numbers that ARE the product of exactly 3 primes
# ---------------------------------------------------------------------------

class TestMultiplyPrimeTrue:
    """Numbers whose prime-factor count (with multiplicity) equals 3."""

    def test_30(self):
        # 30 = 2 * 3 * 5
        assert is_multiply_prime(30) is True

    def test_8(self):
        # 8 = 2 * 2 * 2
        assert is_multiply_prime(8) is True

    def test_12(self):
        # 12 = 2 * 2 * 3
        assert is_multiply_prime(12) is True

    def test_27(self):
        # 27 = 3 * 3 * 3
        assert is_multiply_prime(27) is True

    def test_18(self):
        # 18 = 2 * 3 * 3
        assert is_multiply_prime(18) is True

    def test_20(self):
        # 20 = 2 * 2 * 5
        assert is_multiply_prime(20) is True

    def test_42(self):
        # 42 = 2 * 3 * 7
        assert is_multiply_prime(42) is True

    def test_44(self):
        # 44 = 2 * 2 * 11
        assert is_multiply_prime(44) is True

    def test_45(self):
        # 45 = 3 * 3 * 5
        assert is_multiply_prime(45) is True

    def test_50(self):
        # 50 = 2 * 5 * 5
        assert is_multiply_prime(50) is True

    def test_98(self):
        # 98 = 2 * 7 * 7
        assert is_multiply_prime(98) is True

    def test_99(self):
        # 99 = 3 * 3 * 11
        assert is_multiply_prime(99) is True

    def test_52(self):
        # 52 = 2 * 2 * 13
        assert is_multiply_prime(52) is True

    def test_68(self):
        # 68 = 2 * 2 * 17
        assert is_multiply_prime(68) is True

    def test_75(self):
        # 75 = 3 * 5 * 5
        assert is_multiply_prime(75) is True


# ---------------------------------------------------------------------------
# Normal cases – numbers that are NOT the product of exactly 3 primes
# ---------------------------------------------------------------------------

class TestMultiplyPrimeFalse:
    """Numbers whose prime-factor count (with multiplicity) != 3."""

    def test_two_factors_6(self):
        # 6 = 2 * 3
        assert is_multiply_prime(6) is False

    def test_two_factors_10(self):
        # 10 = 2 * 5
        assert is_multiply_prime(10) is False

    def test_two_factors_14(self):
        # 14 = 2 * 7
        assert is_multiply_prime(14) is False

    def test_two_factors_15(self):
        # 15 = 3 * 5
        assert is_multiply_prime(15) is False

    def test_two_factors_4(self):
        # 4 = 2 * 2
        assert is_multiply_prime(4) is False

    def test_two_factors_9(self):
        # 9 = 3 * 3
        assert is_multiply_prime(9) is False

    def test_four_factors_100(self):
        # 100 = 2 * 2 * 5 * 5
        assert is_multiply_prime(100) is False

    def test_four_factors_60(self):
        # 60 = 2 * 2 * 3 * 5
        assert is_multiply_prime(60) is False

    def test_one_factor_prime_2(self):
        # 2 is prime
        assert is_multiply_prime(2) is False

    def test_one_factor_prime_3(self):
        # 3 is prime
        assert is_multiply_prime(3) is False

    def test_one_factor_prime_5(self):
        # 5 is prime
        assert is_multiply_prime(5) is False

    def test_one_factor_prime_7(self):
        # 7 is prime
        assert is_multiply_prime(7) is False

    def test_one_factor_prime_11(self):
        # 11 is prime
        assert is_multiply_prime(11) is False

    def test_one_factor_prime_13(self):
        # 13 is prime
        assert is_multiply_prime(13) is False

    def test_one_factor_prime_97(self):
        # 97 is prime
        assert is_multiply_prime(97) is False


# ---------------------------------------------------------------------------
# Boundary cases – edge values at the low end
# ---------------------------------------------------------------------------

class TestBoundaryLow:
    """Edge cases at the lower boundary of valid input range."""

    def test_zero(self):
        assert is_multiply_prime(0) is False

    def test_one(self):
        assert is_multiply_prime(1) is False

    def test_negative_one(self):
        assert is_multiply_prime(-1) is False

    def test_negative_five(self):
        assert is_multiply_prime(-5) is False

    def test_negative_hundred(self):
        assert is_multiply_prime(-100) is False


# ---------------------------------------------------------------------------
# Edge cases near the upper bound (a < 100)
# ---------------------------------------------------------------------------

class TestBoundaryHigh:
    """Edge cases near the documented upper bound."""

    def test_96(self):
        # 96 = 2^5 * 3 -> 6 prime factors
        assert is_multiply_prime(96) is False

    def test_90(self):
        # 90 = 2 * 3 * 3 * 5 -> 4 prime factors
        assert is_multiply_prime(90) is False

    def test_84(self):
        # 84 = 2 * 2 * 3 * 7 -> 4 prime factors
        assert is_multiply_prime(84) is False

    def test_81(self):
        # 81 = 3^4 -> 4 prime factors
        assert is_multiply_prime(81) is False

    def test_64(self):
        # 64 = 2^6 -> 6 prime factors
        assert is_multiply_prime(64) is False


# ---------------------------------------------------------------------------
# Additional property-based checks
# ---------------------------------------------------------------------------

class TestProperties:
    """Tests based on mathematical properties of the function."""

    def test_all_primes_below_100_return_false(self):
        """Every prime number below 100 should return False."""
        primes = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97,
        ]
        for p in primes:
            assert is_multiply_prime(p) is False, f"Expected False for prime {p}"

    def test_all_squares_of_primes_return_false(self):
        """p^2 has exactly 2 prime factors, so should return False."""
        squares = [p * p for p in [2, 3, 5, 7, 11, 13]]
        for s in squares:
            assert is_multiply_prime(s) is False, f"Expected False for {s}={int(s**0.5)}^2"

    def test_cubes_of_primes_return_true(self):
        """p^3 has exactly 3 prime factors, so should return True."""
        cubes = [p * p * p for p in [2, 3]]
        for c in cubes:
            assert is_multiply_prime(c) is True, f"Expected True for {c}={int(c**(1/3))}^3"

    def test_product_of_three_distinct_primes_return_true(self):
        """Any product of three distinct primes should return True."""
        triples = [
            (2, 3, 5),   # 30
            (2, 3, 7),   # 42
            (2, 3, 11),  # 66
            (2, 5, 7),   # 70
            (3, 5, 7),   # 105 — exceeds 100, skip
        ]
        for a, b, c in triples:
            n = a * b * c
            if n < 100:
                assert is_multiply_prime(n) is True, f"Expected True for {n}={a}*{b}*{c}"
