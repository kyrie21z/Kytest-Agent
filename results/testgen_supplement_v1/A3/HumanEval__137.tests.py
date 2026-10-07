"""Unit tests for compare_one function in solution.py."""

import pytest
from solution import compare_one


# =============================================================================
# Normal Cases – typical inputs covering all documented type combinations
# =============================================================================

class TestNormalCases:
    """Tests with typical, well-formed inputs."""

    def test_int_vs_int(self):
        assert compare_one(1, 2) == 2

    def test_int_vs_int_reversed(self):
        assert compare_one(2, 1) == 2

    def test_int_vs_float(self):
        assert compare_one(1, 2.5) == 2.5

    def test_float_vs_int(self):
        assert compare_one(2.5, 1) == 2.5

    def test_float_vs_float(self):
        assert compare_one(3.1, 2.9) == 3.1

    def test_string_vs_string(self):
        assert compare_one("5", "6") == "6"

    def test_string_vs_int(self):
        assert compare_one("10", 5) == "10"

    def test_int_vs_string(self):
        assert compare_one(5, "10") == "10"

    def test_string_with_comma_vs_int(self):
        assert compare_one(1, "2,3") == "2,3"

    def test_string_with_comma_vs_string(self):
        assert compare_one("5,1", "6") == "6"

    def test_string_with_dot_vs_string(self):
        assert compare_one("5.1", "6") == "6"

    def test_negative_numbers(self):
        assert compare_one(-1, -2) == -1

    def test_negative_vs_positive(self):
        assert compare_one(-1, 1) == 1

    def test_positive_vs_negative(self):
        assert compare_one(1, -1) == 1

    def test_zero_vs_positive(self):
        assert compare_one(0, 1) == 1

    def test_zero_vs_negative(self):
        assert compare_one(0, -1) == 0

    def test_both_zero(self):
        assert compare_one(0, 0) is None

    def test_large_numbers(self):
        assert compare_one(1_000_000, 999_999) == 1_000_000

    def test_small_floats(self):
        assert compare_one(0.001, 0.0001) == 0.001


# =============================================================================
# Boundary Cases – edges of valid input ranges
# =============================================================================

class TestBoundaryCases:
    """Tests at the boundaries of valid input ranges."""

    def test_equal_integers(self):
        assert compare_one(5, 5) is None

    def test_equal_floats(self):
        assert compare_one(3.14, 3.14) is None

    def test_equal_int_and_string_numeric(self):
        assert compare_one(1, "1") is None

    def test_equal_float_and_string_numeric(self):
        assert compare_one(2.5, "2.5") is None

    def test_equal_with_comma_decimal(self):
        assert compare_one(2.5, "2,5") is None

    def test_equal_negative(self):
        assert compare_one(-3, -3) is None

    def test_equal_via_different_string_formats(self):
        # "2,5" (comma) should equal 2.5 (float)
        assert compare_one(2.5, "2,5") is None

    def test_very_small_difference(self):
        assert compare_one(1.0, 1.0000001) == 1.0000001

    def test_very_small_difference_reversed(self):
        assert compare_one(1.0000001, 1.0) == 1.0000001

    def test_same_value_different_types_return_none(self):
        assert compare_one(0, "0") is None

    def test_string_zero_vs_int_zero(self):
        assert compare_one("0", 0) is None


# =============================================================================
# Edge Cases – empty, null-like, zero-size inputs
# =============================================================================

class TestEdgeCases:
    """Tests with empty strings, whitespace, and zero-size inputs."""

    def test_empty_string_vs_number(self):
        # float("") raises ValueError
        with pytest.raises(ValueError):
            compare_one("", 1)

    def test_number_vs_empty_string(self):
        with pytest.raises(ValueError):
            compare_one(1, "")

    def test_two_empty_strings(self):
        # float("") raises ValueError
        with pytest.raises(ValueError):
            compare_one("", "")

    def test_whitespace_string(self):
        # float(" ") raises ValueError
        with pytest.raises(ValueError):
            compare_one(" ", 1)

    def test_zero_length_string_vs_number(self):
        with pytest.raises(ValueError):
            compare_one("", 5)


# =============================================================================
# Invalid Inputs – non-numeric strings that cannot be parsed
# =============================================================================

class TestInvalidInputs:
    """Tests with inputs that cannot be converted to a number."""

    def test_non_numeric_string(self):
        with pytest.raises(ValueError):
            compare_one("abc", 1)

    def test_non_numeric_string_other_way(self):
        with pytest.raises(ValueError):
            compare_one(1, "xyz")

    def test_two_non_numeric_strings(self):
        with pytest.raises(ValueError):
            compare_one("hello", "world")

    def test_mixed_valid_invalid(self):
        with pytest.raises(ValueError):
            compare_one("123", "not_a_number")

    def test_special_characters_in_string(self):
        with pytest.raises(ValueError):
            compare_one("@#$%", 1)

    def test_string_with_multiple_commas(self):
        # "1,2,3" -> replace commas -> "1.2.3" -> float() fails
        with pytest.raises(ValueError):
            compare_one("1,2,3", 1)


# =============================================================================
# Exception Cases – verify specific error types and behaviors
# =============================================================================

class TestExceptionCases:
    """Tests that verify exception handling behavior."""

    def test_value_error_for_unparseable_input(self):
        """Ensure ValueError is raised for unparseable string inputs."""
        with pytest.raises(ValueError, match="could not convert string to float"):
            compare_one("foo", "bar")

    def test_value_error_raised_from_first_argument(self):
        """Error should propagate when first arg is invalid."""
        with pytest.raises(ValueError):
            compare_one("invalid", 42)

    def test_value_error_raised_from_second_argument(self):
        """Error should propagate when second arg is invalid."""
        with pytest.raises(ValueError):
            compare_one(42, "invalid")

    def test_none_input_raises_error(self):
        """None gets converted to 'None' string, which is not numeric."""
        with pytest.raises(ValueError):
            compare_one(None, 1)

    def test_none_vs_none_raises_error(self):
        with pytest.raises(ValueError):
            compare_one(None, None)


# =============================================================================
# Return Type Preservation Tests
# =============================================================================

class TestReturnTypePreservation:
    """Verify that the returned value preserves the original type."""

    def test_returns_original_float_type(self):
        result = compare_one(1, 2.5)
        assert isinstance(result, float)
        assert result == 2.5

    def test_returns_original_int_type(self):
        result = compare_one(1, 2)
        assert isinstance(result, int)
        assert result == 2

    def test_returns_original_string_type(self):
        result = compare_one("5", "6")
        assert isinstance(result, str)
        assert result == "6"

    def test_returns_string_with_comma(self):
        result = compare_one(1, "2,3")
        assert isinstance(result, str)
        assert result == "2,3"

    def test_returns_none_on_equality(self):
        result = compare_one(1, "1")
        assert result is None
