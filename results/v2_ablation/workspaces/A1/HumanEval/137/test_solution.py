import pytest
from solution import compare_one


class TestCompareOne_NormalCases:
    """Test normal cases with typical inputs."""

    def test_two_integers(self):
        assert compare_one(1, 2) == 2

    def test_two_integers_reversed(self):
        assert compare_one(2, 1) == 2

    def test_integer_and_float(self):
        assert compare_one(1, 2.5) == 2.5

    def test_float_and_integer(self):
        assert compare_one(2.5, 1) == 2.5

    def test_two_floats(self):
        assert compare_one(3.14, 2.71) == 3.14

    def test_string_with_dot(self):
        assert compare_one("1.5", "2.5") == "2.5"

    def test_string_with_comma(self):
        assert compare_one("1,5", "2,3") == "2,3"

    def test_mixed_int_and_string_comma(self):
        assert compare_one(1, "2,3") == "2,3"

    def test_mixed_int_and_string_dot(self):
        assert compare_one(1, "2.3") == "2.3"

    def test_both_strings(self):
        assert compare_one("5,1", "6") == "6"

    def test_both_strings_dot(self):
        assert compare_one("5.1", "6.0") == "6.0"

    def test_negative_vs_positive(self):
        assert compare_one(-1, 1) == 1

    def test_positive_vs_negative(self):
        assert compare_one(1, -1) == 1


class TestCompareOne_EqualValues:
    """Test cases where values are numerically equal — should return None."""

    def test_same_integers(self):
        assert compare_one(5, 5) is None

    def test_int_and_equal_float(self):
        assert compare_one(1, 1.0) is None

    def test_float_and_equal_int(self):
        assert compare_one(1.0, 1) is None

    def test_int_and_equal_string(self):
        assert compare_one(1, "1") is None

    def test_float_and_equal_string(self):
        assert compare_one(1.0, "1") is None

    def test_string_and_equal_int(self):
        assert compare_one("1", 1) is None

    def test_string_and_equal_float(self):
        assert compare_one("1", 1.0) is None

    def test_string_comma_equals_string_dot(self):
        assert compare_one("1,0", "1.0") is None

    def test_string_comma_equals_string_comma(self):
        assert compare_one("3,14", "3,14") is None

    def test_string_dot_equals_string_dot(self):
        assert compare_one("3.14", "3.14") is None

    def test_zero_vs_zero(self):
        assert compare_one(0, 0) is None

    def test_zero_vs_string_zero(self):
        assert compare_one(0, "0") is None

    def test_string_zero_vs_int_zero(self):
        assert compare_one("0", 0) is None

    def test_string_zero_comma_vs_int(self):
        assert compare_one("0,0", 0) is None

    def test_trailing_zeros_equivalence(self):
        assert compare_one("1,00", "1.0") is None


class TestCompareOne_BoundaryCases:
    """Test boundary cases at the edges of valid input ranges."""

    def test_negative_numbers(self):
        assert compare_one(-1, -2) == -1

    def test_negative_numbers_reversed(self):
        assert compare_one(-2, -1) == -1

    def test_negative_vs_positive(self):
        assert compare_one(-5, 3) == 3

    def test_positive_vs_negative(self):
        assert compare_one(3, -5) == 3

    def test_large_numbers(self):
        assert compare_one(999999, 1000000) == 1000000

    def test_small_decimals(self):
        assert compare_one(0.001, 0.002) == 0.002

    def test_very_small_decimal_string(self):
        assert compare_one("0,001", "0,002") == "0,002"

    def test_equal_negatives(self):
        assert compare_one(-3, -3) is None

    def test_negative_int_vs_positive_string(self):
        assert compare_one(-1, "5") == "5"

    def test_negative_string_vs_positive_int(self):
        assert compare_one("-1,5", 3) == 3

    def test_negative_string_vs_negative_string(self):
        assert compare_one("-1,5", "-2,3") == "-1,5"

    def test_zero_boundary(self):
        assert compare_one(0, 1) == 1

    def test_zero_boundary_reversed(self):
        assert compare_one(1, 0) == 1

    def test_negative_zero_vs_positive(self):
        assert compare_one(-0.0, 0.0) is None


class TestCompareOne_ReturnTypePreservation:
    """Verify that the returned value preserves the original type of the larger input."""

    def test_returns_int_when_int_is_larger(self):
        result = compare_one(5, 3)
        assert result == 5
        assert isinstance(result, int)

    def test_returns_float_when_float_is_larger(self):
        result = compare_one(3, 5.5)
        assert result == 5.5
        assert isinstance(result, float)

    def test_returns_string_when_string_is_larger(self):
        result = compare_one(3, "5,5")
        assert result == "5,5"
        assert isinstance(result, str)

    def test_returns_first_arg_type_when_first_is_larger(self):
        result = compare_one("10", 5)
        assert result == "10"
        assert isinstance(result, str)

    def test_returns_second_arg_type_when_second_is_larger(self):
        result = compare_one(5, "10")
        assert result == "10"
        assert isinstance(result, str)


class TestCompareOne_ExceptionCases:
    """Test cases where invalid inputs cause exceptions."""

    def test_non_numeric_string_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one("abc", 5)

    def test_non_numeric_string_on_other_side_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one(5, "xyz")

    def test_both_non_numeric_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one("abc", "def")

    def test_mixed_numeric_and_non_numeric_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one(5, "not_a_number")


class TestCompareOne_EmptyAndSpecialInputs:
    """Test edge cases with empty, whitespace, or special string inputs."""

    def test_empty_string_vs_number_raises_value_error(self):
        # "" becomes "." after replace(",", "."), and float(".") raises ValueError
        with pytest.raises(ValueError):
            compare_one("", "5")

    def test_empty_string_vs_zero_raises_value_error(self):
        # "" becomes "." after replace, which raises ValueError
        with pytest.raises(ValueError):
            compare_one("", 0)

    def test_whitespace_string(self):
        # " 5" parses as 5.0
        assert compare_one(" 5", "3") == " 5"

    def test_string_with_multiple_commas(self):
        # "1,2,3" -> "1.2.3" which raises ValueError
        with pytest.raises(ValueError):
            compare_one("1,2,3", "5")

    def test_string_only_comma(self):
        # "," -> "." which raises ValueError
        with pytest.raises(ValueError):
            compare_one(",", "5")

    def test_negative_string_with_comma(self):
        assert compare_one("-1,5", "-0,5") == "-0,5"

    def test_large_string_numbers(self):
        assert compare_one("1000000", "999999") == "1000000"
