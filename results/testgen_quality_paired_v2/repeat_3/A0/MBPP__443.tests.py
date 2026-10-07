import pytest
from solution import largest_neg


class TestLargestNeg:
    """Tests for the largest_neg function."""

    # --- Basic functionality: mixed positive and negative numbers ---

    def test_basic_mixed(self):
        """Find largest negative in a list with both positives and negatives."""
        assert largest_neg([1, -2, -3, 4]) == -2

    def test_single_negative(self):
        """List with one negative and rest positive."""
        assert largest_neg([5, 6, -1, 8]) == -1

    def test_multiple_negatives(self):
        """Multiple negatives; should return the one closest to zero."""
        assert largest_neg([-1, -2, -3, -4, 5]) == -1

    def test_largest_negative_not_first(self):
        """Largest negative appears later in the list."""
        assert largest_neg([10, -5, -1, -3]) == -1

    def test_largest_negative_at_end(self):
        """Largest negative is the last element."""
        assert largest_neg([1, 2, 3, -1]) == -1

    def test_largest_negative_at_start(self):
        """Largest negative is the first element."""
        assert largest_neg([-1, -5, -10]) == -1

    # --- All negatives ---

    def test_all_negatives(self):
        """All elements are negative; return the largest (closest to zero)."""
        assert largest_neg([-1, -2, -3]) == -1

    def test_all_negatives_unsorted(self):
        """All negatives in random order."""
        assert largest_neg([-5, -1, -3, -2, -4]) == -1

    # --- No negative numbers ---

    def test_no_negatives_raises(self):
        """List with no negative numbers should raise ValueError."""
        with pytest.raises(ValueError):
            largest_neg([1, 2, 3, 4])

    def test_empty_list_raises(self):
        """Empty list should raise ValueError."""
        with pytest.raises(ValueError):
            largest_neg([])

    # --- Edge cases with zeros ---

    def test_with_zero(self):
        """Zero is not negative; largest negative should still be found."""
        assert largest_neg([0, -1, -2, 3]) == -1

    def test_only_zero_and_positive(self):
        """Only zero and positives — no negatives exist."""
        with pytest.raises(ValueError):
            largest_neg([0, 1, 2])

    # --- Duplicate values ---

    def test_duplicate_negatives(self):
        """Duplicates of the largest negative."""
        assert largest_neg([-1, -1, -2, -3]) == -1

    def test_all_same_negative(self):
        """All elements are the same negative number."""
        assert largest_neg([-5, -5, -5]) == -5

    # --- Single element ---

    def test_single_negative_element(self):
        """List with exactly one negative number."""
        assert largest_neg([-7]) == -7

    def test_single_positive_element(self):
        """List with exactly one positive number — no negatives."""
        with pytest.raises(ValueError):
            largest_neg([7])

    # --- Large values ---

    def test_large_values(self):
        """Works with large magnitude numbers."""
        assert largest_neg([1000000, -1, -999999]) == -1

    def test_large_negative_values(self):
        """Works with very large negative numbers."""
        assert largest_neg([-1000000, -999999, -500000]) == -500000

    # --- Floats ---

    def test_float_negatives(self):
        """Works with floating-point negatives."""
        assert largest_neg([1.5, -0.5, -2.5, 3.0]) == -0.5

    def test_float_vs_int(self):
        """Mix of floats and ints."""
        assert largest_neg([1, -0.1, -2, 3.5]) == -0.1

    # --- Negative zero ---

    def test_negative_zero(self):
        """Negative zero is treated as zero (not negative)."""
        assert largest_neg([0, -0, -1, 2]) == -1

    # --- Unsorted / reverse sorted ---

    def test_reverse_sorted(self):
        """List sorted descending by value."""
        assert largest_neg([10, 5, -1, -5, -10]) == -1

    def test_ascending_sorted(self):
        """List sorted ascending by value."""
        assert largest_neg([-10, -5, -1, 5, 10]) == -1
