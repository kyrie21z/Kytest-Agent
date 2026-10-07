"""Unit tests for the monotonic function in solution.py."""

import pytest
from solution import monotonic


class TestMonotonicIncreasing:
    """Tests for monotonically increasing lists."""

    def test_strictly_increasing(self):
        assert monotonic([1, 2, 4, 20]) is True

    def test_increasing_with_duplicates(self):
        assert monotonic([1, 1, 2, 3, 3, 5]) is True

    def test_single_element_increasing(self):
        assert monotonic([42]) is True

    def test_two_elements_increasing(self):
        assert monotonic([1, 2]) is True

    def test_all_same_elements(self):
        assert monotonic([5, 5, 5, 5]) is True

    def test_negative_increasing(self):
        assert monotonic([-5, -3, -1, 0, 2]) is True

    def test_mixed_positive_negative_increasing(self):
        assert monotonic([-10, -5, 0, 5, 10]) is True

    def test_float_increasing(self):
        assert monotonic([1.1, 2.2, 3.3, 4.4]) is True

    def test_large_increasing_list(self):
        assert monotonic(list(range(1000))) is True


class TestMonotonicDecreasing:
    """Tests for monotonically decreasing lists."""

    def test_strictly_decreasing(self):
        assert monotonic([4, 1, 0, -10]) is True

    def test_decreasing_with_duplicates(self):
        assert monotonic([5, 5, 4, 3, 3, 1]) is True

    def test_single_element_decreasing(self):
        assert monotonic([7]) is True

    def test_two_elements_decreasing(self):
        assert monotonic([10, 5]) is True

    def test_negative_decreasing(self):
        assert monotonic([0, -1, -3, -10]) is True

    def test_float_decreasing(self):
        assert monotonic([5.5, 4.4, 3.3, 2.2]) is True

    def test_large_decreasing_list(self):
        assert monotonic(list(range(1000, 0, -1))) is True


class TestNotMonotonic:
    """Tests for lists that are neither increasing nor decreasing."""

    def test_not_monotonic_basic(self):
        assert monotonic([1, 20, 4, 10]) is False

    def test_not_monotonic_v_shape(self):
        assert monotonic([1, 3, 2, 4]) is False

    def test_not_monotonic_inverted_v(self):
        assert monotonic([5, 3, 4, 2]) is False

    def test_not_monotonic_alternating(self):
        assert monotonic([1, 3, 2, 4, 3, 5]) is False

    def test_not_monotonic_three_elements(self):
        assert monotonic([1, 3, 2]) is False

    def test_not_monotonic_four_elements(self):
        assert monotonic([1, 2, 1, 2]) is False

    def test_not_monotonic_with_zeros(self):
        assert monotonic([0, 1, 0, 1]) is False

    def test_not_monotonic_large_list(self):
        assert monotonic([1, 2, 3, 2, 1, 0, 1, 2, 3]) is False


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_list(self):
        assert monotonic([]) is True

    def test_two_equal_elements(self):
        assert monotonic([3, 3]) is True

    def test_two_different_elements_increasing(self):
        assert monotonic([1, 99]) is True

    def test_two_different_elements_decreasing(self):
        assert monotonic([99, 1]) is True

    def test_all_zeros(self):
        assert monotonic([0, 0, 0, 0, 0]) is True

    def test_single_zero(self):
        assert monotonic([0]) is True

    def test_very_large_numbers(self):
        assert monotonic([10**18, 10**18 + 1, 10**18 + 2]) is True

    def test_very_small_numbers(self):
        assert monotonic([-10**18, -(10**18 + 1), -(10**18 + 2)]) is True

    def test_mixed_signs_not_monotonic(self):
        assert monotonic([-5, 5, -5, 5]) is False


class TestDocstringExamples:
    """Verify the examples from the docstring pass."""

    def test_docstring_example_1(self):
        # >>> monotonic([1, 2, 4, 20]) -> True
        assert monotonic([1, 2, 4, 20]) is True

    def test_docstring_example_2(self):
        # >>> monotonic([1, 20, 4, 10]) -> False
        assert monotonic([1, 20, 4, 10]) is False

    def test_docstring_example_3(self):
        # >>> monotonic([4, 1, 0, -10]) -> True
        assert monotonic([4, 1, 0, -10]) is True
