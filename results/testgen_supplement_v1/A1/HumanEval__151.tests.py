"""Unit tests for solution.double_the_difference."""

import pytest
from solution import double_the_difference


class TestNormalCases:
    """Tests with typical valid inputs."""

    def test_simple_mixed_list(self):
        # [1, 3, 2, 0] -> odd positives: 1, 3 -> 1^2 + 3^2 = 1 + 9 = 10
        assert double_the_difference([1, 3, 2, 0]) == 10

    def test_single_odd_positive(self):
        # [9] -> 9^2 = 81
        assert double_the_difference([9]) == 81

    def test_multiple_odd_positives(self):
        # [1, 3, 5] -> 1 + 9 + 25 = 35
        assert double_the_difference([1, 3, 5]) == 35

    def test_all_even_numbers(self):
        # [2, 4, 6] -> no odd numbers -> 0
        assert double_the_difference([2, 4, 6]) == 0

    def test_negative_and_positive_odds(self):
        # [9, -2] -> only 9 is odd positive -> 81
        assert double_the_difference([9, -2]) == 81

    def test_large_odd_number(self):
        # [7] -> 49
        assert double_the_difference([7]) == 49

    def test_many_elements(self):
        # [1, 2, 3, 4, 5, 6, 7] -> odds: 1, 3, 5, 7 -> 1+9+25+49 = 84
        assert double_the_difference([1, 2, 3, 4, 5, 6, 7]) == 84


class TestBoundaryCases:
    """Tests at edges of valid input ranges."""

    def test_smallest_odd_positive(self):
        # [1] -> 1^2 = 1
        assert double_the_difference([1]) == 1

    def test_largest_odd_positive(self):
        # [99999] -> 99999^2 = 9999800001
        assert double_the_difference([99999]) == 99999 ** 2

    def test_zero_is_excluded(self):
        # [0] -> 0 is even, so ignored -> 0
        assert double_the_difference([0]) == 0

    def test_neg_one_is_excluded(self):
        # [-1] -> negative, so ignored -> 0
        assert double_the_difference([-1]) == 0

    def test_two_is_excluded(self):
        # [2] -> even, so ignored -> 0
        assert double_the_difference([2]) == 0

    def test_only_boundary_values(self):
        # [0, 1, 2, -1] -> only 1 qualifies -> 1
        assert double_the_difference([0, 1, 2, -1]) == 1


class TestEmptyNullZeroSizeInputs:
    """Tests for empty, null, or zero-size inputs."""

    def test_empty_list(self):
        assert double_the_difference([]) == 0

    def test_list_with_only_zeros(self):
        # [0, 0, 0] -> all even -> 0
        assert double_the_difference([0, 0, 0]) == 0

    def test_list_with_only_negatives(self):
        # [-1, -3, -5] -> all negative -> 0
        assert double_the_difference([-1, -3, -5]) == 0

    def test_list_with_only_evens(self):
        # [2, 4, 6, 8] -> all even -> 0
        assert double_the_difference([2, 4, 6, 8]) == 0


class TestInvalidInputsNonIntegers:
    """Tests for non-integer inputs (floats, etc.)."""

    def test_float_odd_like_3_5(self):
        # [3.5] -> has "." in str -> ignored -> 0
        assert double_the_difference([3.5]) == 0

    def test_float_even_like_2_0(self):
        # [2.0] -> has "." in str -> ignored -> 0
        assert double_the_difference([2.0]) == 0

    def test_mixed_int_and_float(self):
        # [1, 2.5, 3] -> 1 and 3 qualify -> 1 + 9 = 10
        assert double_the_difference([1, 2.5, 3]) == 10

    def test_negative_float(self):
        # [-3.5] -> has "." -> ignored -> 0
        assert double_the_difference([-3.5]) == 0

    def test_boolean_true(self):
        # True is technically 1 in Python. True % 2 == 1, True > 0, "." not in str(True) -> "True"
        # So True would qualify as odd positive integer by the function's logic.
        result = double_the_difference([True])
        assert result == 1

    def test_boolean_false(self):
        # False == 0, False % 2 == 0, so it fails the odd check -> 0
        assert double_the_difference([False]) == 0


class TestExceptionCases:
    """Tests where the function can raise exceptions."""

    def test_list_with_strings_raises(self):
        # Strings don't support % 2 operation -> TypeError
        with pytest.raises(TypeError):
            double_the_difference(["3"])

    def test_list_with_none_raises(self):
        # None doesn't support % 2 -> TypeError
        with pytest.raises(TypeError):
            double_the_difference([None])

    def test_list_with_mixed_valid_invalid(self):
        # Mix of valid ints and invalid types -> TypeError from the invalid element
        with pytest.raises(TypeError):
            double_the_difference([1, "hello", 3])

    def test_list_with_dict_raises(self):
        with pytest.raises(TypeError):
            double_the_difference([{"a": 1}])

    def test_list_with_tuple_raises(self):
        with pytest.raises(TypeError):
            double_the_difference([(1, 2)])


class TestEdgeBehavior:
    """Additional edge cases around function behavior."""

    def test_duplicate_odd_numbers(self):
        # [3, 3, 3] -> 9 + 9 + 9 = 27
        assert double_the_difference([3, 3, 3]) == 27

    def test_alternating_odd_even(self):
        # [1, 2, 3, 4, 5] -> 1 + 9 + 25 = 35
        assert double_the_difference([1, 2, 3, 4, 5]) == 35

    def test_negative_odd_with_positive_odd(self):
        # [-3, 5] -> only 5 qualifies -> 25
        assert double_the_difference([-3, 5]) == 25

    def test_large_list_of_odds(self):
        # Sum of squares of 1, 3, 5, ..., 99
        odds = list(range(1, 100, 2))
        expected = sum(o ** 2 for o in odds)
        assert double_the_difference(odds) == expected

    def test_float_that_looks_like_integer(self):
        # [3.0] -> "." in str("3.0") -> ignored -> 0
        assert double_the_difference([3.0]) == 0

    def test_negative_even(self):
        # [-2] -> negative -> ignored -> 0
        assert double_the_difference([-2]) == 0

    def test_single_large_element(self):
        # [101] -> 101^2 = 10201
        assert double_the_difference([101]) == 10201
