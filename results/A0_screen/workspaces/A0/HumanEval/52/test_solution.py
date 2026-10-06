import pytest
from solution import below_threshold


class TestBelowThreshold:
    """Tests for the below_threshold function."""

    # --- Basic positive cases (all elements below threshold) ---

    def test_all_below_basic(self):
        """All numbers strictly below threshold should return True."""
        assert below_threshold([1, 2, 4, 10], 100) is True

    def test_single_element_below(self):
        """A single element below threshold should return True."""
        assert below_threshold([3], 5) is True

    def test_empty_list(self):
        """An empty list should return True (vacuous truth)."""
        assert below_threshold([], 10) is True

    def test_negative_numbers_below(self):
        """Negative numbers below threshold should return True."""
        assert below_threshold([-5, -3, -1], 0) is True

    def test_mixed_positive_negative_below(self):
        """Mixed positive and negative numbers all below threshold."""
        assert below_threshold([-10, 0, 5], 10) is True

    def test_large_values_below(self):
        """Large values all below threshold."""
        assert below_threshold([10**9, 10**9 - 1], 10**9 + 1) is True

    # --- Basic negative cases (at least one element at or above threshold) ---

    def test_one_above_threshold(self):
        """One number at or above threshold should return False."""
        assert below_threshold([1, 20, 4, 10], 5) is False

    def test_one_at_threshold(self):
        """One number equal to threshold should return False."""
        assert below_threshold([1, 5, 4, 10], 5) is False

    def test_all_above_threshold(self):
        """All numbers above threshold should return False."""
        assert below_threshold([10, 20, 30], 5) is False

    def test_single_element_at_threshold(self):
        """Single element equal to threshold should return False."""
        assert below_threshold([5], 5) is False

    def test_single_element_above_threshold(self):
        """Single element above threshold should return False."""
        assert below_threshold([10], 5) is False

    # --- Edge cases ---

    def test_zero_threshold(self):
        """Threshold of zero with positive numbers."""
        assert below_threshold([1, 2, 3], 0) is False

    def test_zero_threshold_with_negatives(self):
        """Threshold of zero with negative numbers."""
        assert below_threshold([-1, -2, -3], 0) is True

    def test_zero_in_list(self):
        """List containing zero."""
        assert below_threshold([0, 1, 2], 3) is True
        assert below_threshold([0, 1, 2], 1) is False

    def test_duplicates_below(self):
        """List with duplicate values all below threshold."""
        assert below_threshold([3, 3, 3, 3], 5) is True

    def test_duplicates_at_threshold(self):
        """List with duplicate values at threshold."""
        assert below_threshold([5, 5, 5], 5) is False

    def test_large_list_all_below(self):
        """Large list with all elements below threshold."""
        large_list = list(range(1000))
        assert below_threshold(large_list, 1001) is True

    def test_large_list_some_above(self):
        """Large list with some elements above threshold."""
        large_list = list(range(1000))
        assert below_threshold(large_list, 500) is False

    def test_float_like_integers(self):
        """Test with integer-like values."""
        assert below_threshold([0, 1, 2, 3, 4], 5) is True

    # --- Boundary conditions ---

    def test_threshold_one(self):
        """Threshold of 1."""
        assert below_threshold([0], 1) is True
        assert below_threshold([1], 1) is False

    def test_two_elements_boundary(self):
        """Two elements, one just below and one at threshold."""
        assert below_threshold([4, 5], 5) is False
        assert below_threshold([4, 4], 5) is True
