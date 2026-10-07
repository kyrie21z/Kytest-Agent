import pytest
from solution import check_Consecutive


class TestCheckConsecutive:
    """Tests for the check_Consecutive function."""

    # --- Basic positive cases ---

    def test_already_sorted_consecutive(self):
        """List is already sorted and consecutive."""
        assert check_Consecutive([1, 2, 3, 4, 5]) is True

    def test_unsorted_consecutive(self):
        """List contains consecutive numbers but is not sorted."""
        assert check_Consecutive([3, 1, 4, 2, 5]) is True

    def test_two_elements_consecutive(self):
        """Two consecutive elements."""
        assert check_Consecutive([2, 3]) is True

    def test_single_element(self):
        """A single-element list is trivially consecutive."""
        assert check_Consecutive([7]) is True

    def test_negative_numbers(self):
        """List of negative consecutive numbers."""
        assert check_Consecutive([-3, -2, -1, 0, 1]) is True

    def test_mixed_positive_negative(self):
        """Consecutive numbers spanning negative and positive."""
        assert check_Consecutive([-2, -1, 0, 1, 2]) is True

    def test_large_range(self):
        """Larger range of consecutive numbers."""
        assert check_Consecutive(list(range(1, 101))) is True

    # --- Negative cases ---

    def test_missing_middle_number(self):
        """Consecutive except one number is missing in the middle."""
        assert check_Consecutive([1, 2, 4, 5]) is False

    def test_gaps_in_sequence(self):
        """Multiple gaps in the sequence."""
        assert check_Consecutive([1, 3, 5, 7]) is False

    def test_duplicate_values(self):
        """List contains duplicate values (not strictly consecutive)."""
        assert check_Consecutive([1, 2, 2, 3]) is False

    def test_all_same_values(self):
        """All elements are the same — duplicates break consecutiveness."""
        assert check_Consecutive([5, 5, 5]) is False

    def test_extra_element_beyond_range(self):
        """An extra number outside the expected consecutive range."""
        assert check_Consecutive([1, 2, 3, 5]) is False

    def test_reversed_order_not_consecutive(self):
        """Reversed list that isn't truly consecutive."""
        assert check_Consecutive([5, 3, 2, 1]) is False

    # --- Edge cases ---

    def test_empty_list(self):
        """Empty list should raise ValueError (min/max undefined)."""
        with pytest.raises(ValueError):
            check_Consecutive([])

    def test_two_identical_elements(self):
        """Two identical elements are duplicates, not consecutive."""
        assert check_Consecutive([4, 4]) is False

    def test_two_different_elements_not_consecutive(self):
        """Two different elements that are not consecutive."""
        assert check_Consecutive([1, 3]) is False

    def test_consecutive_with_duplicates_at_end(self):
        """Consecutive numbers with a trailing duplicate."""
        assert check_Consecutive([1, 2, 3, 3]) is False

    def test_consecutive_with_duplicates_at_start(self):
        """Consecutive numbers with a leading duplicate."""
        assert check_Consecutive([1, 1, 2, 3]) is False

    def test_negative_consecutive_with_gap(self):
        """Negative consecutive numbers with a gap."""
        assert check_Consecutive([-3, -1, 0, 1]) is False

    def test_unsorted_negative_consecutive(self):
        """Unsorted negative consecutive numbers."""
        assert check_Consecutive([0, -2, -1, -3]) is True

    def test_zero_in_sequence(self):
        """Sequence includes zero."""
        assert check_Consecutive([-1, 0, 1]) is True

    def test_large_consecutive_unsorted(self):
        """Large set of consecutive numbers in random order."""
        nums = list(range(-50, 50))
        import random
        random.seed(42)
        random.shuffle(nums)
        assert check_Consecutive(nums) is True
