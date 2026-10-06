"""Unit tests for solution.get_positive."""

import pytest
from solution import get_positive


class TestGetPositive:
    """Tests for the get_positive function."""

    def test_basic_mixed_list(self):
        """Test with a mix of positive, negative, and zero values."""
        result = get_positive([-1, 2, -4, 5, 6])
        assert result == [2, 5, 6]

    def test_multiple_positives_and_negatives(self):
        """Test with multiple positives and negatives including zero."""
        result = get_positive([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10])
        assert result == [5, 3, 2, 3, 9, 123, 1]

    def test_all_positive_numbers(self):
        """Test when all numbers are positive."""
        result = get_positive([1, 2, 3, 4, 5])
        assert result == [1, 2, 3, 4, 5]

    def test_all_negative_numbers(self):
        """Test when all numbers are negative — should return empty list."""
        result = get_positive([-1, -2, -3, -4])
        assert result == []

    def test_empty_list(self):
        """Test with an empty list."""
        result = get_positive([])
        assert result == []

    def test_list_with_only_zero(self):
        """Test when the list contains only zero — zero is not positive."""
        result = get_positive([0, 0, 0])
        assert result == []

    def test_single_positive_number(self):
        """Test with a single positive number."""
        result = get_positive([42])
        assert result == [42]

    def test_single_negative_number(self):
        """Test with a single negative number."""
        result = get_positive([-7])
        assert result == []

    def test_single_zero(self):
        """Test with a single zero."""
        result = get_positive([0])
        assert result == []

    def test_duplicates_preserved(self):
        """Test that duplicate positive numbers are preserved in order."""
        result = get_positive([1, 2, 2, 3, 1, 4])
        assert result == [1, 2, 2, 3, 1, 4]

    def test_large_numbers(self):
        """Test with very large positive and negative numbers."""
        result = get_positive([-10**18, 10**18, -10**15, 10**15])
        assert result == [10**18, 10**15]

    def test_order_preserved(self):
        """Test that the original order of positive numbers is preserved."""
        result = get_positive([10, -1, 5, -2, 1, -3, 3])
        assert result == [10, 5, 1, 3]

    def test_alternating_signs(self):
        """Test with alternating positive and negative numbers."""
        result = get_positive([1, -1, 2, -2, 3, -3])
        assert result == [1, 2, 3]

    def test_no_negative_numbers(self):
        """Test with no negative numbers at all."""
        result = get_positive([0, 1, 2, 3])
        assert result == [1, 2, 3]

    def test_return_type_is_list(self):
        """Test that the return value is always a list."""
        assert isinstance(get_positive([]), list)
        assert isinstance(get_positive([1, -1]), list)
        assert isinstance(get_positive([-1, -2]), list)
