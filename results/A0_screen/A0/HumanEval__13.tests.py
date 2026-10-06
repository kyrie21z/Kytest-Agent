import pytest
from solution import greatest_common_divisor


class TestGreatestCommonDivisor:
    """Unit tests for the greatest_common_divisor function."""

    # --- Docstring examples ---
    def test_docstring_example_1(self):
        assert greatest_common_divisor(3, 5) == 1

    def test_docstring_example_2(self):
        assert greatest_common_divisor(25, 15) == 5

    # --- Basic positive integers ---
    def test_basic_gcd(self):
        assert greatest_common_divisor(12, 8) == 4

    def test_gcd_one_divides_other(self):
        assert greatest_common_divisor(10, 5) == 5

    def test_gcd_equal_numbers(self):
        assert greatest_common_divisor(7, 7) == 7

    def test_gcd_coprime_numbers(self):
        assert greatest_common_divisor(13, 17) == 1

    def test_gcd_with_prime(self):
        assert greatest_common_divisor(11, 22) == 11

    # --- Edge cases involving zero ---
    def test_gcd_zero_second(self):
        assert greatest_common_divisor(5, 0) == 5

    def test_gcd_zero_first(self):
        assert greatest_common_divisor(0, 5) == 5

    def test_gcd_both_zero(self):
        assert greatest_common_divisor(0, 0) == 0

    # --- Negative numbers ---
    def test_gcd_negative_first(self):
        assert greatest_common_divisor(-12, 8) == 4

    def test_gcd_negative_second(self):
        # The function returns a negative result when b < 0 and a % b != 0
        assert greatest_common_divisor(12, -8) == -4

    def test_gcd_both_negative(self):
        # The function returns a negative result when both args are negative
        assert greatest_common_divisor(-12, -8) == -4

    def test_gcd_one_negative_coprime(self):
        assert greatest_common_divisor(-3, 5) == 1

    # --- Larger numbers ---
    def test_gcd_large_numbers(self):
        assert greatest_common_divisor(1071, 462) == 21

    def test_gcd_large_coprime(self):
        assert greatest_common_divisor(1000000007, 999999937) == 1

    def test_gcd_power_of_two(self):
        assert greatest_common_divisor(256, 128) == 128

    # --- One argument is 1 ---
    def test_gcd_with_one(self):
        assert greatest_common_divisor(1, 100) == 1

    def test_gcd_one_and_one(self):
        assert greatest_common_divisor(1, 1) == 1

    # --- Type checking ---
    def test_returns_int(self):
        result = greatest_common_divisor(25, 15)
        assert isinstance(result, int)
