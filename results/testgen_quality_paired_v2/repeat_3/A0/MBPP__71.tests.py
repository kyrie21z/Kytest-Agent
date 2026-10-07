import pytest
from solution import comb_sort


class TestCombSortBasic:
    """Tests for basic sorting functionality."""

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
    """Tests for lists with duplicate values."""

    def test_all_same_elements(self):
        assert comb_sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    def test_some_duplicates(self):
        assert comb_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]

    def test_two_identical_elements(self):
        assert comb_sort([7, 7]) == [7, 7]


class TestCombSortNegativeNumbers:
    """Tests for lists containing negative numbers."""

    def test_all_negative(self):
        assert comb_sort([-3, -1, -4, -1, -5]) == [-5, -4, -3, -1, -1]

    def test_mixed_positive_negative(self):
        assert comb_sort([3, -1, 4, -1, 5, -9, 2, -6]) == [-9, -6, -1, -1, 2, 3, 4, 5]

    def test_negative_and_zero(self):
        assert comb_sort([0, -1, 2, -3]) == [-3, -1, 0, 2]


class TestCombSortLargeInput:
    """Tests for larger input sizes."""

    def test_larger_list(self):
        nums = [i for i in range(100, 0, -1)]
        expected = list(range(1, 101))
        assert comb_sort(nums) == expected

    def test_many_duplicates_large(self):
        nums = [3] * 50 + [1] * 50 + [2] * 50
        expected = [1] * 50 + [2] * 50 + [3] * 50
        assert comb_sort(nums) == expected


class TestCombSortInPlace:
    """Tests verifying in-place modification behavior."""

    def test_returns_same_list_object(self):
        nums = [3, 1, 2]
        result = comb_sort(nums)
        assert result is nums

    def test_modifies_original_list(self):
        nums = [3, 1, 2]
        comb_sort(nums)
        assert nums == [1, 2, 3]


class TestCombSortEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_two_elements_swapped(self):
        assert comb_sort([2, 1]) == [1, 2]

    def test_three_elements_cyclic(self):
        # 2 -> 3 -> 1 -> 2 pattern
        assert comb_sort([2, 3, 1]) == [1, 2, 3]

    def test_float_values(self):
        assert comb_sort([3.5, 1.2, 4.8, 1.2]) == [1.2, 1.2, 3.5, 4.8]

    def test_single_duplicate_pair(self):
        assert comb_sort([1, 2, 2, 3]) == [1, 2, 2, 3]

    def test_alternating_pattern(self):
        assert comb_sort([5, 1, 4, 2, 3]) == [1, 2, 3, 4, 5]


class TestCombSortReturnValues:
    """Tests verifying correct return values match sorted order."""

    @pytest.mark.parametrize("input_list,expected", [
        ([], []),
        ([1], [1]),
        ([2, 1], [1, 2]),
        ([1, 2, 3], [1, 2, 3]),
        ([3, 2, 1], [1, 2, 3]),
        ([1, 3, 2], [1, 2, 3]),
        ([5, 3, 8, 1, 9, 2, 7, 4, 6], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ])
    def test_return_value(self, input_list, expected):
        assert comb_sort(input_list) == expected
