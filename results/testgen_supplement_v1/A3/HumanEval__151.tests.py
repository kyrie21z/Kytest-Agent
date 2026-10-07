"""Unit tests for solution.double_the_difference."""

import pytest
from solution import double_the_difference


class TestNormalCases:
    """Tests with typical valid inputs."""

    def test_basic_example_from_docstring(self):
        # [1, 3, 2, 0] -> 1^2 + 3^2 = 1 + 9 = 10
        assert double_the_difference([1, 3, 2, 0]) == 10

    def test_negative_even_ignored(self):
        # [-1, -2, 0] -> all ignored -> 0
        assert double_the_difference([-1, -2, 0]) == 0

    def test_positive_odd_only(self):
        # [9, -2] -> 9^2 = 81
        assert double_the_difference([9, -2]) == 81

    def test_single_zero(self):
        # [0] -> 0
        assert double_the_difference([0]) == 0

    def test_multiple_odds(self):
        # [1, 3, 5] -> 1 + 9 + 25 = 35
        assert double_the_difference([1, 3, 5]) == 35

    def test_mixed_even_and_odd(self):
        # [1, 2, 3, 4, 5] -> 1 + 9 + 25 = 35
        assert double_the_difference([1, 2, 3, 4, 5]) == 35

    def test_all_positives(self):
        # [1, 2, 3, 4, 5, 6, 7] -> 1 + 9 + 25 + 49 = 84
        assert double_the_difference([1, 2, 3, 4, 5, 6, 7]) == 84

    def test_single_odd(self):
        # [5] -> 25
        assert double_the_difference([5]) == 25

    def test_single_even(self):
        # [4] -> 0
        assert double_the_difference([4]) == 0

    def test_large_odd_number(self):
        # [101] -> 101^2 = 10201
        assert double_the_difference([101]) == 10201

    def test_repeated_values(self):
        # [1, 1, 1] -> 1 + 1 + 1 = 3
        assert double_the_difference([1, 1, 1]) == 3

    def test_negative_odd_numbers(self):
        # [-3, -5] -> both ignored (negative) -> 0
        assert double_the_difference([-3, -5]) == 0

    def test_even_positive_numbers(self):
        # [2, 4, 6, 8] -> all even -> 0
        assert double_the_difference([2, 4, 6, 8]) == 0


class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_smallest_positive_odd(self):
        # [1] -> 1^2 = 1
        assert double_the_difference([1]) == 1

    def test_largest_common_odd(self):
        # [99] -> 99^2 = 9801
        assert double_the_difference([99]) == 9801

    def test_boundary_between_even_and_odd(self):
        # [2, 3] -> 3^2 = 9
        assert double_the_difference([2, 3]) == 9

    def test_zero_is_not_odd(self):
        # [0, 1] -> 1^2 = 1
        assert double_the_difference([0, 1]) == 1

    def test_negative_one_not_included(self):
        # [-1] -> -1 % 2 == -1 != 1, and -1 < 0 -> 0
        assert double_the_difference([-1]) == 0

    def test_many_zeros(self):
        # [0, 0, 0, 0] -> 0
        assert double_the_difference([0, 0, 0, 0]) == 0

    def test_alternating_odd_even(self):
        # [1, 2, 3, 4, 5, 6] -> 1 + 9 + 25 = 35
        assert double_the_difference([1, 2, 3, 4, 5, 6]) == 35


class TestEmptyAndZeroSizeInputs:
    """Tests for empty, null, or zero-size inputs."""

    def test_empty_list(self):
        assert double_the_difference([]) == 0

    def test_list_of_only_zeros(self):
        assert double_the_difference([0, 0, 0]) == 0

    def test_list_of_only_negatives(self):
        assert double_the_difference([-1, -2, -3]) == 0

    def test_list_of_only_evens(self):
        assert double_the_difference([2, 4, 6, 8, 10]) == 0


class TestNonIntegerInputs:
    """Tests for non-integer numeric inputs (floats)."""

    def test_float_odd_like(self):
        # [1.5] -> not an integer -> 0
        assert double_the_difference([1.5]) == 0

    def test_float_even_like(self):
        # [3.5] -> not an integer -> 0
        assert double_the_difference([3.5]) == 0

    def test_negative_float(self):
        # [-1.5] -> not an integer -> 0
        assert double_the_difference([-1.5]) == 0

    def test_mixed_int_and_float(self):
        # [1, 2.5, 3] -> 1^2 + 3^2 = 10
        assert double_the_difference([1, 2.5, 3]) == 10

    def test_integer_as_float(self):
        # [2.0] -> "." in str(2.0) -> not treated as int -> 0
        assert double_the_difference([2.0]) == 0

    def test_positive_float(self):
        # [5.0] -> "." in str(5.0) -> not treated as int -> 0
        assert double_the_difference([5.0]) == 0

    def test_various_floats(self):
        # [1.0, 3.0, 5.0] -> all have "." in str -> 0
        assert double_the_difference([1.0, 3.0, 5.0]) == 0


class TestBooleanInputs:
    """Tests for boolean values (bool is subclass of int in Python)."""

    def test_true_value(self):
        # True == 1, which is odd and positive -> 1^2 = 1
        assert double_the_difference([True]) == 1

    def test_false_value(self):
        # False == 0, which is even -> 0
        assert double_the_difference([False]) == 0

    def test_mixed_bool_and_int(self):
        # [True, 3, False] -> 1^2 + 3^2 = 1 + 9 = 10
        assert double_the_difference([True, 3, False]) == 10

    def test_all_booleans(self):
        # [True, True] -> 1 + 1 = 2
        assert double_the_difference([True, True]) == 2


class TestExceptionCases:
    """Tests for inputs that may raise exceptions."""

    def test_none_element(self):
        # None % 2 raises TypeError
        with pytest.raises(TypeError):
            double_the_difference([1, None, 3])

    def test_string_element(self):
        # "a" % 2 raises TypeError
        with pytest.raises(TypeError):
            double_the_difference([1, "a", 3])

    def test_list_element(self):
        # [1] % 2 raises TypeError
        with pytest.raises(TypeError):
            double_the_difference([1, [2], 3])

    def test_dict_element(self):
        # {"a": 1} % 2 raises TypeError
        with pytest.raises(TypeError):
            double_the_difference([1, {"a": 1}, 3])

    def test_tuple_element(self):
        # (1,) % 2 raises TypeError
        with pytest.raises(TypeError):
            double_the_difference([1, (2,), 3])

    def test_complex_number(self):
        # Complex numbers don't support % 2
        with pytest.raises(TypeError):
            double_the_difference([1, 2j, 3])

    def test_inf_ignored(self):
        # float('inf') % 2 returns nan, which != 1, so it's ignored
        assert double_the_difference([float('inf')]) == 0

    def test_nan_ignored(self):
        # float('nan') % 2 returns nan, which != 1, so it's ignored
        assert double_the_difference([float('nan')]) == 0

    def test_inf_with_valid_odds(self):
        # [1, float('inf'), 3] -> 1 + 9 = 10
        assert double_the_difference([1, float('inf'), 3]) == 10

    def test_nan_with_valid_odds(self):
        # [1, float('nan'), 3] -> 1 + 9 = 10
        assert double_the_difference([1, float('nan'), 3]) == 10


class TestEdgeBehavior:
    """Additional edge-case behaviors."""

    def test_duplicate_odds(self):
        # [3, 3, 3] -> 9 + 9 + 9 = 27
        assert double_the_difference([3, 3, 3]) == 27

    def test_large_list(self):
        # Sum of squares of all odd numbers from 1 to 99
        # Odds: 1, 3, 5, ..., 99 -> 50 numbers
        # Sum = sum(k^2 for k in range(1, 100, 2)) = 166650
        lst = list(range(1, 100))
        assert double_the_difference(lst) == 166650

    def test_all_same_odd(self):
        # [7, 7, 7, 7, 7] -> 49 * 5 = 245
        assert double_the_difference([7, 7, 7, 7, 7]) == 245

    def test_order_doesnt_matter(self):
        # Same elements, different order
        assert double_the_difference([5, 1, 3]) == double_the_difference([3, 5, 1])

    def test_negative_with_positive_odd(self):
        # [-3, 5] -> 5^2 = 25
        assert double_the_difference([-3, 5]) == 25

    def test_zero_with_odd(self):
        # [0, 1, 0, 3, 0] -> 1 + 9 = 10
        assert double_the_difference([0, 1, 0, 3, 0]) == 10
