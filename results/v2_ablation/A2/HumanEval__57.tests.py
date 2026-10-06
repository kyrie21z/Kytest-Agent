"""Unit tests for the monotonic() function in solution.py."""

import pytest
from solution import monotonic


# ---------------------------------------------------------------------------
# 1. Docstring examples (the given doctests)
# ---------------------------------------------------------------------------

class TestDocstringExamples:
    def test_increasing(self):
        """[1, 2, 4, 20] is monotonically increasing -> True"""
        assert monotonic([1, 2, 4, 20]) is True

    def test_not_monotonic(self):
        """[1, 20, 4, 10] goes up then down -> False"""
        assert monotonic([1, 20, 4, 10]) is False

    def test_decreasing(self):
        """[4, 1, 0, -10] is monotonically decreasing -> True"""
        assert monotonic([4, 1, 0, -10]) is True


# ---------------------------------------------------------------------------
# 2. Empty and single-element inputs
# ---------------------------------------------------------------------------

class TestEmptyAndSingleton:
    def test_empty_list(self):
        """An empty list is trivially monotonic."""
        assert monotonic([]) is True

    def test_single_element(self):
        """A single-element list is trivially monotonic."""
        assert monotonic([42]) is True


# ---------------------------------------------------------------------------
# 3. Two-element lists (boundary of "at least two items")
# ---------------------------------------------------------------------------

class TestTwoElements:
    def test_strictly_increasing(self):
        assert monotonic([1, 2]) is True

    def test_strictly_decreasing(self):
        assert monotonic([2, 1]) is True

    def test_equal_elements(self):
        assert monotonic([5, 5]) is True

    def test_negative_increasing(self):
        assert monotonic([-3, -1]) is True

    def test_negative_decreasing(self):
        assert monotonic([-1, -3]) is True

    def test_mixed_sign_increasing(self):
        assert monotonic([-1, 1]) is True

    def test_mixed_sign_decreasing(self):
        assert monotonic([1, -1]) is True


# ---------------------------------------------------------------------------
# 4. Monotonically increasing (various forms)
# ---------------------------------------------------------------------------

class TestMonotonicallyIncreasing:
    def test_strictly_increasing(self):
        assert monotonic([1, 2, 3, 4, 5]) is True

    def test_non_decreasing_with_duplicates(self):
        assert monotonic([1, 2, 2, 3, 3, 3]) is True

    def test_all_same(self):
        assert monotonic([7, 7, 7, 7]) is True

    def test_two_step_increase(self):
        assert monotonic([0, 10, 20, 30]) is True

    def test_large_values(self):
        assert monotonic([0, 1_000_000, 2_000_000]) is True

    def test_negative_to_positive(self):
        assert monotonic([-5, -3, 0, 2, 7]) is True

    def test_single_step_then_flat(self):
        assert monotonic([1, 1, 1, 2, 2]) is True


# ---------------------------------------------------------------------------
# 5. Monotonically decreasing (various forms)
# ---------------------------------------------------------------------------

class TestMonotonicallyDecreasing:
    def test_strictly_decreasing(self):
        assert monotonic([5, 4, 3, 2, 1]) is True

    def test_non_increasing_with_duplicates(self):
        assert monotonic([5, 5, 3, 3, 1, 1]) is True

    def test_all_same(self):
        assert monotonic([7, 7, 7, 7]) is True

    def test_two_step_decrease(self):
        assert monotonic([30, 20, 10, 0]) is True

    def test_large_values(self):
        assert monotonic([2_000_000, 1_000_000, 0]) is True

    def test_positive_to_negative(self):
        assert monotonic([7, 2, 0, -3, -5]) is True

    def test_single_step_then_flat(self):
        assert monotonic([2, 2, 1, 1, 1]) is True


# ---------------------------------------------------------------------------
# 6. Not monotonic – various patterns
# ---------------------------------------------------------------------------

class TestNotMonotonic:
    def test_up_then_down(self):
        assert monotonic([1, 3, 2]) is False

    def test_down_then_up(self):
        assert monotonic([3, 1, 2]) is False

    def test_docstring_example(self):
        assert monotonic([1, 20, 4, 10]) is False

    def test_multiple_peaks(self):
        assert monotonic([1, 5, 2, 6, 3]) is False

    def test_plateau_then_change_direction(self):
        # [1, 2, 2, 1] is non-decreasing then non-increasing, not purely one way
        assert monotonic([1, 2, 2, 1]) is False

    def test_plateau_then_opposite(self):
        assert monotonic([3, 3, 4, 2]) is False

    def test_wide_v_pattern(self):
        assert monotonic([5, 3, 4, 2]) is False

    def test_longer_not_monotonic(self):
        assert monotonic([1, 2, 3, 2, 1]) is False

    def test_alternating(self):
        assert monotonic([1, 2, 1, 2, 1]) is False


# ---------------------------------------------------------------------------
# 7. Boundary / edge values
# ---------------------------------------------------------------------------

class TestBoundaryValues:
    def test_zeros_only(self):
        assert monotonic([0, 0, 0, 0]) is True

    def test_single_zero(self):
        assert monotonic([0]) is True

    def test_increasing_from_zero(self):
        assert monotonic([0, 1, 2, 3]) is True

    def test_decreasing_to_zero(self):
        assert monotonic([3, 2, 1, 0]) is True

    def test_max_int_values(self):
        assert monotonic([1, 2147483647]) is True

    def test_min_and_max(self):
        assert monotonic([-2147483648, 2147483647]) is True


# ---------------------------------------------------------------------------
# 8. Larger lists
# ---------------------------------------------------------------------------

class TestLargerLists:
    def test_sorted_ascending_100(self):
        lst = list(range(100))
        assert monotonic(lst) is True

    def test_sorted_descending_100(self):
        lst = list(range(99, -1, -1))
        assert monotonic(lst) is True

    def test_constant_100(self):
        assert monotonic([0] * 100) is True

    def test_one_disorder_in_ascending(self):
        lst = list(range(100))
        lst[50] = 0  # break monotonicity
        assert monotonic(lst) is False


# ---------------------------------------------------------------------------
# 9. Type / input shape expectations
# ---------------------------------------------------------------------------

class TestInputShape:
    def test_regular_list(self):
        assert monotonic([10, 20, 30]) is True

    def test_list_with_negative_numbers(self):
        assert monotonic([-10, -5, 0, 5, 10]) is True

    def test_list_with_negative_decreasing(self):
        assert monotonic([10, 5, 0, -5, -10]) is True
