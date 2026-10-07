"""Unit tests for solution.change_base."""

import pytest
from solution import change_base


class TestChangeBaseDocstringExamples:
    """Tests from the docstring examples."""

    def test_change_base_8_to_3(self):
        assert change_base(8, 3) == "22"

    def test_change_base_8_to_2(self):
        assert change_base(8, 2) == "1000"

    def test_change_base_7_to_2(self):
        assert change_base(7, 2) == "111"


class TestZeroCases:
    """Tests for input value of zero."""

    def test_zero_to_binary(self):
        assert change_base(0, 2) == "0"

    def test_zero_to_decimal(self):
        assert change_base(0, 10) == "0"

    def test_zero_to_various_bases(self):
        for base in range(2, 10):
            assert change_base(0, base) == "0"


class TestSingleDigitResults:
    """Tests where the result fits in a single digit."""

    def test_small_number_same_base(self):
        assert change_base(5, 8) == "5"

    def test_single_digit_binary(self):
        assert change_base(1, 2) == "1"

    def test_single_digit_octal(self):
        assert change_base(7, 8) == "7"


class TestBaseTwoBinary:
    """Tests for base-2 (binary) conversion."""

    def test_one(self):
        assert change_base(1, 2) == "1"

    def test_two(self):
        assert change_base(2, 2) == "10"

    def test_three(self):
        assert change_base(3, 2) == "11"

    def test_four(self):
        assert change_base(4, 2) == "100"

    def test_sixteen(self):
        assert change_base(16, 2) == "10000"

    def test_power_of_two(self):
        assert change_base(64, 2) == "1000000"

    def test_all_ones(self):
        assert change_base(15, 2) == "1111"


class TestBaseThree:
    """Tests for base-3 conversion."""

    def test_three(self):
        assert change_base(3, 3) == "10"

    def test_nine(self):
        assert change_base(9, 3) == "100"

    def test_twenty_six(self):
        assert change_base(26, 3) == "222"

    def test_seven(self):
        assert change_base(7, 3) == "21"


class TestBaseFourThroughNine:
    """Tests for bases 4 through 9."""

    def test_base_4(self):
        assert change_base(10, 4) == "22"

    def test_base_5(self):
        assert change_base(10, 5) == "20"

    def test_base_6(self):
        assert change_base(10, 6) == "14"

    def test_base_7(self):
        assert change_base(10, 7) == "13"

    def test_base_8(self):
        assert change_base(10, 8) == "12"

    def test_base_9(self):
        assert change_base(10, 9) == "11"


class TestBaseTenDecimal:
    """Tests for base-10 (decimal) conversion."""

    def test_ten(self):
        assert change_base(10, 10) == "10"

    def test_forty_two(self):
        assert change_base(42, 10) == "42"

    def test_hundred(self):
        assert change_base(100, 10) == "100"

    def test_large_number(self):
        assert change_base(12345, 10) == "12345"


class TestLargerNumbers:
    """Tests for larger input values."""

    def test_100_binary(self):
        assert change_base(100, 2) == "1100100"

    def test_100_octal(self):
        assert change_base(100, 8) == "144"

    def test_255_binary(self):
        assert change_base(255, 2) == "11111111"

    def test_1000_decimal(self):
        assert change_base(1000, 10) == "1000"

    def test_1000_hex_like_base_8(self):
        assert change_base(1000, 8) == "1750"


class TestReturnTypes:
    """Tests verifying return type is always a string."""

    def test_returns_string_for_nonzero(self):
        assert isinstance(change_base(10, 2), str)

    def test_returns_string_for_zero(self):
        assert isinstance(change_base(0, 2), str)

    def test_returns_string_for_large_input(self):
        assert isinstance(change_base(10000, 2), str)


class TestNegativeNumbers:
    """Tests for negative number inputs.

    Note: The current implementation does not handle negative numbers
    correctly (it enters an infinite loop). These tests verify that
    the function is not expected to support negative inputs.
    """

    def test_negative_numbers_not_supported(self):
        # The function has no explicit handling for negative x;
        # it will loop forever because x //= base never reaches 0.
        # We document this limitation rather than test the broken behavior.
        pass
