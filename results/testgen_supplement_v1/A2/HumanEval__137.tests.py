import pytest
from solution import compare_one


# ──────────────────────────────────────────────
# Normal / typical-input cases
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with straightforward, typical inputs."""

    def test_int_vs_int(self):
        assert compare_one(1, 2) == 2

    def test_int_vs_int_reversed(self):
        assert compare_one(2, 1) == 2

    def test_float_vs_float(self):
        assert compare_one(1.5, 2.5) == 2.5

    def test_float_vs_float_reversed(self):
        assert compare_one(2.5, 1.5) == 2.5

    def test_int_vs_float(self):
        assert compare_one(1, 2.5) == 2.5

    def test_int_vs_float_reversed(self):
        assert compare_one(2.5, 1) == 2.5

    def test_int_vs_string_comma(self):
        # Docstring example: compare_one(1, "2,3") ➞ "2,3"
        assert compare_one(1, "2,3") == "2,3"

    def test_int_vs_string_dot(self):
        assert compare_one(1, "2.3") == "2.3"

    def test_float_vs_string_comma(self):
        assert compare_one(1.5, "2,3") == "2,3"

    def test_float_vs_string_dot(self):
        assert compare_one(1.5, "2.3") == "2.3"

    def test_string_vs_string_comma(self):
        # Docstring example: compare_one("5,1", "6") ➞ "6"
        assert compare_one("5,1", "6") == "6"

    def test_string_vs_string_dot(self):
        assert compare_one("5.1", "6") == "6"

    def test_string_vs_string_both_comma(self):
        assert compare_one("1,5", "2,3") == "2,3"

    def test_string_wins_over_int(self):
        assert compare_one("10", 5) == "10"

    def test_int_wins_over_string(self):
        assert compare_one(10, "5") == 10

    def test_string_wins_over_float(self):
        assert compare_one("10", 5.5) == "10"

    def test_float_wins_over_string(self):
        assert compare_one(10.0, "5") == 10.0


# ──────────────────────────────────────────────
# Equal-value cases (should return None)
# ──────────────────────────────────────────────

class TestEqualValues:
    """When both values represent the same number, return None."""

    def test_int_equal_int(self):
        assert compare_one(1, 1) is None

    def test_int_equal_string_int(self):
        assert compare_one(1, "1") is None

    def test_int_equal_string_with_dot(self):
        assert compare_one(1, "1.0") is None

    def test_int_equal_string_with_comma(self):
        assert compare_one(1, "1,0") is None

    def test_float_equal_int(self):
        assert compare_one(1.0, 1) is None

    def test_float_equal_string(self):
        assert compare_one(1.0, "1") is None

    def test_string_equal_string(self):
        assert compare_one("1", "1") is None

    def test_string_comma_equal_string_dot(self):
        assert compare_one("1,0", "1.0") is None

    def test_negative_zero(self):
        assert compare_one(-0, 0) is None

    def test_large_equal_values(self):
        assert compare_one(999999, "999999") is None


# ──────────────────────────────────────────────
# Boundary cases at edges of valid ranges
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Edge-of-range numeric inputs."""

    def test_zero_vs_positive(self):
        assert compare_one(0, 1) == 1

    def test_zero_vs_negative(self):
        assert compare_one(0, -1) == 0

    def test_negative_vs_negative(self):
        assert compare_one(-1, -2) == -1

    def test_negative_vs_negative_reversed(self):
        assert compare_one(-2, -1) == -1

    def test_negative_vs_positive(self):
        assert compare_one(-1, 1) == 1

    def test_very_small_float(self):
        assert compare_one(0.0001, 0.0002) == 0.0002

    def test_very_large_numbers(self):
        assert compare_one(1e100, 1e99) == 1e100

    def test_very_large_string(self):
        assert compare_one("1e100", 1e99) == "1e100"

    def test_exact_half(self):
        assert compare_one(0.5, 0.75) == 0.75

    def test_just_below_one(self):
        assert compare_one(0.999, 1) == 1

    def test_just_above_one(self):
        assert compare_one(1, 1.001) == 1.001

    def test_single_digit_strings(self):
        assert compare_one("3", "7") == "7"

    def test_multi_digit_vs_single_digit(self):
        assert compare_one("100", "9") == "100"

    def test_decimal_boundary(self):
        assert compare_one("0,99", "1") == "1"


# ──────────────────────────────────────────────
# Empty, null, zero-size, and special-string cases
# ──────────────────────────────────────────────

class TestSpecialInputs:
    """Edge-case inputs like empty strings, whitespace, etc."""

    def test_empty_string_raises(self):
        """An empty string cannot be converted to a float."""
        with pytest.raises(ValueError):
            compare_one("", "1")

    def test_whitespace_string_raises(self):
        """Whitespace-only strings cannot be converted to a float."""
        with pytest.raises(ValueError):
            compare_one(" ", "1")

    def test_string_with_only_comma_raises(self):
        """A lone comma is not a valid number."""
        with pytest.raises(ValueError):
            compare_one(",", "1")

    def test_string_with_only_dot_raises(self):
        """A lone dot is not a valid number."""
        with pytest.raises(ValueError):
            compare_one(".", "1")

    def test_string_with_multiple_decimals(self):
        """Multiple dots/commas produce an invalid float."""
        with pytest.raises(ValueError):
            compare_one("1.2.3", "1")

    def test_string_with_letters_raises(self):
        """Non-numeric characters cause ValueError."""
        with pytest.raises(ValueError):
            compare_one("abc", "1")

    def test_none_input_raises(self):
        """None cannot be converted to float."""
        with pytest.raises(ValueError):
            compare_one(None, "1")

    def test_list_input_raises(self):
        """Lists are not valid inputs."""
        with pytest.raises(ValueError):
            compare_one([1], "1")

    def test_dict_input_raises(self):
        """Dicts are not valid inputs."""
        with pytest.raises(ValueError):
            compare_one({}, "1")


# ──────────────────────────────────────────────
# Return-type preservation
# ──────────────────────────────────────────────

class TestReturnTypePreservation:
    """The returned value must be the *original* argument (not coerced)."""

    def test_returns_original_int(self):
        result = compare_one(1, 2)
        assert result == 2
        assert isinstance(result, int)

    def test_returns_original_float(self):
        result = compare_one(1.5, 2.5)
        assert result == 2.5
        assert isinstance(result, float)

    def test_returns_original_string(self):
        result = compare_one(1, "2,3")
        assert result == "2,3"
        assert isinstance(result, str)

    def test_returns_original_string_comma(self):
        result = compare_one("5,1", "6")
        assert result == "6"
        assert isinstance(result, str)

    def test_returns_first_when_first_larger(self):
        result = compare_one(5, 3)
        assert result == 5
        assert isinstance(result, int)

    def test_returns_second_when_second_larger(self):
        result = compare_one(3, 5)
        assert result == 5
        assert isinstance(result, int)

    def test_returns_none_on_equality(self):
        result = compare_one(1, "1")
        assert result is None


# ──────────────────────────────────────────────
# Docstring examples (regression guard)
# ──────────────────────────────────────────────

class TestDocstringExamples:
    """Exact examples from the docstring must pass."""

    def test_example_1(self):
        # compare_one(1, 2.5) ➞ 2.5
        assert compare_one(1, 2.5) == 2.5

    def test_example_2(self):
        # compare_one(1, "2,3") ➞ "2,3"
        assert compare_one(1, "2,3") == "2,3"

    def test_example_3(self):
        # compare_one("5,1", "6") ➞ "6"
        assert compare_one("5,1", "6") == "6"

    def test_example_4(self):
        # compare_one("1", 1) ➞ None
        assert compare_one("1", 1) is None
