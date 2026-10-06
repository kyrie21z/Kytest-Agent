import pytest
from solution import has_close_elements


class TestHasCloseElements:
    """Tests for the has_close_elements function."""

    # --- Basic positive/negative cases from docstring ---

    def test_no_close_elements_basic(self):
        """Example from docstring: no pair within 0.5."""
        assert has_close_elements([1.0, 2.0, 3.0], 0.5) is False

    def test_has_close_elements_basic(self):
        """Example from docstring: some pair within 0.3."""
        assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) is True

    # --- Edge cases: empty and small lists ---

    def test_empty_list(self):
        """An empty list has no pairs, so should return False."""
        assert has_close_elements([], 0.5) is False

    def test_single_element(self):
        """A single-element list has no pairs, so should return False."""
        assert has_close_elements([1.0], 0.5) is False

    def test_two_elements_not_close(self):
        """Two elements farther apart than threshold."""
        assert has_close_elements([1.0, 5.0], 0.5) is False

    def test_two_elements_close(self):
        """Two elements closer than threshold."""
        assert has_close_elements([1.0, 1.2], 0.5) is True

    # --- Boundary: exactly at threshold ---

    def test_exactly_at_threshold(self):
        """Difference equal to threshold should NOT trigger (strictly less)."""
        assert has_close_elements([1.0, 2.0], 1.0) is False

    def test_just_below_threshold(self):
        """Difference just below threshold should trigger."""
        assert has_close_elements([1.0, 1.99], 1.0) is True

    def test_just_above_threshold(self):
        """Difference just above threshold should not trigger."""
        assert has_close_elements([1.0, 2.01], 1.0) is False

    # --- Zero and negative thresholds ---

    def test_zero_threshold(self):
        """With threshold 0, only identical values count as 'close'."""
        assert has_close_elements([1.0, 2.0, 3.0], 0.0) is False

    def test_zero_threshold_with_duplicates(self):
        """With threshold 0, duplicate values should return True."""
        assert has_close_elements([1.0, 2.0, 2.0, 3.0], 0.0) is True

    def test_negative_threshold(self):
        """Negative threshold means every pair qualifies (difference >= 0 > neg)."""
        assert has_close_elements([1.0, 2.0], -0.1) is True

    def test_negative_threshold_empty(self):
        """Negative threshold with empty list still returns False."""
        assert has_close_elements([], -0.1) is False

    # --- Duplicate / all-same values ---

    def test_all_same_values(self):
        """All identical values with any positive threshold."""
        assert has_close_elements([5.0, 5.0, 5.0], 1.0) is True

    def test_all_same_values_zero_threshold(self):
        """All identical values with zero threshold."""
        assert has_close_elements([5.0, 5.0, 5.0], 0.0) is True

    # --- Negative numbers ---

    def test_negative_numbers_close(self):
        """Negative numbers that are close together."""
        assert has_close_elements([-1.0, -0.5, 0.0], 0.3) is True

    def test_negative_numbers_not_close(self):
        """Negative numbers far apart."""
        assert has_close_elements([-5.0, -1.0, 0.0], 0.3) is False

    def test_mixed_positive_negative(self):
        """Mix of positive and negative numbers."""
        assert has_close_elements([-1.0, 0.0, 1.0], 0.5) is True

    # --- Unsorted input ---

    def test_unsorted_input_close(self):
        """Unsorted list with close elements."""
        assert has_close_elements([5.0, 1.0, 3.0, 2.0], 0.5) is True

    def test_unsorted_input_not_close(self):
        """Unsorted list without close elements."""
        assert has_close_elements([5.0, 1.0, 3.0, 7.0], 0.5) is False

    # --- Larger lists ---

    def test_large_list_no_close(self):
        """Large evenly-spaced list with tight threshold."""
        numbers = [i * 1.0 for i in range(100)]
        assert has_close_elements(numbers, 0.5) is False

    def test_large_list_has_close(self):
        """Large list with one close pair."""
        numbers = [i * 1.0 for i in range(100)]
        numbers[5] = 5.1  # Make 5.0 and 5.1 close
        assert has_close_elements(numbers, 0.5) is True

    # --- Float precision edge cases ---

    def test_very_small_difference(self):
        """Very small differences with appropriate threshold."""
        assert has_close_elements([1.0, 1.0 + 1e-10], 1e-9) is True

    def test_very_small_difference_below_threshold(self):
        """Very small difference but threshold even smaller."""
        assert has_close_elements([1.0, 1.0 + 1e-10], 1e-11) is False

    # --- Multiple close pairs ---

    def test_multiple_close_pairs(self):
        """List with several close pairs."""
        assert has_close_elements([1.0, 1.1, 2.0, 2.1, 3.0, 3.1], 0.2) is True

    # --- Integer-like floats ---

    def test_integer_like_floats(self):
        """Integer-like float values."""
        assert has_close_elements([1, 2, 3], 0.5) is False
        assert has_close_elements([1, 2, 2, 3], 0.5) is True
