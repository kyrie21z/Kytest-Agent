import pytest
from solution import compare_one


class TestCompareOneBasic:
    """Tests for basic integer and float comparisons."""

    def test_int_vs_float_smaller(self):
        assert compare_one(1, 2.5) == 2.5

    def test_int_vs_float_equal_value(self):
        assert compare_one(1, 1.0) is None

    def test_int_vs_float_larger(self):
        assert compare_one(5, 3) == 5

    def test_float_vs_int_smaller(self):
        assert compare_one(3.7, 4) == 4

    def test_float_vs_int_larger(self):
        assert compare_one(6.1, 5) == 6.1

    def test_two_ints_equal(self):
        assert compare_one(7, 7) is None

    def test_two_ints_different(self):
        assert compare_one(10, 3) == 10
        assert compare_one(3, 10) == 10

    def test_two_floats_equal(self):
        assert compare_one(2.5, 2.5) is None

    def test_two_floats_different(self):
        assert compare_one(2.5, 3.1) == 3.1
        assert compare_one(3.1, 2.5) == 3.1


class TestCompareOneStrings:
    """Tests for string inputs with '.' and ',' decimal separators."""

    def test_string_with_comma_vs_int(self):
        assert compare_one(1, "2,3") == "2,3"

    def test_string_with_comma_vs_int_reversed(self):
        assert compare_one("5", 2) == "5"

    def test_string_with_dot_vs_int(self):
        assert compare_one(1, "2.3") == "2.3"

    def test_string_vs_string_comma(self):
        assert compare_one("5,1", "6") == "6"

    def test_string_vs_string_dot(self):
        assert compare_one("5.1", "6") == "6"

    def test_string_vs_string_equal(self):
        assert compare_one("3,14", "3.14") is None

    def test_string_vs_string_first_larger(self):
        result = compare_one("10", "5")
        assert result == "10"

    def test_string_vs_string_second_larger(self):
        result = compare_one("3", "8")
        assert result == "8"

    def test_string_with_comma_vs_float(self):
        assert compare_one("1,5", 2.0) == 2.0

    def test_string_with_dot_vs_float(self):
        assert compare_one("1.5", 2.0) == 2.0


class TestCompareOneEqualValues:
    """Tests where values are numerically equal but may differ in type."""

    def test_int_and_string_equal(self):
        assert compare_one("1", 1) is None

    def test_int_and_string_equal_reversed(self):
        assert compare_one(1, "1") is None

    def test_float_and_string_equal(self):
        assert compare_one(2.5, "2,5") is None

    def test_float_and_string_equal_dot(self):
        assert compare_one(2.5, "2.5") is None

    def test_string_and_string_equal(self):
        assert compare_one("3", "3") is None

    def test_negative_zero(self):
        assert compare_one(-0, 0) is None

    def test_string_negative_zero(self):
        assert compare_one("-0", 0) is None


class TestCompareOneNegativeNumbers:
    """Tests involving negative numbers."""

    def test_negative_int_vs_positive_int(self):
        assert compare_one(-1, 5) == 5

    def test_negative_int_vs_negative_int(self):
        assert compare_one(-3, -1) == -1

    def test_negative_float_vs_positive_float(self):
        assert compare_one(-2.5, 1.5) == 1.5

    def test_negative_string_vs_positive(self):
        assert compare_one("-5", 3) == 3

    def test_negative_string_vs_negative_string(self):
        assert compare_one("-1,5", "-2,5") == "-1,5"

    def test_negative_vs_equal(self):
        assert compare_one(-3, "-3") is None


class TestCompareOneEdgeCases:
    """Edge case tests."""

    def test_zero_vs_positive(self):
        assert compare_one(0, 1) == 1

    def test_zero_vs_negative(self):
        assert compare_one(0, -1) == 0

    def test_large_numbers(self):
        assert compare_one(1000000, 999999) == 1000000

    def test_small_decimal_difference(self):
        assert compare_one(1.0001, 1.0) == 1.0001

    def test_string_large_number(self):
        assert compare_one("1000", 500) == "1000"

    def test_both_strings_same_value_different_format(self):
        assert compare_one("1,000", "1.000") is None

    def test_mixed_types_all_equal(self):
        assert compare_one(0, "0,0") is None
        assert compare_one(0.0, "0") is None
