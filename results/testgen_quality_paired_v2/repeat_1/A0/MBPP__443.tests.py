import pytest
from solution import largest_neg


class TestLargestNeg:
    """Tests for the largest_neg function."""

    # --- Basic functionality: lists with negative numbers ---

    def test_single_negative(self):
        """A list with one negative number returns that number."""
        assert largest_neg([-5]) == -5

    def test_two_negatives(self):
        """With two negatives, returns the smallest (most negative)."""
        assert largest_neg([-3, -7]) == -7

    def test_multiple_negatives(self):
        """With multiple negatives, returns the smallest."""
        assert largest_neg([-1, -5, -3, -10, -2]) == -10

    def test_all_same_negative(self):
        """All identical negatives should return that value."""
        assert largest_neg([-4, -4, -4]) == -4

    # --- Mixed positive and negative numbers ---

    def test_mixed_positive_and_negative(self):
        """Returns the smallest number among positives and negatives."""
        assert largest_neg([1, -3, 4, -2, 5]) == -3

    def test_largest_negative_but_smallest_overall(self):
        """When the largest negative is also the smallest overall."""
        assert largest_neg([10, 20, -1]) == -1

    def test_negative_is_not_the_largest_negative(self):
        """Even if there are larger negatives, returns the smallest."""
        assert largest_neg([5, -1, -2, -3]) == -3

    # --- All positive numbers ---

    def test_all_positives(self):
        """With all positives, returns the smallest positive."""
        assert largest_neg([1, 2, 3, 4, 5]) == 1

    def test_single_positive(self):
        """Single positive number returns itself."""
        assert largest_neg([42]) == 42

    # --- Zero handling ---

    def test_with_zero_and_negatives(self):
        """Zero is greater than negatives; returns smallest negative."""
        assert largest_neg([0, -1, -2]) == -2

    def test_with_zero_and_positives(self):
        """Zero is the smallest when mixed with positives."""
        assert largest_neg([0, 1, 2]) == 0

    def test_only_zeros(self):
        """List of only zeros returns zero."""
        assert largest_neg([0, 0, 0]) == 0

    # --- Edge cases ---

    def test_empty_list_raises_error(self):
        """An empty list should raise an IndexError."""
        with pytest.raises(IndexError):
            largest_neg([])

    def test_large_list(self):
        """Works correctly with a large list."""
        nums = list(range(-1000, 1000))
        assert largest_neg(nums) == -1000

    def test_duplicates_in_list(self):
        """Duplicates do not affect correctness."""
        assert largest_neg([3, -1, 3, -1, 2, -1]) == -1

    def test_negative_at_start(self):
        """Negative number at the start of the list."""
        assert largest_neg([-9, 1, 2, 3]) == -9

    def test_negative_at_end(self):
        """Negative number at the end of the list."""
        assert largest_neg([1, 2, 3, -9]) == -9

    def test_negative_in_middle(self):
        """Negative number in the middle of the list."""
        assert largest_neg([1, -9, 3]) == -9

    # --- Parameter validation ---

    def test_none_input_raises_error(self):
        """Passing None should raise an error."""
        with pytest.raises(TypeError):
            largest_neg(None)

    def test_non_list_iterable(self):
        """Tuples work similarly since they support indexing and iteration."""
        assert largest_neg((-5, -2, -8)) == -8
