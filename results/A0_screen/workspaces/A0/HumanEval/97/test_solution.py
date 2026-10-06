import pytest
from solution import multiply


class TestMultiplyBasic:
    """Tests for basic functionality of the multiply function."""

    def test_positive_integers(self):
        assert multiply(148, 412) == 16

    def test_another_positive_pair(self):
        assert multiply(19, 28) == 72

    def test_one_value_ends_in_zero(self):
        assert multiply(2020, 1851) == 0

    def test_negative_second_argument(self):
        assert multiply(14, -15) == 20


class TestMultiplyEdgeCases:
    """Tests for edge cases."""

    def test_both_negative_numbers(self):
        assert multiply(-14, -28) == 32

    def test_first_argument_is_zero(self):
        assert multiply(0, 5) == 0

    def test_second_argument_is_zero(self):
        assert multiply(5, 0) == 0

    def test_both_arguments_are_zero(self):
        assert multiply(0, 0) == 0

    def test_single_digit_numbers(self):
        assert multiply(3, 7) == 21

    def test_same_single_digit_numbers(self):
        assert multiply(5, 5) == 25

    def test_large_numbers(self):
        # 123456789 -> unit digit 9, 987654321 -> unit digit 1, product = 9
        assert multiply(123456789, 987654321) == 9

    def test_large_number_with_trailing_zeros(self):
        assert multiply(1000000, 999) == 0

    def test_negative_first_positive_second(self):
        assert multiply(-14, 15) == 20

    def test_very_large_numbers(self):
        assert multiply(999999999999, 888888888888) == 72


class TestMultiplyUnitDigitLogic:
    """Tests that verify unit digit extraction logic."""

    def test_unit_digits_product(self):
        # 123 -> unit digit 3, 456 -> unit digit 6, product = 18
        assert multiply(123, 456) == 18

    def test_unit_digit_is_one(self):
        assert multiply(111, 222) == 2

    def test_unit_digit_is_nine(self):
        assert multiply(19, 29) == 81

    def test_mixed_signs_unit_digits(self):
        # -123 -> unit digit 3, 456 -> unit digit 6, product = 18
        assert multiply(-123, 456) == 18
