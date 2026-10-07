import pytest
from solution import pancake_sort


class TestPancakeSort:
    """Tests for the pancake_sort function."""

    def test_empty_list(self):
        assert pancake_sort([]) == []

    def test_single_element(self):
        assert pancake_sort([1]) == [1]

    def test_two_elements_already_sorted(self):
        assert pancake_sort([1, 2]) == [1, 2]

    def test_two_elements_unsorted(self):
        assert pancake_sort([2, 1]) == [1, 2]

    def test_already_sorted(self):
        assert pancake_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert pancake_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_random_order(self):
        assert pancake_sort([3, 1, 2]) == [1, 2, 3]

    def test_with_duplicates(self):
        assert pancake_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]

    def test_negative_numbers(self):
        assert pancake_sort([-3, -1, -4, -1, -5]) == [-5, -4, -3, -1, -1]

    def test_mixed_positive_and_negative(self):
        assert pancake_sort([3, -1, 2, -5, 0]) == [-5, -1, 0, 2, 3]

    def test_all_same_elements(self):
        assert pancake_sort([7, 7, 7, 7]) == [7, 7, 7, 7]

    def test_larger_list(self):
        nums = [64, 25, 12, 22, 11, 90, 50, 30, 40, 80]
        result = pancake_sort(nums)
        assert result == sorted(nums)

    def test_returns_sorted_list(self):
        nums = [5, 3, 8, 1, 2, 7, 4, 6]
        result = pancake_sort(nums)
        assert result == sorted(nums)

    def test_preserves_count(self):
        nums = [3, 1, 4, 1, 5, 9, 2, 6]
        result = pancake_sort(nums)
        assert len(result) == len(nums)

    def test_preserves_elements(self):
        nums = [3, 1, 4, 1, 5, 9, 2, 6]
        result = pancake_sort(nums)
        assert sorted(result) == sorted(nums)
