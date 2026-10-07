import pytest
from solution import comb_sort


class TestCombSortBasic:
    """Test basic sorting functionality."""

    def test_empty_list(self):
        assert comb_sort([]) == []

    def test_single_element(self):
        assert comb_sort([1]) == [1]

    def test_two_elements_sorted(self):
        assert comb_sort([1, 2]) == [1, 2]

    def test_two_elements_unsorted(self):
        assert comb_sort([2, 1]) == [1, 2]

    def test_already_sorted(self):
        assert comb_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert comb_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_random_order(self):
        assert comb_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]


class TestCombSortDuplicates:
    """Test handling of duplicate values."""

    def test_all_same_elements(self):
        assert comb_sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    def test_two_duplicates(self):
        assert comb_sort([2, 1, 2]) == [1, 2, 2]

    def test_many_duplicates(self):
        assert comb_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


class TestCombSortNegativeNumbers:
    """Test handling of negative numbers."""

    def test_all_negative(self):
        assert comb_sort([-3, -1, -4, -1, -5]) == [-5, -4, -3, -1, -1]

    def test_mixed_positive_and_negative(self):
        assert comb_sort([3, -1, 4, -1, 5, -9, 2, -6]) == [-9, -6, -1, -1, 2, 3, 4, 5]

    def test_zero_and_negative(self):
        assert comb_sort([0, -1, 1, -2, 2]) == [-2, -1, 0, 1, 2]


class TestCombSortLargeInput:
    """Test with larger inputs."""

    def test_larger_list(self):
        data = [64, 34, 25, 12, 22, 11, 90, 1, 55, 33, 78, 44, 88, 23, 67]
        expected = sorted(data)
        assert comb_sort(data) == expected

    def test_100_elements(self):
        import random
        random.seed(42)
        data = [random.randint(-1000, 1000) for _ in range(100)]
        expected = sorted(data)
        assert comb_sort(data) == expected


class TestCombSortInPlace:
    """Test that the function modifies the list in place."""

    def test_in_place_modification(self):
        original = [5, 3, 1, 4, 2]
        result = comb_sort(original)
        # The returned value should be the sorted list
        assert result == [1, 2, 3, 4, 5]
        # The original list should also be modified
        assert original == [1, 2, 3, 4, 5]

    def test_returns_same_object(self):
        original = [5, 3, 1, 4, 2]
        result = comb_sort(original)
        assert result is original


class TestCombSortEdgeCases:
    """Test edge cases."""

    def test_single_duplicate(self):
        assert comb_sort([1, 1]) == [1, 1]

    def test_three_identical(self):
        assert comb_sort([7, 7, 7]) == [7, 7, 7]

    def test_alternating_pattern(self):
        assert comb_sort([1, 3, 2, 4, 1, 3, 2, 4]) == [1, 1, 2, 2, 3, 3, 4, 4]

    def test_large_values(self):
        assert comb_sort([10**9, 1, 10**8, 2, 10**7]) == [1, 2, 10**7, 10**8, 10**9]

    def test_floats(self):
        assert comb_sort([3.5, 1.2, 4.8, 2.1]) == [1.2, 2.1, 3.5, 4.8]

    def test_mixed_int_float(self):
        assert comb_sort([3, 1.5, 2, 4.5]) == [1.5, 2, 3, 4.5]
