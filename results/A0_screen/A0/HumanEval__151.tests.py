import pytest
from solution import double_the_difference


class TestDoubleTheDifference:
    """Tests for the double_the_difference function."""

    # --- Basic functionality ---

    def test_basic_example_from_docstring(self):
        assert double_the_difference([1, 3, 2, 0]) == 10

    def test_negative_numbers_only(self):
        assert double_the_difference([-1, -2, 0]) == 0

    def test_single_positive_odd(self):
        assert double_the_difference([9, -2]) == 81

    def test_zero_only(self):
        assert double_the_difference([0]) == 0

    # --- Empty list ---

    def test_empty_list(self):
        assert double_the_difference([]) == 0

    # --- Positive odd integers ---

    def test_single_positive_odd_integer(self):
        assert double_the_difference([3]) == 9

    def test_multiple_positive_odd_integers(self):
        assert double_the_difference([1, 3, 5]) == 1 + 9 + 25  # 35

    def test_all_positive_odds(self):
        assert double_the_difference([1, 1, 1]) == 3

    def test_large_positive_odd(self):
        assert double_the_difference([999]) == 998001

    # --- Even numbers (should be ignored) ---

    def test_even_numbers_only(self):
        assert double_the_difference([2, 4, 6, 8]) == 0

    def test_mixed_even_and_odd(self):
        assert double_the_difference([2, 3, 4, 5]) == 9 + 25  # 34

    def test_zero_is_ignored(self):
        assert double_the_difference([0, 2, 4]) == 0

    # --- Negative numbers (should be ignored) ---

    def test_negative_odd_ignored(self):
        assert double_the_difference([-1, -3, -5]) == 0

    def test_negative_even_ignored(self):
        assert double_the_difference([-2, -4, -6]) == 0

    def test_mixed_negative_and_positive(self):
        assert double_the_difference([-1, 3, -5, 7]) == 9 + 49  # 58

    # --- Floats (should be ignored) ---

    def test_float_values_ignored(self):
        assert double_the_difference([1.5, 3.5, 5.5]) == 0

    def test_float_that_looks_like_odd(self):
        assert double_the_difference([3.0]) == 0

    def test_negative_float_ignored(self):
        assert double_the_difference([-1.5, -3.5]) == 0

    def test_mixed_int_and_float(self):
        assert double_the_difference([1, 2.5, 3, 4.0]) == 1 + 9  # 10

    # --- Non-integer types (should raise TypeError) ---

    def test_string_in_list_raises_error(self):
        """Strings cause TypeError because % operator fails on them."""
        with pytest.raises(TypeError):
            double_the_difference([1, "hello", 3])

    def test_none_in_list_raises_error(self):
        """None causes TypeError because % operator fails on it."""
        with pytest.raises(TypeError):
            double_the_difference([1, None, 3])

    # --- Edge cases ---

    def test_single_element_odd(self):
        assert double_the_difference([7]) == 49

    def test_single_element_even(self):
        assert double_the_difference([8]) == 0

    def test_single_element_negative(self):
        assert double_the_difference([-7]) == 0

    def test_duplicate_odd_numbers(self):
        assert double_the_difference([3, 3, 3]) == 27

    def test_large_list_of_odds(self):
        lst = [i for i in range(1, 20, 2)]  # [1, 3, 5, ..., 19]
        expected = sum(i ** 2 for i in lst)
        assert double_the_difference(lst) == expected

    def test_alternating_even_odd(self):
        assert double_the_difference([1, 2, 3, 4, 5, 6]) == 1 + 9 + 25  # 35

    def test_only_zeros(self):
        assert double_the_difference([0, 0, 0]) == 0

    def test_mixed_with_zero(self):
        assert double_the_difference([0, 1, 0, 3, 0]) == 1 + 9  # 10

    # --- Boundary values ---

    def test_smallest_positive_odd(self):
        assert double_the_difference([1]) == 1

    def test_largest_common_odd(self):
        assert double_the_difference([99999]) == 9999800001

    # --- Return type check ---

    def test_return_type(self):
        assert isinstance(double_the_difference([1, 3]), int)

    def test_return_type_empty(self):
        assert isinstance(double_the_difference([]), int)
