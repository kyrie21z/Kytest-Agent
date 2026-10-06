import pytest
from solution import is_multiply_prime


class TestIsMultiplyPrime_NormalCases:
    """Tests for typical inputs where the number is exactly the product of 3 primes."""

    def test_30(self):
        # 30 = 2 * 3 * 5
        assert is_multiply_prime(30) is True

    def test_42(self):
        # 42 = 2 * 3 * 7
        assert is_multiply_prime(42) is True

    def test_66(self):
        # 66 = 2 * 3 * 11
        assert is_multiply_prime(66) is True

    def test_70(self):
        # 70 = 2 * 5 * 7
        assert is_multiply_prime(70) is True

    def test_105(self):
        # 105 = 3 * 5 * 7
        assert is_multiply_prime(105) is True


class TestIsMultiplyPrime_BoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_a_equals_1(self):
        # 1 is not a product of any primes
        assert is_multiply_prime(1) is False

    def test_a_equals_2(self):
        # 2 is a single prime, not product of 3 primes
        assert is_multiply_prime(2) is False

    def test_a_equals_3(self):
        # 3 is a single prime
        assert is_multiply_prime(3) is False

    def test_a_equals_4(self):
        # 4 = 2 * 2, only 2 prime factors
        assert is_multiply_prime(4) is False

    def test_a_equals_8(self):
        # 8 = 2 * 2 * 2, exactly 3 prime factors (with repetition)
        assert is_multiply_prime(8) is True

    def test_a_equals_12(self):
        # 12 = 2 * 2 * 3, exactly 3 prime factors
        assert is_multiply_prime(12) is True

    def test_a_equals_27(self):
        # 27 = 3 * 3 * 3, exactly 3 prime factors
        assert is_multiply_prime(27) is True

    def test_a_equals_98(self):
        # 98 = 2 * 7 * 7, exactly 3 prime factors
        assert is_multiply_prime(98) is True

    def test_a_equals_99(self):
        # 99 = 3 * 3 * 11, exactly 3 prime factors
        assert is_multiply_prime(99) is True

    def test_a_equals_97(self):
        # 97 is prime, only 1 prime factor
        assert is_multiply_prime(97) is False


class TestIsMultiplyPrime_EmptyZeroNegativeInputs:
    """Tests for zero, negative, and edge-case small inputs."""

    def test_zero(self):
        assert is_multiply_prime(0) is False

    def test_negative_one(self):
        assert is_multiply_prime(-1) is False

    def test_negative_five(self):
        assert is_multiply_prime(-5) is False

    def test_negative_hundred(self):
        assert is_multiply_prime(-100) is False


class TestIsMultiplyPrime_TooFewPrimes:
    """Numbers with fewer than 3 prime factors should return False."""

    def test_two_primes_product(self):
        # 6 = 2 * 3
        assert is_multiply_prime(6) is False

    def test_two_same_primes(self):
        # 9 = 3 * 3
        assert is_multiply_prime(9) is False

    def test_single_prime(self):
        # 5 is prime
        assert is_multiply_prime(5) is False

    def test_another_single_prime(self):
        # 11 is prime
        assert is_multiply_prime(11) is False


class TestIsMultiplyPrime_TooManyPrimes:
    """Numbers with more than 3 prime factors should return False."""

    def test_four_primes(self):
        # 24 = 2 * 2 * 2 * 3
        assert is_multiply_prime(24) is False

    def test_four_same_primes(self):
        # 16 = 2 * 2 * 2 * 2
        assert is_multiply_prime(16) is False

    def test_five_primes(self):
        # 32 = 2 * 2 * 2 * 2 * 2
        assert is_multiply_prime(32) is False

    def test_mixed_many_primes(self):
        # 60 = 2 * 2 * 3 * 5
        assert is_multiply_prime(60) is False

    def test_210(self):
        # 210 = 2 * 3 * 5 * 7
        assert is_multiply_prime(210) is False


class TestIsMultiplyPrime_MoreValues:
    """Additional coverage for various numbers up to ~100."""

    def test_14(self):
        # 14 = 2 * 7
        assert is_multiply_prime(14) is False

    def test_15(self):
        # 15 = 3 * 5
        assert is_multiply_prime(15) is False

    def test_18(self):
        # 18 = 2 * 3 * 3
        assert is_multiply_prime(18) is True

    def test_20(self):
        # 20 = 2 * 2 * 5
        assert is_multiply_prime(20) is True

    def test_28(self):
        # 28 = 2 * 2 * 7
        assert is_multiply_prime(28) is True

    def test_33(self):
        # 33 = 3 * 11
        assert is_multiply_prime(33) is False

    def test_34(self):
        # 34 = 2 * 17
        assert is_multiply_prime(34) is False

    def test_35(self):
        # 35 = 5 * 7
        assert is_multiply_prime(35) is False

    def test_36(self):
        # 36 = 2 * 2 * 3 * 3
        assert is_multiply_prime(36) is False

    def test_50(self):
        # 50 = 2 * 5 * 5
        assert is_multiply_prime(50) is True

    def test_52(self):
        # 52 = 2 * 2 * 13
        assert is_multiply_prime(52) is True

    def test_54(self):
        # 54 = 2 * 3 * 3 * 3
        assert is_multiply_prime(54) is False

    def test_55(self):
        # 55 = 5 * 11
        assert is_multiply_prime(55) is False

    def test_65(self):
        # 65 = 5 * 13
        assert is_multiply_prime(65) is False

    def test_77(self):
        # 77 = 7 * 11
        assert is_multiply_prime(77) is False

    def test_85(self):
        # 85 = 5 * 17
        assert is_multiply_prime(85) is False

    def test_87(self):
        # 87 = 3 * 29
        assert is_multiply_prime(87) is False

    def test_91(self):
        # 91 = 7 * 13
        assert is_multiply_prime(91) is False
