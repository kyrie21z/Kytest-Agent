"""Unit tests for solution.py using pytest."""

import pytest
from solution import unique


class TestUniqueBasic:
    """Tests for the basic functionality of unique()."""

    def test_example_from_docstring(self):
        """Test the example provided in the docstring."""
        assert unique([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [0, 2, 3, 5, 9, 123]

    def test_empty_list(self):
        """Test with an empty list."""
        assert unique([]) == []

    def test_single_element(self):
        """Test with a single-element list."""
        assert unique([42]) == [42]

    def test_all_same_elements(self):
        """Test when all elements are identical."""
        assert unique([7, 7, 7, 7]) == [7]

    def test_no_duplicates(self):
        """Test with a list that has no duplicate elements."""
        assert unique([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_two_elements_same(self):
        """Test with two identical elements."""
        assert unique([3, 3]) == [3]

    def test_two_elements_different(self):
        """Test with two different elements."""
        assert unique([3, 1]) == [1, 3]


class TestUniqueNegativeNumbers:
    """Tests involving negative numbers."""

    def test_negative_numbers(self):
        """Test with negative numbers."""
        assert unique([-5, -3, -5, -1, -3]) == [-5, -3, -1]

    def test_mixed_positive_and_negative(self):
        """Test with a mix of positive and negative numbers."""
        assert unique([-2, 3, -2, 0, 3, 1]) == [-2, 0, 1, 3]

    def test_only_negatives(self):
        """Test with only negative numbers."""
        assert unique([-10, -20, -10, -5]) == [-20, -10, -5]


class TestUniqueFloats:
    """Tests involving floating-point numbers."""

    def test_float_values(self):
        """Test with float values."""
        assert unique([1.5, 2.5, 1.5, 3.5]) == [1.5, 2.5, 3.5]

    def test_mixed_int_and_float(self):
        """Test with a mix of integers and floats."""
        assert unique([1, 1.0, 2, 2.5]) == [1, 2, 2.5]

    def test_negative_floats(self):
        """Test with negative float values."""
        assert unique([-1.5, -2.5, -1.5]) == [-2.5, -1.5]


class TestUniqueEdgeCases:
    """Tests for edge cases."""

    def test_large_list_with_duplicates(self):
        """Test with a larger list containing many duplicates."""
        data = [1] * 100 + [2] * 50 + [3] * 25
        assert unique(data) == [1, 2, 3]

    def test_already_sorted(self):
        """Test with an already sorted list."""
        assert unique([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        """Test with a reverse-sorted list."""
        assert unique([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_random_order(self):
        """Test with elements in random order."""
        assert unique([9, 1, 5, 3, 7, 2, 8, 4, 6]) == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_zeros(self):
        """Test with zero values."""
        assert unique([0, 0, 0, 1, -1]) == [-1, 0, 1]

    def test_large_numbers(self):
        """Test with large integer values."""
        assert unique([10**9, 10**8, 10**9, 10**7]) == [10**7, 10**8, 10**9]


class TestUniqueReturnProperties:
    """Tests to verify return value properties."""

    def test_return_is_sorted(self):
        """Verify that the returned list is always sorted."""
        result = unique([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        assert result == sorted(result)

    def test_return_has_no_duplicates(self):
        """Verify that the returned list has no duplicate elements."""
        result = unique([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
        assert len(result) == len(set(result))

    def test_return_preserves_all_unique_values(self):
        """Verify that all unique values from input are present in output."""
        original = [5, 3, 5, 2, 3, 3, 9, 0, 123]
        result = unique(original)
        assert set(result) == set(original)
