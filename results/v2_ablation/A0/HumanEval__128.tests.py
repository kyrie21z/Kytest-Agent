import pytest
from solution import prod_signs


class TestProdSignsEmpty:
    """Tests for empty input."""

    def test_empty_list(self):
        assert prod_signs([]) is None

    def test_empty_list_with_spaces(self):
        assert prod_signs([ ]) is None


class TestProdSignsWithZero:
    """Tests when the array contains zero."""

    def test_zero_in_middle(self):
        assert prod_signs([1, 0, 3]) == 0

    def test_zero_at_start(self):
        assert prod_signs([0, 1, 2]) == 0

    def test_zero_at_end(self):
        assert prod_signs([1, 2, 0]) == 0

    def test_only_zero(self):
        assert prod_signs([0]) == 0

    def test_multiple_zeros(self):
        assert prod_signs([0, 0, 0]) == 0

    def test_zero_with_negative(self):
        assert prod_signs([-5, 0, 3]) == 0


class TestProdSignsAllPositive:
    """Tests when all elements are positive."""

    def test_single_positive(self):
        assert prod_signs([5]) == 5

    def test_all_positive_example(self):
        assert prod_signs([1, 2, 2, 4]) == 9

    def test_all_ones(self):
        assert prod_signs([1, 1, 1]) == 3

    def test_large_positive_numbers(self):
        assert prod_signs([10, 20, 30]) == 60

    def test_single_element(self):
        assert prod_signs([7]) == 7


class TestProdSignsAllNegative:
    """Tests when all elements are negative."""

    def test_single_negative(self):
        assert prod_signs([-5]) == -5

    def test_two_negatives(self):
        assert prod_signs([-2, -3]) == 5

    def test_three_negatives(self):
        assert prod_signs([-1, -2, -3]) == -6

    def test_four_negatives(self):
        assert prod_signs([-1, -2, -3, -4]) == 10

    def test_even_count_negative(self):
        assert prod_signs([-1, -1, -1, -1]) == 4

    def test_odd_count_negative(self):
        assert prod_signs([-1, -1, -1]) == -3


class TestProdSignsMixedSigns:
    """Tests with mixed positive and negative numbers."""

    def test_example_from_docstring(self):
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_one_negative_others_positive(self):
        assert prod_signs([1, 2, -3]) == -6

    def test_two_negative_others_positive(self):
        assert prod_signs([1, -2, -3]) == 6

    def test_alternating_signs(self):
        assert prod_signs([1, -1, 1, -1]) == 4

    def test_mixed_with_larger_values(self):
        assert prod_signs([3, -2, 5, -1]) == 11

    def test_single_positive_and_single_negative(self):
        assert prod_signs([5, -3]) == -8

    def test_many_elements_mixed(self):
        # Two negatives -> even count -> positive sign product
        # sum of magnitudes = 1+2+3+4+5 = 15
        assert prod_signs([1, -2, 3, -4, 5]) == 15

    def test_many_elements_mixed_negative_result(self):
        # Three negatives -> odd count -> negative sign product
        # sum of magnitudes = 1+2+3+4+5 = 15
        assert prod_signs([1, -2, -3, 4, -5]) == -15


class TestProdSignsEdgeCases:
    """Additional edge cases."""

    def test_single_zero(self):
        assert prod_signs([0]) == 0

    def test_large_array_all_same_sign(self):
        arr = [1] * 100
        assert prod_signs(arr) == 100

    def test_large_array_mixed_sign(self):
        arr = [1, -1] * 50
        assert prod_signs(arr) == 100

    def test_negative_one_values(self):
        assert prod_signs([-1, -1, -1]) == -3

    def test_positive_one_values(self):
        assert prod_signs([1, 1, 1]) == 3

    def test_mixed_ones_and_negatives(self):
        assert prod_signs([1, -1, 1]) == -3

    def test_extreme_value(self):
        assert prod_signs([1000000]) == 1000000

    def test_extreme_negative_value(self):
        assert prod_signs([-1000000]) == -1000000

    def test_extreme_mixed_values(self):
        assert prod_signs([1000000, -2000000]) == -3000000


class TestProdSignsTypeChecks:
    """Tests to verify return types."""

    def test_returns_none_for_empty(self):
        result = prod_signs([])
        assert result is None

    def test_returns_int_for_non_empty(self):
        assert isinstance(prod_signs([1, 2, 3]), int)

    def test_returns_int_for_negative_result(self):
        assert isinstance(prod_signs([-1, 2]), int)

    def test_returns_int_for_zero_result(self):
        assert isinstance(prod_signs([0, 1]), int)


class TestProdSignsDocstringExamples:
    """Verify the examples from the docstring work correctly."""

    def test_docstring_example_1(self):
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_docstring_example_2(self):
        assert prod_signs([0, 1]) == 0

    def test_docstring_example_3(self):
        assert prod_signs([]) is None
