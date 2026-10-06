import pytest
from solution import is_multiply_prime


class TestIsMultiplyPrime_NormalCases:
    """Tests where the input is the product of exactly 3 distinct or repeated primes."""

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

    def test_42(self):
        # 42 = 2 * 3 * 7
        assert is_multiply_prime(42) is True

    def test_105(self):
        # 105 = 3 * 5 * 7
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

    def test_16(self):
        # 16 = 2 * 2 * 2 * 2 -> 4 primes
        assert is_multiply_prime(16) is False

    def test_24(self):
        # 24 = 2 * 2 * 2 * 3 -> 4 primes
        assert is_multiply_prime(24) is False


class TestIsMultiplyPrime_FalseCases:
    """Tests where the input is NOT the product of exactly 3 primes."""

    def test_6(self):
        # 6 = 2 * 3 -> only 2 primes
        assert is_multiply_prime(6) is False

    def test_10(self):
        # 10 = 2 * 5 -> only 2 primes
        assert is_multiply_prime(10) is False

    def test_14(self):
        # 14 = 2 * 7 -> only 2 primes
        assert is_multiply_prime(14) is False

    def test_100(self):
        # 100 = 2 * 2 * 5 * 5 -> 4 primes
        assert is_multiply_prime(100) is False

    def test_210(self):
        # 210 = 2 * 3 * 5 * 7 -> 4 primes
        assert is_multiply_prime(210) is False

    def test_7(self):
        # 7 is prime -> only 1 prime factor
        assert is_multiply_prime(7) is False

    def test_2(self):
        # 2 is prime -> only 1 prime factor
        assert is_multiply_prime(2) is False

    def test_3(self):
        # 3 is prime -> only 1 prime factor
        assert is_multiply_prime(3) is False

    def test_4(self):
        # 4 = 2 * 2 -> only 2 primes
        assert is_multiply_prime(4) is False

    def test_9(self):
        # 9 = 3 * 3 -> only 2 primes
        assert is_multiply_prime(9) is False

    def test_15(self):
        # 15 = 3 * 5 -> only 2 primes
        assert is_multiply_prime(15) is False

    def test_18(self):
        # 18 = 2 * 3 * 3 -> 3 primes
        assert is_multiply_prime(18) is True

    def test_20(self):
        # 20 = 2 * 2 * 5 -> 3 primes
        assert is_multiply_prime(20) is True

    def test_52(self):
        # 52 = 2 * 2 * 13 -> 3 primes
        assert is_multiply_prime(52) is True

    def test_84(self):
        # 84 = 2 * 2 * 3 * 7 -> 4 primes
        assert is_multiply_prime(84) is False


class TestIsMultiplyPrime_BoundaryAndEdgeCases:
    """Tests at boundaries and edge values."""

    def test_zero(self):
        # 0 <= 1, returns False immediately
        assert is_multiply_prime(0) is False

    def test_one(self):
        # 1 <= 1, returns False immediately
        assert is_multiply_prime(1) is False

    def test_negative_one(self):
        # negative numbers are <= 1
        assert is_multiply_prime(-1) is False

    def test_negative_five(self):
        assert is_multiply_prime(-5) is False

    def test_two(self):
        # smallest prime, only 1 factor
        assert is_multiply_prime(2) is False

    def test_largest_three_prime_product_under_100(self):
        # 98 = 2 * 7 * 7 and 99 = 3 * 3 * 11
        assert is_multiply_prime(98) is True
        assert is_multiply_prime(99) is True


class TestIsMultiplyPrime_TypeHandling:
    """Tests for non-standard input types."""

    def test_float_input(self):
        # Float input causes TypeError in list multiplication
        with pytest.raises(TypeError):
            is_multiply_prime(30.0)

    def test_string_input(self):
        # String input will likely cause TypeError; just ensure no silent failure
        with pytest.raises((TypeError, ValueError)):
            is_multiply_prime("30")

    def test_none_input(self):
        with pytest.raises(TypeError):
            is_multiply_prime(None)

    def test_list_input(self):
        with pytest.raises(TypeError):
            is_multiply_prime([30])
