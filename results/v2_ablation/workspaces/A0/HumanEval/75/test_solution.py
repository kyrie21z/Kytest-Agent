import pytest
from solution import is_multiply_prime


class TestIsMultiplyPrime:
    """Tests for the is_multiply_prime function."""

    # --- Known True cases: products of exactly 3 primes ---

    def test_30(self):
        """30 = 2 * 3 * 5"""
        assert is_multiply_prime(30) is True

    def test_8(self):
        """8 = 2 * 2 * 2"""
        assert is_multiply_prime(8) is True

    def test_12(self):
        """12 = 2 * 2 * 3"""
        assert is_multiply_prime(12) is True

    def test_42(self):
        """42 = 2 * 3 * 7"""
        assert is_multiply_prime(42) is True

    def test_27(self):
        """27 = 3 * 3 * 3"""
        assert is_multiply_prime(27) is True

    def test_20(self):
        """20 = 2 * 2 * 5"""
        assert is_multiply_prime(20) is True

    def test_52(self):
        """52 = 2 * 2 * 13"""
        assert is_multiply_prime(52) is True

    def test_98(self):
        """98 = 2 * 7 * 7"""
        assert is_multiply_prime(98) is True

    def test_105(self):
        """105 = 3 * 5 * 7"""
        assert is_multiply_prime(105) is True

    def test_125(self):
        """125 = 5 * 5 * 5"""
        assert is_multiply_prime(125) is True

    # --- Known False cases: not a product of exactly 3 primes ---

    def test_60(self):
        """60 = 2 * 2 * 3 * 5 — four primes, not three"""
        assert is_multiply_prime(60) is False

    def test_100(self):
        """100 = 2 * 2 * 5 * 5 — four primes"""
        assert is_multiply_prime(100) is False

    def test_14(self):
        """14 = 2 * 7 — only two primes"""
        assert is_multiply_prime(14) is False

    def test_6(self):
        """6 = 2 * 3 — only two primes"""
        assert is_multiply_prime(6) is False

    def test_1(self):
        """1 is not a product of any primes"""
        assert is_multiply_prime(1) is False

    def test_0(self):
        """0 is not a product of any primes"""
        assert is_multiply_prime(0) is False

    def test_negative(self):
        """Negative numbers are not products of primes"""
        assert is_multiply_prime(-5) is False

    def test_2(self):
        """2 is a single prime, not a product of 3"""
        assert is_multiply_prime(2) is False

    def test_3(self):
        """3 is a single prime, not a product of 3"""
        assert is_multiply_prime(3) is False

    def test_4(self):
        """4 = 2 * 2 — only two primes"""
        assert is_multiply_prime(4) is False

    def test_9(self):
        """9 = 3 * 3 — only two primes"""
        assert is_multiply_prime(9) is False

    def test_16(self):
        """16 = 2^4 — four primes"""
        assert is_multiply_prime(16) is False

    def test_24(self):
        """24 = 2 * 2 * 2 * 3 — four primes"""
        assert is_multiply_prime(24) is False

    def test_35(self):
        """35 = 5 * 7 — only two primes"""
        assert is_multiply_prime(35) is False

    def test_77(self):
        """77 = 7 * 11 — only two primes"""
        assert is_multiply_prime(77) is False

    def test_216(self):
        """216 = 2^3 * 3^3 — six primes"""
        assert is_multiply_prime(216) is False
