import pytest
from solution import double_the_difference


class TestDoubleTheDifference:
    """Tests for the double_the_difference function."""

    # --- Basic functionality: odd positive integers ---

    def test_single_odd_positive(self):
        assert double_the_difference([1]) == 1

    def test_multiple_odd_positives(self):
        assert double_the_difference([1, 3, 5]) == 1 + 9 + 25  # 35

    def test_example_from_docstring_1(self):
        assert double_the_difference([1, 3, 2, 0]) == 10  # 1^2 + 3^2

    def test_example_from_docstring_3(self):
        assert double_the_difference([9, -2]) == 81  # 9^2

    # --- Even numbers (should be ignored) ---

    def test_even_numbers_only(self):
        assert double_the_difference([2, 4, 6, 8]) == 0

    def test_mixed_even_and_odd(self):
        assert double_the_difference([2, 3, 4, 5]) == 9 + 25  # 34

    # --- Negative numbers (should be ignored) ---

    def test_negative_odds_only(self):
        assert double_the_difference([-1, -3, -5]) == 0

    def test_example_from_docstring_2(self):
        assert double_the_difference([-1, -2, 0]) == 0

    def test_negative_and_positive_mix(self):
        assert double_the_difference([-3, 3]) == 9  # only 3^2

    # --- Zero (even, should be ignored) ---

    def test_zero_only(self):
        assert double_the_difference([0]) == 0

    def test_zero_in_mixed_list(self):
        assert double_the_difference([0, 1, 2]) == 1  # only 1^2

    # --- Empty list ---

    def test_empty_list(self):
        assert double_the_difference([]) == 0

    # --- Floats / non-integers (should be ignored) ---

    def test_float_values(self):
        assert double_the_difference([1.5, 3.7, 5.1]) == 0

    def test_integer_like_floats(self):
        # 3.0 has "." in str("3.0"), so it's ignored
        assert double_the_difference([3.0, 5.0]) == 0

    def test_large_integer(self):
        assert double_the_difference([101]) == 101 ** 2  # 10201

    # --- Edge cases with large values ---

    def test_large_odd_number(self):
        assert double_the_difference([999]) == 999 ** 2  # 998001

    def test_many_elements(self):
        lst = list(range(1, 21))  # [1, 2, ..., 20]
        expected = sum(i ** 2 for i in range(1, 21) if i % 2 == 1)
        assert double_the_difference(lst) == expected

    # --- Boundary: smallest odd positive ---

    def test_smallest_odd_positive(self):
        assert double_the_difference([1]) == 1

    # --- Only non-matching elements ---

    def test_all_zeros(self):
        assert double_the_difference([0, 0, 0]) == 0

    def test_all_negatives(self):
        assert double_the_difference([-1, -3, -5, -7]) == 0

    def test_all_evens(self):
        assert double_the_difference([2, 4, 6, 8, 10]) == 0

    # --- Combination edge cases ---

    def test_single_element_odd(self):
        assert double_the_difference([7]) == 49

    def test_single_element_even(self):
        assert double_the_difference([8]) == 0

    def test_single_element_negative(self):
        assert double_the_difference([-5]) == 0

    def test_single_element_float(self):
        assert double_the_difference([3.14]) == 0

    def test_duplicate_odd_values(self):
        assert double_the_difference([3, 3, 3]) == 9 + 9 + 9  # 27

    def test_large_list_with_mixed_types(self):
        lst = [1, 2, 3, 4, 5, -1, -3, 0, 2.5, 7]
        expected = 1**2 + 3**2 + 5**2 + 7**2  # 1 + 9 + 25 + 49 = 84
        assert double_the_difference(lst) == expected
