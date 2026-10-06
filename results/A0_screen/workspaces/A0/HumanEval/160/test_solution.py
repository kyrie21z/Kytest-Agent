import pytest
from solution import do_algebra


class TestDoAlgebraBasicOperations:
    """Tests for basic algebraic operations."""

    def test_addition(self):
        result = do_algebra(["+", "+"], [1, 2, 3])
        assert result == 6  # 1 + 2 + 3 = 6

    def test_subtraction(self):
        result = do_algebra(["-", "-"], [10, 3, 2])
        assert result == 5  # 10 - 3 - 2 = 5

    def test_multiplication(self):
        result = do_algebra(["*", "*"], [2, 3, 4])
        assert result == 24  # 2 * 3 * 4 = 24

    def test_mixed_operations(self):
        result = do_algebra(["+", "*", "-"], [2, 3, 4, 5])
        assert result == 9  # 2 + 3 * 4 - 5 = 9

    def test_operator_precedence(self):
        """Verify that eval respects standard operator precedence."""
        result = do_algebra(["*", "+", "*"], [1, 2, 3, 4])
        assert result == 14  # 1 * 2 + 3 * 4 = 2 + 12 = 14


class TestFloorDivision:
    """Tests for floor division operation."""

    def test_floor_division_exact(self):
        result = do_algebra(["//"], [10, 2])
        assert result == 5  # 10 // 2 = 5

    def test_floor_division_rounds_down(self):
        result = do_algebra(["//"], [7, 2])
        assert result == 3  # 7 // 2 = 3

    def test_multiple_floor_divisions(self):
        result = do_algebra(["//", "//"], [100, 10, 3])
        assert result == 3  # (100 // 10) // 3 = 10 // 3 = 3

    def test_floor_division_with_other_ops(self):
        result = do_algebra(["+", "//"], [10, 3, 2])
        assert result == 11  # 10 + 3 // 2 = 10 + 1 = 11


class TestExponentiation:
    """Tests for exponentiation operation."""

    def test_exponentiation_basic(self):
        result = do_algebra(["**"], [2, 3])
        assert result == 8  # 2 ** 3 = 8

    def test_exponentiation_power_of_zero(self):
        result = do_algebra(["**"], [5, 0])
        assert result == 1  # 5 ** 0 = 1

    def test_exponentiation_zero_base(self):
        result = do_algebra(["**"], [0, 5])
        assert result == 0  # 0 ** 5 = 0

    def test_multiple_exponentiations(self):
        # Python's ** is right-associative: 2 ** 2 ** 3 = 2 ** (2 ** 3) = 2 ** 8 = 256
        result = do_algebra(["**", "**"], [2, 2, 3])
        assert result == 256

    def test_exponentiation_with_addition(self):
        result = do_algebra(["+", "**"], [1, 2, 3])
        assert result == 9  # 1 + 2 ** 3 = 1 + 8 = 9


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_minimum_operands(self):
        """Test with the minimum allowed input: 2 operands and 1 operator."""
        result = do_algebra(["+"], [0, 1])
        assert result == 1

    def test_single_operand_pair(self):
        result = do_algebra(["-"], [100, 50])
        assert result == 50

    def test_all_zeros(self):
        result = do_algebra(["+", "+", "+"], [0, 0, 0, 0])
        assert result == 0

    def test_large_numbers(self):
        result = do_algebra(["*", "*"], [100, 100, 100])
        assert result == 1000000  # 100 * 100 * 100 = 1_000_000

    def test_large_exponent(self):
        result = do_algebra(["**"], [2, 10])
        assert result == 1024  # 2 ** 10 = 1024

    def test_negative_result(self):
        result = do_algebra(["-"], [1, 10])
        assert result == -9  # 1 - 10 = -9


class TestZeroDivisionError:
    """Tests for division by zero scenarios."""

    def test_floor_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            do_algebra(["//"], [10, 0])

    def test_floor_division_by_zero_in_chain(self):
        with pytest.raises(ZeroDivisionError):
            do_algebra(["+", "//"], [10, 5, 0])


class TestComplexExpressions:
    """Tests for more complex multi-operator expressions."""

    def test_complex_expression_1(self):
        # 10 + 5 - 2 * 3 + 1 = 10 + 5 - 6 + 1 = 10
        result = do_algebra(["+", "-", "*", "+"], [10, 5, 2, 3, 1])
        assert result == 10

    def test_complex_expression_2(self):
        # 2 * 3 + 4 - 5 ** 2 = 6 + 4 - 25 = -15
        result = do_algebra(["*", "+", "-", "**"], [2, 3, 4, 5, 2])
        assert result == -15

    def test_all_same_operands(self):
        result = do_algebra(["+", "+", "+"], [5, 5, 5, 5])
        assert result == 20  # 5 + 5 + 5 + 5 = 20

    def test_alternating_operations(self):
        # 100 + 50 - 25 + 10 - 5 = 130
        result = do_algebra(["+", "-", "+", "-"], [100, 50, 25, 10, 5])
        assert result == 130


class TestOperandTypes:
    """Tests ensuring correct handling of operand types."""

    def test_single_digit_operands(self):
        result = do_algebra(["+"], [1, 2])
        assert result == 3

    def test_multi_digit_operands(self):
        result = do_algebra(["+"], [123, 456])
        assert result == 579

    def test_mixed_size_operands(self):
        result = do_algebra(["*", "+"], [1, 999, 1])
        assert result == 1000  # 1 * 999 + 1 = 1000


class TestReturnTypes:
    """Tests verifying return type correctness."""

    def test_integer_return_for_addition(self):
        result = do_algebra(["+", "+"], [1, 2, 3])
        assert isinstance(result, int)

    def test_integer_return_for_multiplication(self):
        result = do_algebra(["*", "*"], [2, 3, 4])
        assert isinstance(result, int)

    def test_integer_return_for_floor_division(self):
        result = do_algebra(["//"], [7, 2])
        assert isinstance(result, int)

    def test_integer_return_for_exponentiation(self):
        result = do_algebra(["**"], [2, 10])
        assert isinstance(result, int)
