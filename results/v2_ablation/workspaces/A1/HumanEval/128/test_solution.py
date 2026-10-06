"""Unit tests for prod_signs in solution.py."""

import pytest
from solution import prod_signs


class TestProdSignsEmpty:
    """Tests for empty input."""

    def test_empty_list_returns_none(self):
        assert prod_signs([]) is None


class TestProdSignsWithZero:
    """Tests when array contains zero."""

    def test_zero_and_positive(self):
        # [0, 1] -> contains 0, return 0
        assert prod_signs([0, 1]) == 0

    def test_zero_and_negative(self):
        # [0, -3] -> contains 0, return 0
        assert prod_signs([0, -3]) == 0

    def test_all_zeros(self):
        # [0, 0, 0] -> contains 0, return 0
        assert prod_signs([0, 0, 0]) == 0

    def test_single_zero(self):
        # [0] -> contains 0, return 0
        assert prod_signs([0]) == 0

    def test_zero_in_middle(self):
        # [1, 0, 2] -> contains 0, return 0
        assert prod_signs([1, 0, 2]) == 0


class TestProdSignsPositiveOnly:
    """Tests with only positive numbers."""

    def test_example_from_docstring(self):
        # [1, 2, 2, -4] -> abs sum = 9, sign product = -1, result = -9
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_single_positive(self):
        # [5] -> abs sum = 5, sign product = 1, result = 5
        assert prod_signs([5]) == 5

    def test_multiple_positives(self):
        # [1, 2, 3] -> abs sum = 6, sign product = 1, result = 6
        assert prod_signs([1, 2, 3]) == 6

    def test_larger_positives(self):
        # [10, 20, 30] -> abs sum = 60, sign product = 1, result = 60
        assert prod_signs([10, 20, 30]) == 60


class TestProdSignsNegativeOnly:
    """Tests with only negative numbers."""

    def test_single_negative(self):
        # [-5] -> abs sum = 5, sign product = -1, result = -5
        assert prod_signs([-5]) == -5

    def test_two_negatives(self):
        # [-1, -2] -> abs sum = 3, sign product = 1, result = 3
        assert prod_signs([-1, -2]) == 3

    def test_three_negatives(self):
        # [-1, -2, -3] -> abs sum = 6, sign product = -1, result = -6
        assert prod_signs([-1, -2, -3]) == -6

    def test_four_negatives(self):
        # [-1, -2, -3, -4] -> abs sum = 10, sign product = 1, result = 10
        assert prod_signs([-1, -2, -3, -4]) == 10

    def test_five_negatives(self):
        # [-1, -2, -3, -4, -5] -> abs sum = 15, sign product = -1, result = -15
        assert prod_signs([-1, -2, -3, -4, -5]) == -15


class TestProdSignsMixedSigns:
    """Tests with mixed positive and negative numbers."""

    def test_one_negative(self):
        # [1, 2, -3] -> abs sum = 6, sign product = -1, result = -6
        assert prod_signs([1, 2, -3]) == -6

    def test_even_negatives(self):
        # [1, -2, 3, -4] -> abs sum = 10, sign product = 1, result = 10
        assert prod_signs([1, -2, 3, -4]) == 10

    def test_odd_negatives(self):
        # [1, -2, 3, -4, -5] -> abs sum = 15, sign product = -1, result = -15
        assert prod_signs([1, -2, 3, -4, -5]) == -15

    def test_mixed_with_large_values(self):
        # [-10, 20, -30] -> abs sum = 60, sign product = 1, result = 60
        assert prod_signs([-10, 20, -30]) == 60

    def test_alternating_signs(self):
        # [1, -1, 1, -1] -> abs sum = 4, sign product = 1, result = 4
        assert prod_signs([1, -1, 1, -1]) == 4


class TestProdSignsEdgeCases:
    """Boundary and edge cases."""

    def test_single_element_positive(self):
        assert prod_signs([1]) == 1

    def test_single_element_negative(self):
        assert prod_signs([-1]) == -1

    def test_largest_abs_value(self):
        # [100] -> abs sum = 100, sign product = 1, result = 100
        assert prod_signs([100]) == 100

    def test_negative_largest_abs_value(self):
        # [-100] -> abs sum = 100, sign product = -1, result = -100
        assert prod_signs([-100]) == -100

    def test_many_elements_same_sign(self):
        # [1]*10 -> abs sum = 10, sign product = 1, result = 10
        assert prod_signs([1] * 10) == 10

    def test_many_elements_opposite_sign(self):
        # [-1]*10 -> abs sum = 10, sign product = 1 (even count), result = 10
        assert prod_signs([-1] * 10) == 10

    def test_many_elements_opposite_sign_odd_count(self):
        # [-1]*9 -> abs sum = 9, sign product = -1 (odd count), result = -9
        assert prod_signs([-1] * 9) == -9

    def test_duplicate_values(self):
        # [2, 2, 2] -> abs sum = 6, sign product = 1, result = 6
        assert prod_signs([2, 2, 2]) == 6

    def test_duplicate_negative_values(self):
        # [-2, -2, -2] -> abs sum = 6, sign product = -1, result = -6
        assert prod_signs([-2, -2, -2]) == -6

    def test_magnitude_sum_only(self):
        # [3, -3] -> abs sum = 6, sign product = -1, result = -6
        assert prod_signs([3, -3]) == -6


class TestProdSignsDocstringExamples:
    """Verify all examples from the docstring pass."""

    def test_docstring_example_1(self):
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_docstring_example_2(self):
        assert prod_signs([0, 1]) == 0

    def test_docstring_example_3(self):
        assert prod_signs([]) is None
