import pytest
from solution import compare_one


class TestCompareOneBasicTypes:
    """Tests with int and float inputs."""

    def test_int_vs_float_smaller(self):
        assert compare_one(1, 2.5) == 2.5

    def test_int_vs_float_equal(self):
        assert compare_one(1, 1.0) is None

    def test_float_vs_int_larger(self):
        assert compare_one(3.7, 2) == 3.7

    def test_two_ints_first_larger(self):
        assert compare_one(5, 3) == 5

    def test_two_ints_second_larger(self):
        assert compare_one(2, 7) == 7

    def test_two_ints_equal(self):
        assert compare_one(4, 4) is None

    def test_negative_numbers_first_larger(self):
        assert compare_one(-1, -5) == -1

    def test_negative_numbers_second_larger(self):
        assert compare_one(-10, -3) == -3

    def test_negative_and_positive(self):
        assert compare_one(-1, 1) == 1

    def test_zero_vs_positive(self):
        assert compare_one(0, 5) == 5

    def test_zero_vs_negative(self):
        assert compare_one(0, -3) == 0

    def test_both_zeros(self):
        assert compare_one(0, 0) is None

    def test_large_numbers(self):
        assert compare_one(1000000, 999999) == 1000000

    def test_small_floats(self):
        assert compare_one(0.001, 0.002) == 0.002


class TestCompareOneStringInputs:
    """Tests with string inputs using '.' as decimal separator."""

    def test_string_vs_string_dot(self):
        assert compare_one("1.5", "2.3") == "2.3"

    def test_string_vs_string_equal(self):
        assert compare_one("3.0", "3") is None

    def test_string_vs_int(self):
        assert compare_one("5.1", 4) == "5.1"

    def test_int_vs_string(self):
        assert compare_one(6, "5.9") == 6

    def test_string_with_trailing_zeros(self):
        assert compare_one("1.00", "1") is None

    def test_string_decimal_comparison(self):
        assert compare_one("0.1", "0.2") == "0.2"


class TestCompareOneCommaDecimalSeparator:
    """Tests with string inputs using ',' as decimal separator."""

    def test_comma_vs_int(self):
        assert compare_one(1, "2,3") == "2,3"

    def test_comma_vs_string(self):
        assert compare_one("5,1", "6") == "6"

    def test_comma_vs_comma(self):
        assert compare_one("3,5", "4,2") == "4,2"

    def test_comma_vs_comma_equal(self):
        assert compare_one("2,5", "2,5") is None

    def test_comma_vs_int_equal(self):
        assert compare_one("3,0", 3) is None

    def test_comma_vs_int_larger(self):
        assert compare_one("7,8", 5) == "7,8"

    def test_comma_vs_int_smaller(self):
        assert compare_one("1,5", 3) == 3


class TestCompareOneMixedTypes:
    """Tests mixing different input types."""

    def test_int_vs_string_comma(self):
        assert compare_one(1, "2,3") == "2,3"

    def test_float_vs_string_comma(self):
        assert compare_one(2.0, "1,9") == 2.0

    def test_string_dot_vs_string_comma(self):
        assert compare_one("3.5", "4,0") == "4,0"

    def test_string_comma_vs_string_dot(self):
        assert compare_one("4,0", "3.5") == "4,0"

    def test_negative_string_vs_positive_int(self):
        assert compare_one("-1,5", 2) == 2

    def test_negative_string_vs_negative_int(self):
        assert compare_one("-3,5", -2) == -2


class TestCompareOneEdgeCases:
    """Edge cases and boundary conditions."""

    def test_very_small_difference(self):
        assert compare_one(1.0, 1.0000001) == 1.0000001

    def test_very_large_numbers(self):
        assert compare_one(1e10, 1e9) == 1e10

    def test_string_with_spaces(self):
        # str() on a number doesn't add spaces, but test anyway
        assert compare_one("1.5", "2.5") == "2.5"

    def test_single_digit_strings(self):
        assert compare_one("1", "9") == "9"

    def test_string_zero_vs_int_zero(self):
        assert compare_one("0", 0) is None

    def test_string_negative_vs_int(self):
        assert compare_one("-5", -3) == -3

    def test_multiple_decimals_in_string(self):
        # Only first valid parse matters; str.replace handles commas
        assert compare_one("1,234", "1,235") == "1,235"


class TestCompareOneReturnTypes:
    """Verify return types match input types."""

    def test_returns_original_type_int(self):
        result = compare_one(5, 3)
        assert isinstance(result, int)
        assert result == 5

    def test_returns_original_type_float(self):
        result = compare_one(3, 5.0)
        assert isinstance(result, float)
        assert result == 5.0

    def test_returns_original_type_string(self):
        result = compare_one("5", 3)
        assert isinstance(result, str)
        assert result == "5"

    def test_returns_none_on_equality(self):
        result = compare_one(1, 1.0)
        assert result is None

    def test_returns_none_on_string_equality(self):
        result = compare_one("3", 3)
        assert result is None
