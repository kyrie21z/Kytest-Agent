import pytest
from solution import comb_sort


class TestCombSort:
    """Tests for the comb_sort function."""

    def test_basic_unsorted(self):
        """Test sorting a basic unsorted list."""
        nums = [5, 3, 1, 4, 2]
        expected = [1, 2, 3, 4, 5]
        assert comb_sort(nums) == expected

    def test_already_sorted(self):
        """Test when the list is already sorted."""
        nums = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        assert comb_sort(nums) == expected

    def test_empty_list(self):
        """Test sorting an empty list."""
        nums = []
        expected = []
        assert comb_sort(nums) == expected

    def test_single_element(self):
        """Test sorting a single-element list."""
        nums = [42]
        expected = [42]
        assert comb_sort(nums) == expected

    def test_two_elements_unsorted(self):
        """Test sorting two elements out of order."""
        nums = [2, 1]
        expected = [1, 2]
        assert comb_sort(nums) == expected

    def test_two_elements_sorted(self):
        """Test sorting two elements already in order."""
        nums = [1, 2]
        expected = [1, 2]
        assert comb_sort(nums) == expected

    def test_duplicates(self):
        """Test sorting a list with duplicate values."""
        nums = [3, 1, 2, 3, 1, 2]
        expected = [1, 1, 2, 2, 3, 3]
        assert comb_sort(nums) == expected

    def test_all_same_elements(self):
        """Test sorting a list where all elements are identical."""
        nums = [5, 5, 5, 5, 5]
        expected = [5, 5, 5, 5, 5]
        assert comb_sort(nums) == expected

    def test_negative_numbers(self):
        """Test sorting a list with negative numbers."""
        nums = [-3, -1, -4, -1, -5, -2]
        expected = [-5, -4, -3, -2, -1, -1]
        assert comb_sort(nums) == expected

    def test_mixed_positive_and_negative(self):
        """Test sorting a list with both positive and negative numbers."""
        nums = [3, -1, 0, 5, -2, 4, -3]
        expected = [-3, -2, -1, 0, 3, 4, 5]
        assert comb_sort(nums) == expected

    def test_large_list(self):
        """Test sorting a larger list."""
        import random
        nums = list(range(100))
        random.shuffle(nums)
        original = nums[:]
        expected = sorted(original)
        assert comb_sort(nums) == expected

    def test_returns_sorted_reference(self):
        """Test that the returned value is the same object as the input (in-place)."""
        nums = [5, 3, 1]
        result = comb_sort(nums)
        assert result is nums

    def test_modifies_in_place(self):
        """Test that the original list is modified in place."""
        nums = [5, 3, 1]
        comb_sort(nums)
        assert nums == [1, 3, 5]

    def test_float_values(self):
        """Test sorting a list with float values."""
        nums = [3.14, 1.59, 2.65, 3.58, 2.71]
        expected = [1.59, 2.65, 2.71, 3.14, 3.58]
        assert comb_sort(nums) == expected

    def test_reverse_sorted(self):
        """Test sorting a list that is reverse sorted."""
        nums = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        assert comb_sort(nums) == expected

    def test_one_duplicate_pair(self):
        """Test with just two equal elements among distinct ones."""
        nums = [1, 3, 2, 3]
        expected = [1, 2, 3, 3]
        assert comb_sort(nums) == expected
