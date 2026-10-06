import pytest
from solution import any_int


class TestAnyIntBasicCases:
    """Tests for basic scenarios where one number is the sum of the other two."""

    def test_positive_sum(self):
        assert any_int(5, 2, 7) is True

    def test_positive_sum_reordered(self):
        assert any_int(2, 7, 5) is True

    def test_positive_sum_first_is_sum(self):
        assert any_int(7, 2, 5) is True

    def test_positive_sum_second_is_sum(self):
        assert any_int(2, 7, 5) is True

    def test_positive_sum_third_is_sum(self):
        assert any_int(5, 2, 7) is True


class TestAnyIntNegativeNumbers:
    """Tests involving negative integers."""

    def test_negative_and_positive(self):
        assert any_int(3, -2, 1) is True

    def test_two_negatives(self):
        assert any_int(-5, -2, -7) is True

    def test_negative_sum(self):
        assert any_int(-1, 2, -3) is True

    def test_mixed_no_match(self):
        assert any_int(3, -2, 2) is False


class TestAnyIntNoMatch:
    """Tests where no number equals the sum of the other two."""

    def test_all_same(self):
        assert any_int(3, 3, 3) is False

    def test_no_relation(self):
        assert any_int(1, 2, 4) is False

    def test_close_values(self):
        assert any_int(10, 20, 35) is False

    def test_one_equals_other(self):
        assert any_int(3, 2, 2) is False


class TestAnyIntWithZero:
    """Tests involving zero."""

    def test_zero_as_sum(self):
        assert any_int(0, 5, -5) is True

    def test_all_zeros(self):
        assert any_int(0, 0, 0) is True

    def test_zero_with_nonzero(self):
        assert any_int(5, 0, 5) is True

    def test_zero_not_sum(self):
        assert any_int(0, 5, 3) is False


class TestAnyIntNonIntegerTypes:
    """Tests where inputs are not strictly int type."""

    def test_float_input(self):
        assert any_int(3.6, -2.2, 2) is False

    def test_float_as_first_arg(self):
        assert any_int(5.0, 2, 7) is False

    def test_float_as_second_arg(self):
        assert any_int(5, 2.0, 7) is False

    def test_float_as_third_arg(self):
        assert any_int(5, 2, 7.0) is False

    def test_string_input(self):
        assert any_int("5", 2, 7) is False

    def test_list_input(self):
        assert any_int([1, 2], 3, 5) is False

    def test_none_input(self):
        assert any_int(None, 2, 7) is False

    def test_mixed_types(self):
        assert any_int(5, "2", 7) is False


class TestAnyIntEdgeCases:
    """Edge cases and boundary conditions."""

    def test_large_numbers(self):
        assert any_int(1000000, 500000, 1500000) is True

    def test_large_negative_numbers(self):
        assert any_int(-1000000, -500000, -1500000) is True

    def test_one_and_negative_one(self):
        assert any_int(1, -1, 0) is True

    def test_single_digit(self):
        assert any_int(1, 1, 2) is True

    def test_negative_first(self):
        assert any_int(-7, 2, 5) is False

    def test_equal_positives(self):
        assert any_int(4, 2, 2) is True


class TestAnyIntBoolBehavior:
    """Tests related to bool being rejected by type(x) != int check."""

    def test_bool_true_rejected(self):
        # type(True) is bool, not int, so it's rejected
        assert any_int(True, 1, 0) is False

    def test_bool_false_rejected(self):
        assert any_int(False, 0, 0) is False

    def test_mixed_bool_and_int_rejected(self):
        assert any_int(True, 2, 3) is False
