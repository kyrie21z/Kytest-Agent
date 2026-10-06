import pytest
from solution import sort_third


class TestSortThird:
    """Unit tests for the sort_third function."""

    def test_empty_list(self):
        assert sort_third([]) == []

    def test_single_element(self):
        assert sort_third([1]) == [1]

    def test_two_elements(self):
        assert sort_third([5, 3]) == [5, 3]

    def test_three_elements_already_sorted(self):
        assert sort_third([1, 2, 3]) == [1, 2, 3]

    def test_four_elements_need_sorting(self):
        # Indices 0 and 3 are divisible by 3 -> values [3, 1] sorted -> [1, 3]
        assert sort_third([3, 2, 1, 1]) == [1, 2, 1, 3]

    def test_example_from_docstring_1(self):
        assert sort_third([1, 2, 3]) == [1, 2, 3]

    def test_example_from_docstring_2(self):
        assert sort_third([5, 6, 3, 4, 8, 9, 2]) == [2, 6, 3, 4, 8, 9, 5]

    def test_all_elements_at_divisible_indices(self):
        # Indices 0, 3, 6 -> values [9, 7, 1] sorted -> [1, 7, 9]
        assert sort_third([9, 2, 3, 7, 5, 6, 1, 8, 4]) == [1, 2, 3, 7, 5, 6, 9, 8, 4]

    def test_negative_numbers(self):
        # Indices 0, 3 -> values [-5, -2] sorted -> [-5, -2]
        assert sort_third([-5, 1, 2, -2, 4, 5]) == [-5, 1, 2, -2, 4, 5]

    def test_negative_numbers_need_reordering(self):
        # Indices 0, 3 -> values [3, -1] sorted -> [-1, 3]
        assert sort_third([3, 1, 2, -1, 4, 5]) == [-1, 1, 2, 3, 4, 5]

    def test_duplicate_values(self):
        # Indices 0, 3, 6 -> values [2, 2, 2] sorted -> [2, 2, 2]
        assert sort_third([2, 5, 3, 2, 7, 8, 2, 1, 9]) == [2, 5, 3, 2, 7, 8, 2, 1, 9]

    def test_duplicates_need_reordering(self):
        # Indices 0, 3, 6 -> values [5, 1, 3] sorted -> [1, 3, 5]
        assert sort_third([5, 2, 3, 1, 4, 6, 3, 7, 8]) == [1, 2, 3, 3, 4, 6, 5, 7, 8]

    def test_length_four(self):
        # Index 0, 3 -> values [4, 2] sorted -> [2, 4]
        assert sort_third([4, 1, 3, 2]) == [2, 1, 3, 4]

    def test_length_five(self):
        # Index 0, 3 -> values [6, 2] sorted -> [2, 6]
        assert sort_third([6, 1, 3, 2, 5]) == [2, 1, 3, 6, 5]

    def test_length_six(self):
        # Index 0, 3 -> values [8, 2] sorted -> [2, 8]
        assert sort_third([8, 1, 3, 2, 5, 6]) == [2, 1, 3, 8, 5, 6]

    def test_preserves_non_divisible_indices(self):
        # Only indices 0, 3 change; indices 1, 2, 4, 5 stay the same
        result = sort_third([9, 10, 11, 1, 13, 14])
        assert result[1] == 10
        assert result[2] == 11
        assert result[4] == 13
        assert result[5] == 14
        assert result[0] == 1  # sorted from [9, 1]
        assert result[3] == 9  # sorted from [9, 1]

    def test_large_list(self):
        lst = list(range(100))
        # Shuffle elements at indices divisible by 3
        third_indices = [i for i in range(100) if i % 3 == 0]
        third_values = [lst[i] for i in third_indices]
        third_values.sort()
        expected = lst[:]
        for idx, val in zip(third_indices, third_values):
            expected[idx] = val
        assert sort_third(lst) == expected

    def test_returns_new_list(self):
        original = [5, 1, 3, 2, 4, 6]
        result = sort_third(original)
        assert result != original or result is not original
        # Verify original is not mutated
        assert original == [5, 1, 3, 2, 4, 6]

    def test_all_same_values(self):
        assert sort_third([7, 7, 7, 7, 7]) == [7, 7, 7, 7, 7]

    def test_reverse_sorted_list(self):
        # Indices 0, 3, 6 -> [6, 3, 0] sorted -> [0, 3, 6]
        assert sort_third([6, 5, 4, 3, 2, 1, 0]) == [0, 5, 4, 3, 2, 1, 6]
