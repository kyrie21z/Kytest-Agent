"""Unit tests for solution.is_prime."""

import pytest
from solution import is_prime


class TestIsPrimeDocstringExamples:
    """Test cases taken directly from the docstring."""

    def test_is_prime_6(self):
        assert is_prime(6) is False

    def test_is_prime_101(self):
        assert is_prime(101) is True

    def test_is_prime_11(self):
        assert is_prime(11) is True

    def test_is_prime_13441(self):
        assert is_prime(13441) is True

    def test_is_prime_61(self):
        assert is_prime(61) is True

    def test_is_prime_4(self):
        assert is_prime(4) is False

    def test_is_prime_1(self):
        assert is_prime(1) is False


class TestIsPrimeSmallPrimes:
    """Smallest prime numbers."""

    def test_is_prime_2(self):
        """2 is the smallest and only even prime."""
        assert is_prime(2) is True

    def test_is_prime_3(self):
        assert is_prime(3) is True

    def test_is_prime_5(self):
        assert is_prime(5) is True

    def test_is_prime_7(self):
        assert is_prime(7) is True


class TestIsPrimeSmallComposites:
    """Small composite (non-prime) numbers."""

    def test_is_prime_8(self):
        assert is_prime(8) is False

    def test_is_prime_9(self):
        assert is_prime(9) is False

    def test_is_prime_10(self):
        assert is_prime(10) is False

    def test_is_prime_15(self):
        assert is_prime(15) is False

    def test_is_prime_21(self):
        assert is_prime(21) is False

    def test_is_prime_25(self):
        assert is_prime(25) is False


class TestIsPrimeBoundaryNonPositive:
    """Inputs at or below the boundary where primality is undefined/false."""

    def test_is_prime_0(self):
        assert is_prime(0) is False

    def test_is_prime_1(self):
        assert is_prime(1) is False

    def test_is_prime_negative_1(self):
        assert is_prime(-1) is False

    def test_is_prime_negative_5(self):
        assert is_prime(-5) is False

    def test_is_prime_negative_100(self):
        assert is_prime(-100) is False


class TestIsPrimePerfectSquares:
    """Perfect squares — edge cases for the sqrt-based loop."""

    def test_is_prime_4(self):
        assert is_prime(4) is False

    def test_is_prime_9(self):
        assert is_prime(9) is False

    def test_is_prime_25(self):
        assert is_prime(25) is False

    def test_is_prime_49(self):
        assert is_prime(49) is False

    def test_is_prime_121(self):
        assert is_prime(121) is False


class TestIsPrimeLargerNumbers:
    """Larger primes and composites to exercise the sqrt loop more."""

    def test_is_prime_997(self):
        """997 is a well-known large prime."""
        assert is_prime(997) is True

    def test_is_prime_1000(self):
        assert is_prime(1000) is False

    def test_is_prime_1009(self):
        """1009 is a prime."""
        assert is_prime(1009) is True

    def test_is_prime_1001(self):
        """1001 = 7 × 11 × 13, composite."""
        assert is_prime(1001) is False

    def test_is_prime_10000(self):
        assert is_prime(10000) is False

    def test_is_prime_99991(self):
        """99991 is a prime."""
        assert is_prime(99991) is True


class TestIsPrimeEvenNumbers:
    """Even numbers: only 2 is prime."""

    def test_is_prime_even_2(self):
        assert is_prime(2) is True

    def test_is_prime_even_4(self):
        assert is_prime(4) is False

    def test_is_prime_even_10(self):
        assert is_prime(10) is False

    def test_is_prime_even_100(self):
        assert is_prime(100) is False


class TestIsPrimeOddComposites:
    """Odd composite numbers."""

    def test_is_prime_odd_composite_9(self):
        assert is_prime(9) is False

    def test_is_prime_odd_composite_15(self):
        assert is_prime(15) is False

    def test_is_prime_odd_composite_27(self):
        assert is_prime(27) is False

    def test_is_prime_odd_composite_35(self):
        assert is_prime(35) is False

    def test_is_prime_odd_composite_77(self):
        assert is_prime(77) is False


class TestIsPrimeReturnTypes:
    """Verify that the return value is strictly bool."""

    def test_return_type_true(self):
        result = is_prime(2)
        assert isinstance(result, bool)
        assert result is True

    def test_return_type_false(self):
        result = is_prime(4)
        assert isinstance(result, bool)
        assert result is False
