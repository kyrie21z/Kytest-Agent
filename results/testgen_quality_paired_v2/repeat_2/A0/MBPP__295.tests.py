import pytest
from solution import sum_div


class TestSumDivBasic:
    """Test basic functionality of sum_div."""

    def test_sum_div_6(self):
        # Divisors of 6: 1, 2, 3 => sum = 6
        assert sum_div(6) == 6

    def test_sum_div_12(self):
        # Divisors of 12: 1, 2, 3, 4, 6 => sum = 16
        assert sum_div(12) == 16

    def test_sum_div_2(self):
        # Divisors of 2: 1 => sum = 1
        assert sum_div(2) == 1

    def test_sum_div_1(self):
        # Divisors of 1: only [1] (loop range(2, 1) is empty) => sum = 1
        assert sum_div(1) == 1

    def test_sum_div_28(self):
        # Divisors of 28: 1, 2, 4, 7, 14 => sum = 28 (perfect number)
        assert sum_div(28) == 28


class TestSumDivPrimes:
    """Test with prime numbers (only proper divisor is 1)."""

    def test_prime_7(self):
        assert sum_div(7) == 1

    def test_prime_13(self):
        assert sum_div(13) == 1

    def test_prime_97(self):
        assert sum_div(97) == 1

    def test_prime_2(self):
        assert sum_div(2) == 1


class TestSumDivComposite:
    """Test with composite numbers."""

    def test_square_9(self):
        # Divisors of 9: 1, 3 => sum = 4
        assert sum_div(9) == 4

    def test_square_16(self):
        # Divisors of 16: 1, 2, 4, 8 => sum = 15
        assert sum_div(16) == 15

    def test_square_25(self):
        # Divisors of 25: 1, 5 => sum = 6
        assert sum_div(25) == 6

    def test_product_of_primes_15(self):
        # Divisors of 15: 1, 3, 5 => sum = 9
        assert sum_div(15) == 9

    def test_product_of_primes_21(self):
        # Divisors of 21: 1, 3, 7 => sum = 11
        assert sum_div(21) == 11

    def test_even_composite_18(self):
        # Divisors of 18: 1, 2, 3, 6, 9 => sum = 21
        assert sum_div(18) == 21

    def test_even_composite_30(self):
        # Divisors of 30: 1, 2, 3, 5, 6, 10, 15 => sum = 42
        assert sum_div(30) == 42


class TestSumDivEdgeCases:
    """Test edge cases."""

    def test_zero(self):
        # range(2, 0) is empty, divisors stays [1], sum = 1
        assert sum_div(0) == 1

    def test_negative_number(self):
        # range(2, -5) is empty, divisors stays [1], sum = 1
        assert sum_div(-5) == 1

    def test_large_number(self):
        # Divisors of 100: 1, 2, 4, 5, 10, 20, 25, 50 => sum = 117
        assert sum_div(100) == 117

    def test_larger_number(self):
        # Divisors of 1000: 1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, 500 => sum = 1340
        assert sum_div(1000) == 1340


class TestSumDivReturnTypes:
    """Test return types."""

    def test_returns_integer(self):
        result = sum_div(6)
        assert isinstance(result, int)

    def test_returns_non_negative(self):
        # Since divisors always include at least [1], sum is always >= 1
        assert sum_div(6) > 0
        assert sum_div(1) > 0
        assert sum_div(0) > 0


class TestSumDivKnownValues:
    """Test against known mathematical values."""

    def test_perfect_number_6(self):
        assert sum_div(6) == 6

    def test_perfect_number_28(self):
        assert sum_div(28) == 28

    def test_abundant_number_12(self):
        # 12 is abundant: sum of proper divisors (16) > 12
        assert sum_div(12) > 12

    def test_deficient_number_7(self):
        # 7 is deficient: sum of proper divisors (1) < 7
        assert sum_div(7) < 7

    def test_abundant_number_18(self):
        assert sum_div(18) > 18

    def test_deficient_number_9(self):
        assert sum_div(9) < 9
