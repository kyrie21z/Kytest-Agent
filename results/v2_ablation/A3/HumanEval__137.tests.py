"""Unit tests for compare_one in solution.py."""

import pytest
from solution import compare_one


class TestCompareOne_NormalCases:
    """Tests with typical, well-formed inputs."""

    def test_int_vs_float(self):
        assert compare_one(1, 2.5) == 2.5

    def test_int_vs_string_comma_decimal(self):
        assert compare_one(1, "2,3") == "2,3"

    def test_string_vs_string(self):
        assert compare_one("5,1", "6") == "6"

    def test_float_vs_int(self):
        assert compare_one(3.0, 2) == 3.0

    def test_negative_numbers(self):
        assert compare_one(-1, -2) == -1

    def test_same_type_integers(self):
        assert compare_one(5, 3) == 5

    def test_same_type_floats(self):
        assert compare_one(3.14, 2.71) == 3.14

    def test_string_decimal_with_dot(self):
        assert compare_one("3.5", "2.9") == "3.5"

    def test_string_decimal_with_comma(self):
        assert compare_one("3,5", "2,9") == "3,5"

    def test_int_positive_vs_negative(self):
        assert compare_one(5, -3) == 5

    def test_float_positive_vs_negative(self):
        assert compare_one(0.5, -1.5) == 0.5

    def test_string_comma_greater_than_string_dot(self):
        # "1,5" = 1.5 > "1.2" = 1.2
        assert compare_one("1,5", "1.2") == "1,5"

    def test_string_dot_greater_than_string_comma(self):
        # "2.9" = 2.9 > "2,5" = 2.5
        assert compare_one("2.9", "2,5") == "2.9"


class TestCompareOne_BoundaryCases:
    """Tests at edges of valid input ranges."""

    def test_zero_vs_positive(self):
        assert compare_one(0, 1) == 1

    def test_zero_vs_negative(self):
        assert compare_one(0, -1) == 0

    def test_equal_zeros(self):
        assert compare_one(0, 0) is None

    def test_very_close_floats(self):
        assert compare_one(1.0, 1.0000001) == 1.0000001

    def test_large_numbers(self):
        assert compare_one(1000000, 999999) == 1000000

    def test_equal_int_and_float_value(self):
        # 1 == 1.0 numerically
        assert compare_one(1, 1.0) is None

    def test_equal_int_and_string_value(self):
        assert compare_one("1", 1) is None

    def test_equal_string_values(self):
        assert compare_one("5", "5") is None

    def test_equal_string_with_comma_and_dot(self):
        assert compare_one("3,14", "3.14") is None

    def test_negative_equal(self):
        assert compare_one(-2.5, "-2,5") is None

    def test_smallest_positive_vs_larger(self):
        assert compare_one(0.001, 0.01) == 0.01

    def test_large_negative(self):
        assert compare_one(-1000000, -999999) == -999999


class TestCompareOne_EqualValues:
    """Tests where both values represent the same number."""

    def test_same_integer(self):
        assert compare_one(42, 42) is None

    def test_same_float(self):
        assert compare_one(7.7, 7.7) is None

    def test_same_string(self):
        assert compare_one("10", "10") is None

    def test_int_equals_string_number(self):
        assert compare_one(7, "7") is None

    def test_float_equals_string_number(self):
        assert compare_one(3.0, "3") is None

    def test_string_comma_equals_string_dot(self):
        assert compare_one("2,5", "2.5") is None

    def test_int_equals_string_comma(self):
        assert compare_one(5, "5,0") is None


class TestCompareOne_InvalidInputs:
    """Tests with inputs that cannot be parsed as numbers."""

    def test_non_numeric_string_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one("abc", 1)

    def test_non_numeric_string_second_arg_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one(1, "xyz")

    def test_both_non_numeric_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one("hello", "world")

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one("", 1)

    def test_mixed_valid_invalid(self):
        with pytest.raises(ValueError):
            compare_one(1, "not_a_number")


class TestCompareOne_ReturnTypePreservation:
    """Tests that the returned value preserves the original type."""

    def test_returns_original_float(self):
        result = compare_one(1, 2.5)
        assert isinstance(result, float)
        assert result == 2.5

    def test_returns_original_int(self):
        result = compare_one(1.5, 3)
        assert isinstance(result, int)
        assert result == 3

    def test_returns_original_string(self):
        result = compare_one(1, "4,5")
        assert isinstance(result, str)
        assert result == "4,5"

    def test_returns_none_when_equal(self):
        result = compare_one(1, 1)
        assert result is None
