import pytest
from solution import compare_one


class TestCompareOne_NormalCases:
    """Test normal/typical inputs."""

    def test_two_integers(self):
        assert compare_one(1, 2) == 2

    def test_integer_smaller(self):
        assert compare_one(10, 20) == 20

    def test_integer_equal_order(self):
        assert compare_one(20, 10) == 20

    def test_integer_and_float(self):
        assert compare_one(1, 2.5) == 2.5

    def test_float_and_integer(self):
        assert compare_one(2.5, 1) == 2.5

    def test_two_floats(self):
        assert compare_one(1.5, 2.5) == 2.5

    def test_float_smaller(self):
        assert compare_one(0.1, 0.2) == 0.2

    def test_string_vs_integer(self):
        assert compare_one(1, "2,3") == "2,3"

    def test_string_vs_integer_reversed(self):
        assert compare_one("2,3", 1) == "2,3"

    def test_two_strings_comma_sep(self):
        assert compare_one("5,1", "6") == "6"

    def test_two_strings_dot_sep(self):
        assert compare_one("5.1", "6.0") == "6.0"

    def test_mixed_separators(self):
        assert compare_one("1.5", "2,5") == "2,5"

    def test_float_vs_string(self):
        assert compare_one(1.5, "2,3") == "2,3"

    def test_string_vs_float(self):
        assert compare_one("2,3", 1.5) == "2,3"


class TestCompareOne_EqualValues:
    """Test cases where values are numerically equal — should return None."""

    def test_same_integers(self):
        assert compare_one(5, 5) is None

    def test_integer_and_equivalent_string_with_comma(self):
        assert compare_one("1", 1) is None

    def test_integer_and_equivalent_string_with_dot(self):
        assert compare_one("1.0", 1) is None

    def test_float_and_equivalent_string_with_comma(self):
        assert compare_one(1.5, "1,5") is None

    def test_float_and_equivalent_string_with_dot(self):
        assert compare_one(1.5, "1.5") is None

    def test_two_strings_different_separators(self):
        assert compare_one("1.5", "1,5") is None

    def test_zero_cases(self):
        assert compare_one(0, 0) is None

    def test_zero_and_string_zero(self):
        assert compare_one(0, "0") is None

    def test_zero_and_string_zero_comma(self):
        assert compare_one(0, "0,0") is None

    def test_negative_zero(self):
        assert compare_one(-0, 0) is None

    def test_trailing_zeros(self):
        assert compare_one(1.0, "1,00") is None


class TestCompareOne_BoundaryCases:
    """Test edge-of-range valid inputs."""

    def test_both_negative(self):
        assert compare_one(-5, -3) == -3

    def test_both_negative_strings(self):
        assert compare_one("-5,1", "-6") == "-5,1"

    def test_negative_vs_positive(self):
        assert compare_one(-1, 1) == 1

    def test_positive_vs_negative(self):
        assert compare_one(1, -1) == 1

    def test_very_small_difference(self):
        assert compare_one(1.0, 1.0000001) == 1.0000001

    def test_large_numbers(self):
        assert compare_one(1000000, 999999) == 1000000

    def test_large_numbers_reversed(self):
        assert compare_one(999999, 1000000) == 1000000

    def test_very_small_positive(self):
        assert compare_one(0.0001, 0.0002) == 0.0002

    def test_equal_negatives(self):
        assert compare_one(-3, -3) is None

    def test_string_negative_vs_integer(self):
        assert compare_one("-1,5", -2) == "-1,5"

    def test_integer_vs_string_negative(self):
        assert compare_one(-2, "-1,5") == "-1,5"


class TestCompareOne_ZeroAndSingleDigit:
    """Test boundary values around zero and single digits."""

    def test_zero_vs_positive(self):
        assert compare_one(0, 1) == 1

    def test_positive_vs_zero(self):
        assert compare_one(1, 0) == 1

    def test_zero_vs_string_positive(self):
        assert compare_one(0, "1,0") == "1,0"

    def test_single_digit_strings(self):
        assert compare_one("3", "7") == "7"

    def test_single_digit_vs_multi(self):
        assert compare_one("9", "10") == "10"

    def test_one_vs_one_point_zero(self):
        assert compare_one(1, "1,0") is None


class TestCompareOne_ReturnTypePreservation:
    """Verify the returned value keeps its original type."""

    def test_returns_original_int_type(self):
        result = compare_one(1, 2)
        assert isinstance(result, int)
        assert result == 2

    def test_returns_original_float_type(self):
        result = compare_one(1, 2.5)
        assert isinstance(result, float)
        assert result == 2.5

    def test_returns_original_string_type(self):
        result = compare_one(1, "2,3")
        assert isinstance(result, str)
        assert result == "2,3"

    def test_returns_none_when_equal(self):
        result = compare_one(1, 1)
        assert result is None

    def test_returns_none_type_is_none(self):
        result = compare_one("1.5", "1,5")
        assert result is None
