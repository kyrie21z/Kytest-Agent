"""Unit tests for solution.double_the_difference."""

import pytest
from solution import double_the_difference


# ──────────────────────────────────────────────
# 1. Normal cases – typical inputs
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with straightforward, expected inputs."""

    def test_basic_example_from_docstring(self):
        # [1, 3, 2, 0] → odd positives: 1, 3 → 1² + 3² = 10
        assert double_the_difference([1, 3, 2, 0]) == 10

    def test_negative_and_even_numbers_ignored(self):
        # [-1, -2, 0] → no positive odds → 0
        assert double_the_difference([-1, -2, 0]) == 0

    def test_single_odd_positive(self):
        # [9] → 9² = 81
        assert double_the_difference([9, -2]) == 81

    def test_all_even_numbers(self):
        # [2, 4, 6] → no odds → 0
        assert double_the_difference([2, 4, 6]) == 0

    def test_mixed_list(self):
        # [1, 5, 7] → all positive odds → 1 + 25 + 49 = 75
        assert double_the_difference([1, 5, 7]) == 75

    def test_larger_odd(self):
        # [11] → 121
        assert double_the_difference([11]) == 121

    def test_multiple_odds_with_evens(self):
        # [3, 4, 5, 6, 7] → 3²+5²+7² = 9+25+49 = 83
        assert double_the_difference([3, 4, 5, 6, 7]) == 83


# ──────────────────────────────────────────────
# 2. Boundary cases – edges of valid input ranges
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the boundaries of what counts as a "positive odd integer"."""

    def test_zero_is_not_included(self):
        # 0 is even, not odd → excluded
        assert double_the_difference([0]) == 0

    def test_one_is_smallest_positive_odd(self):
        # 1² = 1
        assert double_the_difference([1]) == 1

    def test_two_is_excluded_even(self):
        # 2 is even → excluded
        assert double_the_difference([2]) == 0

    def test_negative_one_is_excluded(self):
        # -1 is odd but negative → excluded
        assert double_the_difference([-1]) == 0

    def test_negative_odd(self):
        # -3 is odd but negative → excluded
        assert double_the_difference([-3]) == 0

    def test_large_positive_odd(self):
        # 999² = 998001
        assert double_the_difference([999]) == 998001


# ──────────────────────────────────────────────
# 3. Empty, null, or zero-size inputs
# ──────────────────────────────────────────────

class TestEmptyAndZeroInputs:
    """Tests with empty or edge-case containers."""

    def test_empty_list(self):
        assert double_the_difference([]) == 0

    def test_list_with_only_zeros(self):
        assert double_the_difference([0, 0, 0]) == 0

    def test_list_with_only_negatives(self):
        assert double_the_difference([-5, -3, -1]) == 0

    def test_list_with_only_evens(self):
        assert double_the_difference([2, 4, 8, 10]) == 0


# ──────────────────────────────────────────────
# 4. Invalid / non-integer inputs
# ──────────────────────────────────────────────

class TestNonIntegerInputs:
    """Tests where elements are not integers (floats, strings, etc.)."""

    def test_float_that_looks_like_integer(self):
        # 1.0 has "." in str(1.0) → excluded by the check
        assert double_the_difference([1.0]) == 0

    def test_float_odd(self):
        # 3.5 is not an integer → excluded
        assert double_the_difference([3.5]) == 0

    def test_negative_float(self):
        # -2.5 is not an integer → excluded
        assert double_the_difference([-2.5]) == 0

    def test_boolean_true(self):
        # True == 1, True % 2 == 1, True > 0, "." not in "True" → included
        # True² = 1
        assert double_the_difference([True]) == 1

    def test_boolean_false(self):
        # False == 0, 0 % 2 == 0 → excluded
        assert double_the_difference([False]) == 0

    def test_mixed_integers_and_floats(self):
        # [1, 2.5, 3] → 1² + 3² = 10
        assert double_the_difference([1, 2.5, 3]) == 10


# ──────────────────────────────────────────────
# 5. Exception cases
# ──────────────────────────────────────────────

class TestExceptionCases:
    """Tests that may raise exceptions due to invalid element types."""

    def test_none_raises_type_error(self):
        # None % 2 raises TypeError
        with pytest.raises(TypeError):
            double_the_difference([None])

    def test_dict_raises_type_error(self):
        # dict % 2 raises TypeError
        with pytest.raises(TypeError):
            double_the_difference([{}])

    def test_nested_list_raises_type_error(self):
        # list % 2 raises TypeError
        with pytest.raises(TypeError):
            double_the_difference([[1]])

    def test_tuple_raises_type_error(self):
        with pytest.raises(TypeError):
            double_the_difference([(1, 2)])

    def test_set_raises_type_error(self):
        with pytest.raises(TypeError):
            double_the_difference([{1}])

    def test_string_raises_type_error(self):
        # String % 2 raises TypeError
        with pytest.raises(TypeError):
            double_the_difference(["1", "3"])


# ──────────────────────────────────────────────
# 6. Additional edge / stress cases
# ──────────────────────────────────────────────

class TestAdditionalCases:
    """Extra cases for thorough coverage."""

    def test_repeated_same_odd(self):
        # [3, 3, 3] → 9 + 9 + 9 = 27
        assert double_the_difference([3, 3, 3]) == 27

    def test_alternating_pos_neg_odds(self):
        # [1, -3, 5, -7, 9] → 1 + 25 + 81 = 107
        assert double_the_difference([1, -3, 5, -7, 9]) == 107

    def test_all_elements_are_positive_odds(self):
        # [1, 3, 5, 7, 9] → 1+9+25+49+81 = 165
        assert double_the_difference([1, 3, 5, 7, 9]) == 165

    def test_single_element_list(self):
        assert double_the_difference([7]) == 49

    def test_many_zeros(self):
        assert double_the_difference([0] * 100) == 0

    def test_large_list_of_odds(self):
        # Sum of squares of first 10 positive odd numbers:
        # 1²+3²+5²+7²+9²+11²+13²+15²+17²+19² = 1330
        assert double_the_difference(list(range(1, 20, 2))) == 1330

    def test_consecutive_positive_odds(self):
        # [1, 3, 5, 7, 9] → 1+9+25+49+81 = 165
        assert double_the_difference([1, 3, 5, 7, 9]) == 165

    def test_large_list_all_filtered(self):
        # Large list with no qualifying elements → 0
        lst = [2 * i for i in range(1, 101)]  # [2, 4, ..., 200]
        assert double_the_difference(lst) == 0

    def test_large_list_all_qualifying(self):
        # Large list with all positive odds → sum of squares of 1,3,...,99
        lst = [2 * i - 1 for i in range(1, 51)]  # [1, 3, ..., 99]
        expected = sum(n ** 2 for n in lst)
        assert double_the_difference(lst) == expected
