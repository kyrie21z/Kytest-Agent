import pytest
from solution import greatest_common_divisor


class TestGreatestCommonDivisor:
    """Tests for the greatest_common_divisor function."""

    # --- Doctest examples from the docstring ---
    def test_gcd_3_and_5(self):
        assert greatest_common_divisor(3, 5) == 1

    def test_gcd_25_and_15(self):
        assert greatest_common_divisor(25, 15) == 5

    # --- Basic cases ---
    def test_gcd_same_number(self):
        assert greatest_common_divisor(7, 7) == 7

    def test_gcd_one_divides_other(self):
        assert greatest_common_divisor(10, 5) == 5

    def test_gcd_one_divides_other_reversed(self):
        assert greatest_common_divisor(5, 10) == 5

    def test_gcd_1_and_n(self):
        assert greatest_common_divisor(1, 100) == 1

    def test_gcd_n_and_1(self):
        assert greatest_common_divisor(100, 1) == 1

    # --- Zero edge cases ---
    def test_gcd_zero_second(self):
        assert greatest_common_divisor(10, 0) == 10

    def test_gcd_zero_first(self):
        assert greatest_common_divisor(0, 10) == 10

    def test_gcd_both_zero(self):
        assert greatest_common_divisor(0, 0) == 0

    # --- Negative numbers (implementation returns negative result when b < 0) ---
    def test_gcd_negative_a(self):
        assert greatest_common_divisor(-12, 8) == 4

    def test_gcd_negative_b(self):
        assert greatest_common_divisor(12, -8) == -4

    def test_gcd_both_negative(self):
        assert greatest_common_divisor(-12, -8) == -4

    # --- Coprime numbers ---
    def test_gcd_coprime_primes(self):
        assert greatest_common_divisor(13, 17) == 1

    def test_gcd_coprime_composites(self):
        assert greatest_common_divisor(8, 9) == 1

    def test_gcd_coprime_large(self):
        assert greatest_common_divisor(14, 15) == 1

    # --- Larger numbers ---
    def test_gcd_large_numbers(self):
        assert greatest_common_divisor(1071, 462) == 21

    def test_gcd_power_of_two(self):
        assert greatest_common_divisor(1024, 512) == 512

    def test_gcd_two_large_primes(self):
        assert greatest_common_divisor(104729, 104743) == 1

    # --- Identity and symmetry ---
    def test_gcd_symmetry(self):
        assert greatest_common_divisor(12, 8) == greatest_common_divisor(8, 12)

    def test_gcd_identity(self):
        assert greatest_common_divisor(1, 1) == 1
