import pytest
from solution import multiply_int


class TestMultiplyIntPositiveCases:
    """Tests for multiplying two positive integers."""

    def test_basic_multiplication(self):
        assert multiply_int(2, 3) == 6

    def test_larger_positive_numbers(self):
        assert multiply_int(5, 7) == 35

    def test_multiply_by_one(self):
        assert multiply_int(10, 1) == 10

    def test_one_times_n(self):
        assert multiply_int(1, 8) == 8

    def test_self_multiplication(self):
        assert multiply_int(6, 6) == 36

    def test_large_result(self):
        assert multiply_int(100, 50) == 5000


class TestMultiplyIntWithZero:
    """Tests involving zero as one of the operands."""

    def test_zero_times_anything(self):
        assert multiply_int(0, 10) == 0

    def test_anything_times_zero(self):
        assert multiply_int(10, 0) == 0

    def test_zero_times_zero(self):
        assert multiply_int(0, 0) == 0


class TestMultiplyIntNegativeNumbers:
    """Tests for multiplying with negative integers."""

    def test_negative_second_operand(self):
        assert multiply_int(5, -3) == -15

    def test_negative_first_operand(self):
        assert multiply_int(-5, 3) == -15

    def test_both_negative_operands(self):
        assert multiply_int(-5, -3) == 15

    def test_negative_with_zero(self):
        assert multiply_int(-7, 0) == 0

    def test_zero_with_negative(self):
        assert multiply_int(0, -5) == 0

    def test_negative_one_times_positive(self):
        assert multiply_int(-1, 10) == -10

    def test_positive_times_negative_one(self):
        assert multiply_int(10, -1) == -10

    def test_negative_one_times_negative_one(self):
        assert multiply_int(-1, -1) == 1


class TestMultiplyIntEdgeCases:
    """Edge case tests."""

    def test_single_digit_multiplication(self):
        assert multiply_int(3, 4) == 12

    def test_negative_small_numbers(self):
        assert multiply_int(-2, -3) == 6

    def test_mixed_signs(self):
        assert multiply_int(-4, 7) == -28

    def test_large_negative_second_operand(self):
        assert multiply_int(100, -10) == -1000

    def test_large_negative_first_operand(self):
        assert multiply_int(-100, 10) == -1000

    def test_both_large_negative(self):
        assert multiply_int(-100, -10) == 1000


class TestMultiplyIntTypeValidation:
    """Tests to ensure the function handles expected input types."""

    def test_integer_inputs(self):
        """Ensure integer inputs work correctly."""
        assert isinstance(multiply_int(3, 4), int)

    def test_result_is_integer(self):
        """Ensure result is always an integer."""
        assert isinstance(multiply_int(-5, 7), int)
