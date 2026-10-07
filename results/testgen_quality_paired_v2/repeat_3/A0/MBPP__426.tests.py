import pytest
from solution import filter_oddnumbers


class TestFilterOddNumbers:
    """Tests for the filter_oddnumbers function."""

    def test_empty_list(self):
        """Test with an empty list."""
        assert filter_oddnumbers([]) == []

    def test_no_odd_numbers(self):
        """Test with a list containing only even numbers."""
        assert filter_oddnumbers([2, 4, 6, 8]) == []

    def test_all_odd_numbers(self):
        """Test with a list containing only odd numbers."""
        assert filter_oddnumbers([1, 3, 5, 7]) == [1, 3, 5, 7]

    def test_mixed_numbers(self):
        """Test with a mix of odd and even numbers."""
        assert filter_oddnumbers([1, 2, 3, 4, 5]) == [1, 3, 5]

    def test_single_odd_number(self):
        """Test with a single odd number."""
        assert filter_oddnumbers([3]) == [3]

    def test_single_even_number(self):
        """Test with a single even number."""
        assert filter_oddnumbers([4]) == []

    def test_negative_numbers(self):
        """Test with negative odd and even numbers."""
        assert filter_oddnumbers([-3, -2, -1, 0, 1, 2, 3]) == [-3, -1, 1, 3]

    def test_preserves_order(self):
        """Test that the original order of odd numbers is preserved."""
        assert filter_oddnumbers([10, 7, 4, 3, 8, 1]) == [7, 3, 1]

    def test_with_zero(self):
        """Test that zero (even) is correctly excluded."""
        assert filter_oddnumbers([0, 1, 2, 3]) == [1, 3]

    def test_large_list(self):
        """Test with a larger list of numbers."""
        nums = list(range(1, 21))
        expected = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        assert filter_oddnumbers(nums) == expected

    def test_returns_new_list(self):
        """Test that the function returns a new list, not a reference to the input."""
        original = [1, 2, 3, 4]
        result = filter_oddnumbers(original)
        assert result == [1, 3]
        # Modify the result and ensure the original is unaffected
        result.append(5)
        assert original == [1, 2, 3, 4]
