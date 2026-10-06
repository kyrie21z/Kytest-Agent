"""Unit tests for solution.monotonic."""

import pytest
from solution import monotonic


class TestMonotonicIncreasing:
    """Tests for monotonically increasing lists."""

    def test_strictly_increasing(self):
        assert monotonic([1, 2, 4, 20]) is True

    def test_two_elements_increasing(self):
        assert monotonic([1, 5]) is True

    def test_single_element(self):
        assert monotonic([42]) is True

    def test_all_same_elements(self):
        assert monotonic([3, 3, 3, 3]) is True

    def test_increasing_with_negatives(self):
        assert monotonic([-5, -3, 0, 7]) is True

    def test_increasing_mixed_signs(self):
        assert monotonic([-2, -1, 0, 1, 2]) is True

    def test_increasing_floats(self):
        assert monotonic([1.1, 2.2, 3.3]) is True

    def test_docstring_example_1(self):
        """From docstring: monotonic([1, 2, 4, 20]) -> True"""
        assert monotonic([1, 2, 4, 20]) is True


class TestMonotonicDecreasing:
    """Tests for monotonically decreasing lists."""

    def test_strictly_decreasing(self):
        assert monotonic([4, 1, 0, -10]) is True

    def test_two_elements_decreasing(self):
        assert monotonic([10, 5]) is True

    def test_docstring_example_3(self):
        """From docstring: monotonic([4, 1, 0, -10]) -> True"""
        assert monotonic([4, 1, 0, -10]) is True

    def test_decreasing_with_positives(self):
        assert monotonic([100, 50, 25, 10]) is True

    def test_decreasing_mixed_signs(self):
        assert monotonic([5, 3, 1, -2, -8]) is True

    def test_decreasing_floats(self):
        assert monotonic([5.5, 3.3, 1.1]) is True


class TestNonMonotonic:
    """Tests for non-monotonic lists."""

    def test_docstring_example_2(self):
        """From docstring: monotonic([1, 20, 4, 10]) -> False"""
        assert monotonic([1, 20, 4, 10]) is False

    def test_up_then_down(self):
        assert monotonic([1, 3, 2]) is False

    def test_down_then_up(self):
        assert monotonic([5, 2, 4]) is False

    def test_v_shape(self):
        assert monotonic([10, 1, 10]) is False

    def test_w_shape(self):
        assert monotonic([1, 3, 1, 3, 1]) is False

    def test_zigzag(self):
        assert monotonic([1, 2, 1, 2, 1]) is False

    def test_large_jumps(self):
        assert monotonic([1, 100, 2, 99]) is False

    def test_three_elements_not_monotonic(self):
        assert monotonic([1, 3, 2]) is False


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_list(self):
        assert monotonic([]) is True

    def test_one_element(self):
        assert monotonic([1]) is True

    def test_two_equal_elements(self):
        assert monotonic([5, 5]) is True

    def test_two_different_elements_increasing(self):
        assert monotonic([1, 2]) is True

    def test_two_different_elements_decreasing(self):
        assert monotonic([2, 1]) is True

    def test_all_zeros(self):
        assert monotonic([0, 0, 0, 0]) is True

    def test_alternating_equal_and_increase(self):
        assert monotonic([1, 1, 2, 2, 3]) is True

    def test_alternating_equal_and_decrease(self):
        assert monotonic([5, 5, 3, 3, 1]) is True


class TestLargeInputs:
    """Tests with larger inputs."""

    def test_long_increasing_sequence(self):
        lst = list(range(1000))
        assert monotonic(lst) is True

    def test_long_decreasing_sequence(self):
        lst = list(range(1000, 0, -1))
        assert monotonic(lst) is True

    def test_long_non_monotonic(self):
        lst = [i if i % 2 == 0 else 1000 - i for i in range(100)]
        assert monotonic(lst) is False
