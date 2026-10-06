"""Unit tests for solution.monotonic."""

import pytest
from solution import monotonic


class TestMonotonicIncreasingCases:
    """Tests for lists that are monotonically increasing."""

    def test_strictly_increasing(self):
        assert monotonic([1, 2, 4, 20]) is True

    def test_two_elements_increasing(self):
        assert monotonic([1, 2]) is True

    def test_single_element(self):
        assert monotonic([5]) is True

    def test_empty_list(self):
        assert monotonic([]) is True

    def test_all_equal_elements(self):
        assert monotonic([3, 3, 3, 3]) is True

    def test_non_decreasing_with_duplicates(self):
        assert monotonic([1, 2, 2, 3]) is True

    def test_negative_numbers_increasing(self):
        assert monotonic([-5, -3, -1, 0]) is True

    def test_floats_increasing(self):
        assert monotonic([1.1, 2.2, 3.3]) is True

    def test_mixed_sign_increasing(self):
        assert monotonic([-3, -1, 0, 2]) is True


class TestMonotonicDecreasingCases:
    """Tests for lists that are monotonically decreasing."""

    def test_strictly_decreasing(self):
        assert monotonic([4, 1, 0, -10]) is True

    def test_two_elements_decreasing(self):
        assert monotonic([5, 3]) is True

    def test_all_equal_elements_decreasing(self):
        assert monotonic([7, 7, 7]) is True

    def test_non_increasing_with_duplicates(self):
        assert monotonic([5, 5, 3, 3, 1]) is True

    def test_negative_numbers_decreasing(self):
        assert monotonic([0, -1, -3, -10]) is True

    def test_floats_decreasing(self):
        assert monotonic([5.5, 3.3, 1.1]) is True


class TestNonMonotonicCases:
    """Tests for lists that are neither increasing nor decreasing."""

    def test_up_then_down(self):
        assert monotonic([1, 20, 4, 10]) is False

    def test_down_then_up(self):
        assert monotonic([5, 3, 7, 1]) is False

    def test_v_shaped(self):
        assert monotonic([3, 1, 4, 2]) is False

    def test_w_shaped(self):
        assert monotonic([1, 3, 1, 3, 1]) is False

    def test_three_elements_not_monotonic(self):
        assert monotonic([1, 3, 2]) is False

    def test_alternating(self):
        assert monotonic([1, 2, 1, 2, 1]) is False

    def test_large_jitter(self):
        assert monotonic([1, 10, 2, 9, 3, 8]) is False


class TestBoundaryCases:
    """Edge case boundary tests."""

    def test_two_equal_elements(self):
        assert monotonic([4, 4]) is True

    def test_two_different_elements_increasing(self):
        assert monotonic([1, 2]) is True

    def test_two_different_elements_decreasing(self):
        assert monotonic([2, 1]) is True

    def test_zero_length_list(self):
        assert monotonic([]) is True

    def test_single_element_list(self):
        assert monotonic([0]) is True

    def test_one_element_change(self):
        # Only one comparison, must be monotonic
        assert monotonic([10, 5]) is True

    def test_large_values(self):
        assert monotonic([0, 10**9, 2 * 10**9]) is True

    def test_large_negative_values(self):
        assert monotonic([0, -(10**9), -(2 * 10**9)]) is True

    def test_many_equal_elements(self):
        assert monotonic([1] * 1000) is True

    def test_strictly_increasing_many_elements(self):
        assert monotonic(list(range(1000))) is True

    def test_strictly_decreasing_many_elements(self):
        assert monotonic(list(range(1000, 0, -1))) is True


class TestMixedSignCases:
    """Tests involving mixed positive and negative values."""

    def test_positive_to_negative_increasing(self):
        assert monotonic([-5, -3, -1, 1, 3]) is True

    def test_positive_to_negative_decreasing(self):
        assert monotonic([5, 3, 1, -1, -3]) is True

    def test_crossing_zero_increasing(self):
        assert monotonic([-2, -1, 0, 1, 2]) is True

    def test_crossing_zero_decreasing(self):
        assert monotonic([2, 1, 0, -1, -2]) is True

    def test_mixed_sign_not_monotonic(self):
        assert monotonic([-1, 2, -3]) is False
