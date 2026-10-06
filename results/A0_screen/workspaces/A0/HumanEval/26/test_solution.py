import pytest
from solution import remove_duplicates


class TestRemoveDuplicates:
    """Unit tests for the remove_duplicates function."""

    def test_basic_example(self):
        """Test the example from the docstring."""
        assert remove_duplicates([1, 2, 3, 2, 4]) == [1, 3, 4]

    def test_empty_list(self):
        """An empty list should return an empty list."""
        assert remove_duplicates([]) == []

    def test_no_duplicates(self):
        """A list with no duplicates should return the same list."""
        assert remove_duplicates([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_all_duplicates(self):
        """A list where every element appears more than once should return empty."""
        assert remove_duplicates([1, 1, 2, 2, 3, 3]) == []

    def test_single_element(self):
        """A single-element list should return that element."""
        assert remove_duplicates([42]) == [42]

    def test_all_same_elements(self):
        """A list of identical elements should return empty."""
        assert remove_duplicates([5, 5, 5, 5]) == []

    def test_negative_numbers(self):
        """Negative numbers should be handled correctly."""
        assert remove_duplicates([-1, -2, -1, -3]) == [-2, -3]

    def test_mixed_positive_and_negative(self):
        """Mix of positive and negative numbers."""
        assert remove_duplicates([1, -1, 2, -1, 3, 2]) == [1, 3]

    def test_preserves_order(self):
        """The relative order of unique elements must be preserved."""
        result = remove_duplicates([5, 1, 2, 1, 3, 2, 4])
        assert result == [5, 3, 4]

    def test_duplicate_at_start(self):
        """Duplicates at the beginning of the list."""
        assert remove_duplicates([1, 1, 2, 3]) == [2, 3]

    def test_duplicate_at_end(self):
        """Duplicates at the end of the list."""
        assert remove_duplicates([1, 2, 3, 3]) == [1, 2]

    def test_multiple_occurrences(self):
        """Elements appearing more than twice should still be removed."""
        assert remove_duplicates([1, 2, 1, 2, 1]) == []

    def test_three_unique_with_duplicates(self):
        """Three unique values mixed with duplicates."""
        assert remove_duplicates([7, 8, 7, 9, 8, 10]) == [9, 10]

    def test_large_input(self):
        """Test with a larger input list."""
        numbers = list(range(100)) + list(range(50))
        expected = list(range(50, 100))
        assert remove_duplicates(numbers) == expected

    def test_zero_in_list(self):
        """Zero should be treated as a valid number."""
        assert remove_duplicates([0, 0, 1, 2, 1]) == [2]

    def test_zeros_only(self):
        """List containing only zeros."""
        assert remove_duplicates([0, 0, 0]) == []

    def test_alternating_pattern(self):
        """Alternating duplicate pattern."""
        assert remove_duplicates([1, 2, 1, 2, 3]) == [3]

    def test_first_and_last_unique(self):
        """First and last elements are unique, middle has duplicates."""
        assert remove_duplicates([1, 2, 2, 3, 3, 4]) == [1, 4]
