import pytest
from solution import closest_integer


class TestClosestIntegerBasic:
    """Tests for basic integer inputs."""

    def test_positive_integer(self):
        assert closest_integer("10") == 10

    def test_negative_integer(self):
        assert closest_integer("-5") == -5

    def test_zero(self):
        assert closest_integer("0") == 0

    def test_large_positive_integer(self):
        assert closest_integer("999999") == 999999

    def test_large_negative_integer(self):
        assert closest_integer("-999999") == -999999


class TestClosestIntegerRoundingDown:
    """Tests for decimals that round toward zero."""

    def test_round_down_positive(self):
        assert closest_integer("15.3") == 15

    def test_round_down_small_fraction(self):
        assert closest_integer("3.1") == 3

    def test_round_down_very_small_fraction(self):
        assert closest_integer("7.01") == 7

    def test_round_down_negative(self):
        assert closest_integer("-15.3") == -15

    def test_round_down_negative_small_fraction(self):
        assert closest_integer("-3.1") == -3


class TestClosestIntegerRoundingUp:
    """Tests for decimals that round away from zero."""

    def test_round_up_positive(self):
        assert closest_integer("15.7") == 16

    def test_round_up_large_fraction(self):
        assert closest_integer("3.9") == 4

    def test_round_up_very_close_to_next(self):
        assert closest_integer("7.99") == 8

    def test_round_up_negative(self):
        assert closest_integer("-15.7") == -16

    def test_round_up_negative_large_fraction(self):
        assert closest_integer("-3.9") == -4


class TestClosestIntegerEquidistant:
    """Tests for .5 cases — rounding away from zero."""

    def test_positive_half(self):
        assert closest_integer("14.5") == 15

    def test_negative_half(self):
        assert closest_integer("-14.5") == -15

    def test_zero_point_five(self):
        assert closest_integer("0.5") == 1

    def test_negative_zero_point_five(self):
        assert closest_integer("-0.5") == -1

    def test_larger_positive_half(self):
        assert closest_integer("100.5") == 101

    def test_larger_negative_half(self):
        assert closest_integer("-100.5") == -101


class TestClosestIntegerEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_just_below_half(self):
        assert closest_integer("14.49") == 14

    def test_just_above_half(self):
        assert closest_integer("14.51") == 15

    def test_just_below_half_negative(self):
        assert closest_integer("-14.49") == -14

    def test_just_above_half_negative(self):
        assert closest_integer("-14.51") == -15

    def test_string_with_leading_zeros(self):
        assert closest_integer("007") == 7

    def test_string_with_trailing_zeros_decimal(self):
        assert closest_integer("10.0") == 10

    def test_very_small_positive(self):
        assert closest_integer("0.1") == 0

    def test_very_small_negative(self):
        assert closest_integer("-0.1") == 0

    def test_very_large_number(self):
        assert closest_integer("999999999.5") == 1000000000

    def test_very_large_negative_number(self):
        assert closest_integer("-999999999.5") == -1000000000


class TestClosestIntegerReturnTypes:
    """Tests verifying return type is int."""

    def test_return_type_positive(self):
        result = closest_integer("10")
        assert isinstance(result, int)

    def test_return_type_negative(self):
        result = closest_integer("-10")
        assert isinstance(result, int)

    def test_return_type_half(self):
        result = closest_integer("14.5")
        assert isinstance(result, int)


class TestClosestIntegerDocstringExamples:
    """Tests based on the docstring examples."""

    def test_docstring_example_1(self):
        assert closest_integer("10") == 10

    def test_docstring_example_2(self):
        assert closest_integer("15.3") == 15
