import pytest
from solution import filter_oddnumbers


class TestFilterOddnumbers:
    """Tests for the filter_oddnumbers function."""

    def test_basic_mixed_list(self):
        """Test filtering odd numbers from a mixed list."""
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = filter_oddnumbers(nums)
        assert result == [1, 3, 5, 7, 9]

    def test_empty_list(self):
        """Test with an empty list returns an empty list."""
        assert filter_oddnumbers([]) == []

    def test_all_even_numbers(self):
        """Test with only even numbers returns an empty list."""
        nums = [2, 4, 6, 8, 10]
        assert filter_oddnumbers(nums) == []

    def test_all_odd_numbers(self):
        """Test with only odd numbers returns the same list."""
        nums = [1, 3, 5, 7, 9]
        assert filter_oddnumbers(nums) == [1, 3, 5, 7, 9]

    def test_single_odd_number(self):
        """Test with a single odd number."""
        assert filter_oddnumbers([3]) == [3]

    def test_single_even_number(self):
        """Test with a single even number."""
        assert filter_oddnumbers([4]) == []

    def test_negative_numbers(self):
        """Test with negative numbers (odd negatives should be included)."""
        nums = [-3, -2, -1, 0, 1, 2, 3]
        result = filter_oddnumbers(nums)
        assert result == [-3, -1, 1, 3]

    def test_zero_included_as_even(self):
        """Test that zero is treated as even and excluded."""
        nums = [0, 1, 2]
        assert filter_oddnumbers(nums) == [1]

    def test_duplicate_values(self):
        """Test with duplicate values in the list."""
        nums = [1, 1, 2, 3, 3, 5]
        result = filter_oddnumbers(nums)
        assert result == [1, 1, 3, 3, 5]

    def test_large_list(self):
        """Test with a larger list of numbers."""
        nums = list(range(1, 101))
        result = filter_oddnumbers(nums)
        expected = list(range(1, 101, 2))
        assert result == expected

    def test_returns_a_list(self):
        """Test that the return type is a list."""
        result = filter_oddnumbers([1, 2, 3])
        assert isinstance(result, list)

    def test_does_not_modify_original(self):
        """Test that the original list is not modified."""
        nums = [1, 2, 3, 4, 5]
        original = nums.copy()
        filter_oddnumbers(nums)
        assert nums == original

    def test_preserves_order(self):
        """Test that the order of odd numbers is preserved."""
        nums = [10, 7, 4, 3, 8, 1, 6, 5]
        result = filter_oddnumbers(nums)
        assert result == [7, 3, 1, 5]

    def test_only_zeros(self):
        """Test with a list containing only zeros."""
        assert filter_oddnumbers([0, 0, 0]) == []

    def test_two_element_list_both_odd(self):
        """Test with two odd numbers."""
        assert filter_oddnumbers([3, 5]) == [3, 5]

    def test_two_element_list_one_each(self):
        """Test with one odd and one even number."""
        assert filter_oddnumbers([2, 3]) == [3]
