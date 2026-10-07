import pytest
from solution import compare_one


class TestCompareOneBasic:
    """Tests for basic integer comparisons."""

    def test_int_vs_int_first_larger(self):
        assert compare_one(5, 3) == 5

    def test_int_vs_int_second_larger(self):
        assert compare_one(3, 5) == 5

    def test_int_vs_int_equal(self):
        assert compare_one(4, 4) is None

    def test_int_vs_int_negative(self):
        assert compare_one(-1, -5) == -1

    def test_int_vs_int_both_negative(self):
        assert compare_one(-5, -1) == -1


class TestCompareOneFloats:
    """Tests for float comparisons."""

    def test_float_vs_float_first_larger(self):
        assert compare_one(2.5, 1.0) == 2.5

    def test_float_vs_float_second_larger(self):
        assert compare_one(1.0, 2.5) == 2.5

    def test_float_vs_float_equal(self):
        assert compare_one(3.14, 3.14) is None

    def test_float_vs_float_negative(self):
        assert compare_one(-0.5, -1.5) == -0.5


class TestCompareOneStrings:
    """Tests for string number comparisons."""

    def test_string_with_dot_first_larger(self):
        assert compare_one("6", "5.1") == "6"

    def test_string_with_dot_second_larger(self):
        assert compare_one("1.0", "2.5") == "2.5"

    def test_string_with_comma_first_larger(self):
        assert compare_one("6", "5,1") == "6"

    def test_string_with_comma_second_larger(self):
        assert compare_one("1,0", "2,3") == "2,3"

    def test_string_with_comma_equal(self):
        assert compare_one("3,14", "3.14") is None

    def test_string_vs_string_equal_values_different_sep(self):
        assert compare_one("1,5", "1.5") is None


class TestCompareOneMixedTypes:
    """Tests for mixed type comparisons."""

    def test_int_vs_float_first_larger(self):
        assert compare_one(5, 3.2) == 5

    def test_int_vs_float_second_larger(self):
        assert compare_one(3, 5.2) == 5.2

    def test_int_vs_float_equal(self):
        assert compare_one(2, 2.0) is None

    def test_int_vs_string_comma(self):
        assert compare_one(1, "2,3") == "2,3"

    def test_int_vs_string_dot(self):
        assert compare_one(1, "2.3") == "2.3"

    def test_int_vs_string_equal(self):
        assert compare_one(1, "1") is None

    def test_int_vs_string_equal_comma(self):
        assert compare_one(1, "1,0") is None

    def test_float_vs_string_comma(self):
        assert compare_one(5.1, "6") == "6"

    def test_float_vs_string_dot(self):
        assert compare_one(5.1, "6") == "6"

    def test_float_vs_string_equal(self):
        assert compare_one(3.14, "3.14") is None

    def test_float_vs_string_equal_comma(self):
        assert compare_one(3.14, "3,14") is None

    def test_string_vs_string_mixed_separator(self):
        assert compare_one("5,1", "6") == "6"

    def test_string_vs_string_first_larger(self):
        assert compare_one("7", "6.9") == "7"

    def test_string_vs_string_second_larger(self):
        assert compare_one("5", "6") == "6"


class TestCompareOneEdgeCases:
    """Tests for edge cases."""

    def test_zero_vs_positive(self):
        assert compare_one(0, 1) == 1

    def test_zero_vs_negative(self):
        assert compare_one(0, -1) == 0

    def test_negative_vs_positive(self):
        assert compare_one(-1, 1) == 1

    def test_large_numbers(self):
        assert compare_one(1000000, 999999) == 1000000

    def test_very_small_float(self):
        assert compare_one(0.0001, 0.00001) == 0.0001

    def test_string_zero_vs_int_zero(self):
        assert compare_one(0, "0") is None

    def test_string_zero_vs_float_zero(self):
        assert compare_one(0.0, "0,0") is None

    def test_equal_strings(self):
        assert compare_one("5", "5") is None

    def test_equal_floats_via_string(self):
        assert compare_one("3,14159", 3.14159) is None


class TestCompareOneReturnTypes:
    """Tests verifying return types match input types."""

    def test_returns_int_when_int_wins(self):
        result = compare_one(10, 5)
        assert isinstance(result, int)
        assert result == 10

    def test_returns_float_when_float_wins(self):
        result = compare_one(5, 10.5)
        assert isinstance(result, float)
        assert result == 10.5

    def test_returns_string_when_string_wins(self):
        result = compare_one(5, "10")
        assert isinstance(result, str)
        assert result == "10"

    def test_returns_none_when_equal(self):
        result = compare_one(5, 5)
        assert result is None

    def test_returns_none_for_equal_strings(self):
        result = compare_one("3", "3")
        assert result is None
