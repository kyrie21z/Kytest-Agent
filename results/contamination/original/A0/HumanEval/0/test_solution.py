import pytest
from solution import has_close_elements


class TestHasCloseElements:
    """Tests for the has_close_elements function."""

    # --- Basic positive/negative cases ---

    def test_no_close_elements(self):
        """No pair is closer than threshold."""
        assert has_close_elements([1.0, 2.0, 3.0], 0.5) is False

    def test_has_close_elements(self):
        """At least one pair is closer than threshold."""
        assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) is True

    def test_close_pair_at_end(self):
        """Close pair appears near the end of the sorted list."""
        assert has_close_elements([1.0, 5.0, 9.0, 9.1], 0.5) is True

    def test_close_pair_at_start(self):
        """Close pair appears near the beginning of the sorted list."""
        assert has_close_elements([10.0, 10.2, 5.0, 1.0], 0.5) is True

    # --- Edge cases with small lists ---

    def test_empty_list(self):
        """Empty list should return False (no pairs exist)."""
        assert has_close_elements([], 0.5) is False

    def test_single_element(self):
        """Single-element list should return False (no pairs exist)."""
        assert has_close_elements([1.0], 0.5) is False

    def test_two_elements_not_close(self):
        """Two elements farther apart than threshold."""
        assert has_close_elements([1.0, 5.0], 0.5) is False

    def test_two_elements_close(self):
        """Two elements closer than threshold."""
        assert has_close_elements([1.0, 1.2], 0.5) is True

    def test_two_elements_equal(self):
        """Two identical elements (distance = 0 < any positive threshold)."""
        assert has_close_elements([3.0, 3.0], 0.5) is True

    # --- Boundary / exact threshold ---

    def test_distance_exactly_threshold(self):
        """Distance equals threshold — should NOT trigger (strictly less than)."""
        assert has_close_elements([1.0, 2.0], 1.0) is False

    def test_distance_just_below_threshold(self):
        """Distance just below threshold — should trigger."""
        assert has_close_elements([1.0, 1.99], 1.0) is True

    def test_distance_just_above_threshold(self):
        """Distance just above threshold — should not trigger."""
        assert has_close_elements([1.0, 2.01], 1.0) is False

    # --- Zero threshold ---

    def test_zero_threshold_with_distinct_values(self):
        """With threshold=0, distinct values means no pair is closer (0 is not < 0)."""
        assert has_close_elements([1.0, 2.0, 3.0], 0.0) is False

    def test_zero_threshold_with_identical_values(self):
        """With threshold=0, identical values have distance 0 which is not < 0."""
        assert has_close_elements([1.0, 2.0, 1.0], 0.0) is False

    # --- Negative threshold ---

    def test_negative_threshold(self):
        """Negative threshold: no pair can be closer than a negative number."""
        assert has_close_elements([1.0, 2.0, 3.0], -0.5) is False

    def test_negative_threshold_with_identical_values(self):
        """Even identical values have distance 0, which is > negative threshold."""
        assert has_close_elements([5.0, 5.0], -1.0) is False

    # --- All same elements ---

    def test_all_same_elements(self):
        """All elements identical; every pair has distance 0."""
        assert has_close_elements([2.0, 2.0, 2.0, 2.0], 0.5) is True

    def test_all_same_elements_zero_threshold(self):
        """All same elements with zero threshold — distance 0 is not < 0."""
        assert has_close_elements([2.0, 2.0, 2.0], 0.0) is False

    # --- Larger lists ---

    def test_large_list_with_close_pair(self):
        """Large list where a close pair exists somewhere in the middle."""
        numbers = [i * 10.0 for i in range(100)]
        numbers[50] = numbers[49] + 0.1  # Insert a close pair
        assert has_close_elements(numbers, 1.0) is True

    def test_large_list_no_close_pair(self):
        """Large list with uniformly spaced elements."""
        numbers = [i * 10.0 for i in range(100)]
        assert has_close_elements(numbers, 1.0) is False

    # --- Unsorted input ---

    def test_unsorted_input(self):
        """Function should handle unsorted input correctly."""
        assert has_close_elements([5.0, 1.0, 3.0, 2.0, 2.1], 0.5) is True

    def test_reverse_sorted_input(self):
        """Reverse-sorted input."""
        assert has_close_elements([5.0, 4.0, 3.0, 2.0, 1.0], 0.5) is False

    def test_random_order(self):
        """Random order input."""
        assert has_close_elements([10.0, 1.0, 8.0, 2.0, 9.0, 9.5], 1.0) is True

    # --- Mixed positive and negative numbers ---

    def test_mixed_positive_negative(self):
        """List with both positive and negative numbers, no pair within threshold."""
        assert has_close_elements([-1.0, -0.5, 0.0, 0.5, 1.0], 0.6) is True

    def test_mixed_positive_negative_no_close(self):
        """Mixed numbers but no pair within threshold."""
        assert has_close_elements([-10.0, 0.0, 10.0], 5.0) is False

    def test_mixed_positive_negative_adjacent(self):
        """Adjacent values in mixed list are close enough."""
        assert has_close_elements([-1.0, -0.9, 0.0, 0.5, 1.0], 0.2) is True

    # --- Floating-point precision ---

    def test_small_floats(self):
        """Very small floating-point numbers with gap larger than threshold."""
        assert has_close_elements([1e-10, 3e-10, 5e-10], 1e-10) is False

    def test_small_floats_close(self):
        """Very small floating-point numbers that are close."""
        assert has_close_elements([1e-10, 1.5e-10, 3e-10], 1e-10) is True

    def test_large_floats(self):
        """Large floating-point numbers with gap smaller than threshold."""
        assert has_close_elements([1e10, 1e10 + 50, 2e10], 100.0) is True

    def test_large_floats_far_apart(self):
        """Large floating-point numbers far apart relative to threshold."""
        assert has_close_elements([1e10, 1e10 + 200, 2e10], 100.0) is False
