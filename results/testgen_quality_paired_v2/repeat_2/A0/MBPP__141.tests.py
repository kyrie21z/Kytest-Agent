import pytest
from solution import pancake_sort


class TestPancakeSort:
    """Tests for the pancake_sort function."""

    def test_empty_list(self):
        assert pancake_sort([]) == []

    def test_single_element(self):
        assert pancake_sort([1]) == [1]

    def test_two_elements_unsorted(self):
        assert pancake_sort([2, 1]) == [1, 2]

    def test_two_elements_sorted(self):
        assert pancake_sort([1, 2]) == [1, 2]

    def test_already_sorted(self):
        assert pancake_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert pancake_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_unordered_list(self):
        assert pancake_sort([3, 1, 2, 5, 4]) == [1, 2, 3, 4, 5]

    def test_with_duplicates(self):
        assert pancake_sort([3, 1, 2, 1, 3]) == [1, 1, 2, 3, 3]

    def test_all_same_elements(self):
        assert pancake_sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    def test_negative_numbers(self):
        assert pancake_sort([-3, -1, -2, 0, 1]) == [-3, -2, -1, 0, 1]

    def test_mixed_positive_negative(self):
        assert pancake_sort([3, -1, 4, -5, 2]) == [-5, -1, 2, 3, 4]

    def test_larger_list(self):
        nums = [9, 7, 6, 8, 5, 4, 3, 2, 1, 0]
        assert pancake_sort(nums) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_result_is_sorted(self):
        import random
        nums = [random.randint(-100, 100) for _ in range(20)]
        result = pancake_sort(nums)
        assert result == sorted(nums)

    def test_result_contains_same_elements(self):
        nums = [5, 3, 1, 4, 2]
        result = pancake_sort(nums)
        assert sorted(result) == sorted(nums)

    def test_floats(self):
        assert pancake_sort([3.5, 1.2, 2.7, 0.1]) == [0.1, 1.2, 2.7, 3.5]

    def test_function_does_not_modify_input_in_place(self):
        # The function creates new lists rather than modifying in place
        nums = [3, 1, 2]
        original = nums.copy()
        pancake_sort(nums)
        # Since the function reassigns locally, the original list is unchanged
        assert nums == original
