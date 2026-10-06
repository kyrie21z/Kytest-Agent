import pytest
from solution import largest_smallest_integers


class TestLargestSmallestIntegers:
    """Unit tests for the largest_smallest_integers function."""

    # --- Examples from docstring ---

    def test_all_positive(self):
        """All positive integers: largest negative is None, smallest positive is 1."""
        assert largest_smallest_integers([2, 4, 1, 3, 5, 7]) == (None, 1)

    def test_empty_list(self):
        """Empty list: both values are None."""
        assert largest_smallest_integers([]) == (None, None)

    def test_single_zero(self):
        """List with only zero: both values are None."""
        assert largest_smallest_integers([0]) == (None, None)

    # --- All positive integers ---

    def test_all_positive_single_element(self):
        """Single positive integer."""
        assert largest_smallest_integers([42]) == (None, 42)

    def test_all_positive_unordered(self):
        """Positive integers in random order."""
        assert largest_smallest_integers([10, 3, 7, 1, 5]) == (None, 1)

    def test_all_positive_duplicates(self):
        """Positive integers with duplicates."""
        assert largest_smallest_integers([5, 3, 3, 1, 1, 2]) == (None, 1)

    # --- All negative integers ---

    def test_all_negative_single_element(self):
        """Single negative integer."""
        assert largest_smallest_integers([-42]) == (-42, None)

    def test_all_negative_unordered(self):
        """Negative integers in random order."""
        assert largest_smallest_integers([-10, -3, -7, -1, -5]) == (-1, None)

    def test_all_negative_duplicates(self):
        """Negative integers with duplicates."""
        assert largest_smallest_integers([-5, -3, -3, -1, -1, -2]) == (-1, None)

    # --- Mixed positive and negative ---

    def test_mixed_basic(self):
        """Basic mix of positive and negative integers."""
        assert largest_smallest_integers([-1, 1]) == (-1, 1)

    def test_mixed_multiple(self):
        """Multiple positive and negative integers."""
        assert largest_smallest_integers([-5, -2, 3, 7]) == (-2, 3)

    def test_mixed_unordered(self):
        """Mixed integers in random order."""
        assert largest_smallest_integers([10, -3, 0, -1, 5, -7]) == (-1, 5)

    def test_mixed_with_larger_range(self):
        """Wide range of positive and negative values."""
        assert largest_smallest_integers([-100, -50, 1, 200]) == (-50, 1)

    # --- Zero handling ---

    def test_only_zeros(self):
        """List containing only zeros."""
        assert largest_smallest_integers([0, 0, 0]) == (None, None)

    def test_zeros_with_negatives(self):
        """Zeros mixed with negative integers."""
        assert largest_smallest_integers([-5, 0, -1, 0]) == (-1, None)

    def test_zeros_with_positives(self):
        """Zeros mixed with positive integers."""
        assert largest_smallest_integers([5, 0, 1, 0]) == (None, 1)

    def test_zeros_with_both(self):
        """Zeros mixed with both positive and negative integers."""
        assert largest_smallest_integers([-3, 0, 2, 0, -1]) == (-1, 2)

    # --- Edge cases ---

    def test_single_negative(self):
        """List with a single negative integer."""
        assert largest_smallest_integers([-7]) == (-7, None)

    def test_single_positive(self):
        """List with a single positive integer."""
        assert largest_smallest_integers([7]) == (None, 7)

    def test_two_elements_different_signs(self):
        """Two elements with different signs."""
        assert largest_smallest_integers([-10, 10]) == (-10, 10)

    def test_two_elements_same_sign_positive(self):
        """Two positive elements."""
        assert largest_smallest_integers([3, 7]) == (None, 3)

    def test_two_elements_same_sign_negative(self):
        """Two negative elements."""
        assert largest_smallest_integers([-3, -7]) == (-3, None)

    # --- Large numbers ---

    def test_large_values(self):
        """Large positive and negative integers."""
        assert largest_smallest_integers([-10**9, 10**9]) == (-10**9, 10**9)

    def test_many_large_values(self):
        """Many large values with correct extremes identified."""
        lst = [-1000, -500, -1, 1, 500, 1000]
        assert largest_smallest_integers(lst) == (-1, 1)

    # --- Return type checks ---

    def test_return_type_tuple(self):
        """Ensure the return value is always a tuple."""
        result = largest_smallest_integers([1, -1])
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_return_type_all_none(self):
        """Return type when all values are None."""
        result = largest_smallest_integers([])
        assert isinstance(result, tuple)
        assert result[0] is None
        assert result[1] is None

    def test_return_type_mixed(self):
        """Return type when one value is an int and the other is None."""
        result = largest_smallest_integers([1, 2, 3])
        assert isinstance(result, tuple)
        assert result[0] is None
        assert isinstance(result[1], int)

    # --- Additional boundary cases ---

    def test_negative_one_and_positive_one(self):
        """Edge case with -1 and 1."""
        assert largest_smallest_integers([-1, 1]) == (-1, 1)

    def test_consecutive_negatives(self):
        """Consecutive negative integers."""
        assert largest_smallest_integers([-5, -4, -3, -2, -1]) == (-1, None)

    def test_consecutive_positives(self):
        """Consecutive positive integers."""
        assert largest_smallest_integers([1, 2, 3, 4, 5]) == (None, 1)

    def test_wide_mixed_range(self):
        """Wide range of values including many negatives and positives."""
        lst = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1,
               1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        assert largest_smallest_integers(lst) == (-1, 1)
