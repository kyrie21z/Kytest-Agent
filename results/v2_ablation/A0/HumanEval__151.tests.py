"""Unit tests for solution.double_the_difference."""

import pytest
from solution import double_the_difference


class TestDoubleTheDifferenceBasic:
    """Tests for basic functionality with odd positive integers."""

    def test_single_odd(self):
        assert double_the_difference([1]) == 1

    def test_multiple_odds(self):
        assert double_the_difference([1, 3, 5]) == 1 + 9 + 25  # 35

    def test_mixed_with_evens(self):
        assert double_the_difference([1, 3, 2, 0]) == 1 + 9  # 10

    def test_all_evens(self):
        assert double_the_difference([2, 4, 6, 8]) == 0

    def test_empty_list(self):
        assert double_the_difference([]) == 0


class TestDoubleTheDifferenceNegatives:
    """Tests for handling negative numbers."""

    def test_negative_odds(self):
        assert double_the_difference([-1, -3, -5]) == 0

    def test_negative_and_positive(self):
        assert double_the_difference([-1, -2, 0]) == 0

    def test_mixed_negative_positive(self):
        assert double_the_difference([9, -2]) == 81

    def test_only_negatives_with_one_odd(self):
        assert double_the_difference([-3, -5, 7]) == 49


class TestDoubleTheDifferenceZeros:
    """Tests for handling zero."""

    def test_zero_alone(self):
        assert double_the_difference([0]) == 0

    def test_zeros_and_odds(self):
        assert double_the_difference([0, 1, 0, 3]) == 1 + 9  # 10

    def test_all_zeros(self):
        assert double_the_difference([0, 0, 0]) == 0


class TestDoubleTheDifferenceFloats:
    """Tests for handling floating-point numbers."""

    def test_float_not_integer(self):
        assert double_the_difference([3.5]) == 0

    def test_float_even_like(self):
        assert double_the_difference([2.0]) == 0

    def test_mixed_integers_and_floats(self):
        assert double_the_difference([1, 3.5, 5, 2.0]) == 1 + 25  # 26

    def test_negative_float(self):
        assert double_the_difference([-3.5]) == 0

    def test_large_float(self):
        assert double_the_difference([100.7]) == 0


class TestDoubleTheDifferenceEdgeCases:
    """Tests for edge cases."""

    def test_single_even(self):
        assert double_the_difference([2]) == 0

    def test_single_zero(self):
        assert double_the_difference([0]) == 0

    def test_single_negative(self):
        assert double_the_difference([-5]) == 0

    def test_single_large_odd(self):
        assert double_the_difference([99]) == 9801

    def test_single_largest_odd(self):
        assert double_the_difference([999]) == 998001

    def test_duplicate_odds(self):
        assert double_the_difference([3, 3, 3]) == 9 + 9 + 9  # 27

    def test_duplicate_evens(self):
        assert double_the_difference([2, 2, 2]) == 0


class TestDoubleTheDifferenceMixed:
    """Tests for mixed input scenarios."""

    def test_complex_mixed(self):
        lst = [1, 2, 3, 4, 5, 6, 7]
        expected = 1 + 9 + 25 + 49  # 84
        assert double_the_difference(lst) == expected

    def test_all_same_odd(self):
        assert double_the_difference([5, 5, 5, 5]) == 4 * 25  # 100

    def test_alternating_odd_even(self):
        assert double_the_difference([1, 2, 3, 4, 5]) == 1 + 9 + 25  # 35

    def test_many_elements(self):
        lst = list(range(1, 21))  # [1, 2, ..., 20]
        odds = [n for n in range(1, 21, 2)]
        expected = sum(n ** 2 for n in odds)
        assert double_the_difference(lst) == expected

    def test_negative_then_positive(self):
        assert double_the_difference([-5, -3, -1, 1, 3, 5]) == 1 + 9 + 25  # 35


class TestDoubleTheDifferenceLargeValues:
    """Tests for large number inputs."""

    def test_large_odd(self):
        val = 9999
        assert double_the_difference([val]) == val ** 2  # 99980001

    def test_multiple_large_odds(self):
        vals = [101, 103, 105]
        expected = sum(v ** 2 for v in vals)
        assert double_the_difference(vals) == expected

    def test_very_large_list(self):
        lst = list(range(1, 1001, 2))  # All odd numbers from 1 to 999
        expected = sum(n ** 2 for n in lst)
        assert double_the_difference(lst) == expected
