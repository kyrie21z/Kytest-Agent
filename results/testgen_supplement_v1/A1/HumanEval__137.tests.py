"""Unit tests for compare_one in solution.py."""

import pytest
from solution import compare_one


# ---------------------------------------------------------------------------
# 1. Normal cases – typical inputs
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with straightforward, typical inputs."""

    def test_int_vs_int(self):
        assert compare_one(1, 2) == 2

    def test_int_vs_int_reversed(self):
        assert compare_one(2, 1) == 2

    def test_int_vs_float(self):
        assert compare_one(1, 2.5) == 2.5

    def test_float_vs_int(self):
        assert compare_one(2.5, 1) == 2.5

    def test_float_vs_float(self):
        assert compare_one(1.5, 2.5) == 2.5

    def test_string_with_comma_vs_int(self):
        assert compare_one(1, "2,3") == "2,3"

    def test_string_with_comma_vs_string(self):
        assert compare_one("5,1", "6") == "6"

    def test_string_with_dot_vs_string(self):
        assert compare_one("1.5", "2.0") == "2.0"

    def test_negative_integers(self):
        assert compare_one(-1, -2) == -1

    def test_negative_vs_positive(self):
        assert compare_one(-1, 1) == 1

    def test_negative_float_vs_positive_int(self):
        assert compare_one(-1.5, 1) == 1

    def test_both_negative_strings(self):
        assert compare_one("-3", "-1") == "-1"

    def test_large_numbers(self):
        assert compare_one(1e100, 1e99) == 1e100

    def test_equal_large_numbers(self):
        assert compare_one(1e100, 1e100) is None

    def test_zero_vs_positive(self):
        assert compare_one(0, 1) == 1

    def test_zero_vs_negative(self):
        assert compare_one(0, -1) == 0

    def test_two_zeros(self):
        assert compare_one(0, 0) is None


# ---------------------------------------------------------------------------
# 2. Boundary cases – edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries of valid input ranges."""

    def test_equal_across_types_int_and_string(self):
        # Same numeric value but different types
        assert compare_one("1", 1) is None

    def test_equal_across_types_float_and_int(self):
        assert compare_one(1.0, 1) is None

    def test_equal_across_types_string_comma_and_int(self):
        assert compare_one("2,0", 2) is None

    def test_equal_across_types_string_dot_and_float(self):
        assert compare_one("3.14", 3.14) is None

    def test_very_small_positive_vs_zero(self):
        assert compare_one(0, 1e-308) == 1e-308

    def test_very_small_negative_vs_zero(self):
        assert compare_one(-1e-308, 0) == 0

    def test_equal_strings_with_different_decimal_formats(self):
        # "1,5" and 1.5 are numerically equal
        assert compare_one("1,5", 1.5) is None

    def test_equal_strings_dot_vs_comma(self):
        assert compare_one("1.5", "1,5") is None

    def test_string_zero_vs_numeric_zero(self):
        assert compare_one("0", 0) is None

    def test_string_comma_zero_vs_numeric_zero(self):
        assert compare_one("0,0", 0) is None

    def test_string_zero_dot_vs_numeric_zero(self):
        assert compare_one("0.0", 0) is None


# ---------------------------------------------------------------------------
# 3. Empty, null, or zero-size inputs
# ---------------------------------------------------------------------------

class TestEmptyAndZeroInputs:
    """Tests involving zero-like or empty-string representations."""

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one("", 1)

    def test_two_empty_strings_raise_value_error(self):
        with pytest.raises(ValueError):
            compare_one("", "")

    def test_zero_string_vs_zero_string(self):
        assert compare_one("0", "0") is None

    def test_zero_comma_string_vs_zero_string(self):
        assert compare_one("0,0", "0") is None

    def test_zero_dot_string_vs_zero_string(self):
        assert compare_one("0.0", "0") is None


# ---------------------------------------------------------------------------
# 4. Invalid inputs – non-numeric strings
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests where inputs cannot be meaningfully compared as numbers."""

    def test_non_numeric_string_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one("abc", 1)

    def test_two_non_numeric_strings_raise_value_error(self):
        with pytest.raises(ValueError):
            compare_one("abc", "def")

    def test_mixed_valid_and_invalid_raises_value_error(self):
        with pytest.raises(ValueError):
            compare_one("123", "xyz")

    def test_special_float_inf_is_valid(self):
        # float("inf") is a valid Python float; inf > 1
        result = compare_one("inf", 1)
        assert result == "inf"

    def test_special_float_nan_is_valid(self):
        # float("nan") is accepted by float(), though comparisons are weird.
        # nan > 1 is False, so b (1) is returned.
        result = compare_one("nan", 1)
        assert result == 1


# ---------------------------------------------------------------------------
# 5. Return type preservation
# ---------------------------------------------------------------------------

class TestReturnTypePreservation:
    """Ensure the returned value preserves its original type."""

    def test_returns_original_int_type(self):
        result = compare_one(1, 2)
        assert result == 2
        assert isinstance(result, int)

    def test_returns_original_float_type(self):
        result = compare_one(1, 2.5)
        assert result == 2.5
        assert isinstance(result, float)

    def test_returns_original_string_type(self):
        result = compare_one(1, "2,3")
        assert result == "2,3"
        assert isinstance(result, str)

    def test_returns_none_when_equal(self):
        result = compare_one(1, 1)
        assert result is None

    def test_returns_none_for_equal_floats(self):
        result = compare_one(1.0, 1.0)
        assert result is None

    def test_returns_original_string_type_from_string_comparison(self):
        result = compare_one("5,1", "6")
        assert result == "6"
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# 6. Additional edge / miscellaneous cases
# ---------------------------------------------------------------------------

class TestMiscellaneous:
    """Extra coverage for less common but valid scenarios."""

    def test_same_value_same_type(self):
        assert compare_one(5, 5) is None

    def test_same_float_value(self):
        assert compare_one(3.14, 3.14) is None

    def test_string_number_greater_than_int(self):
        assert compare_one("10", "5") == "10"

    def test_int_greater_than_string_number(self):
        assert compare_one(10, "5") == 10

    def test_negative_string_vs_positive_int(self):
        assert compare_one("-5", 3) == 3

    def test_positive_string_vs_negative_int(self):
        assert compare_one("5", -3) == "5"

    def test_both_strings_negative(self):
        assert compare_one("-10", "-5") == "-5"

    def test_string_with_multiple_digits(self):
        assert compare_one("100", "99") == "100"

    def test_float_with_many_decimals(self):
        assert compare_one(1.123456789, 1.123456788) == 1.123456789

    def test_string_decimal_vs_integer_boundary(self):
        assert compare_one("0.999", 1) == 1

    def test_integer_vs_string_decimal_boundary(self):
        assert compare_one(1, "0.999") == 1
