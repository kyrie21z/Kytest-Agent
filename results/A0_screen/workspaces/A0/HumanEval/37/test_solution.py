import pytest
from solution import sort_even


class TestSortEven:
    """Tests for the sort_even function."""

    def test_empty_list(self):
        assert sort_even([]) == []

    def test_single_element(self):
        assert sort_even([1]) == [1]

    def test_two_elements(self):
        assert sort_even([2, 1]) == [2, 1]

    def test_three_elements_already_sorted(self):
        assert sort_even([1, 2, 3]) == [1, 2, 3]

    def test_four_elements_example_from_docstring(self):
        assert sort_even([5, 6, 3, 4]) == [3, 6, 5, 4]

    def test_all_even_indices_need_sorting(self):
        # Even indices: 0, 2 -> values 5, 1 -> sorted: 1, 5
        # Odd indices: 1, 3 -> values 2, 3 -> unchanged
        assert sort_even([5, 2, 1, 3]) == [1, 2, 5, 3]

    def test_already_sorted_even_indices(self):
        # Even indices already sorted: 1, 3, 5
        assert sort_even([1, 9, 3, 8, 5, 7]) == [1, 9, 3, 8, 5, 7]

    def test_reverse_sorted_even_indices(self):
        # Even indices: 5, 3, 1 -> sorted: 1, 3, 5
        assert sort_even([5, 9, 3, 8, 1, 7]) == [1, 9, 3, 8, 5, 7]

    def test_negative_numbers(self):
        # Even indices: -1, 3, -5 -> sorted: -5, -1, 3
        assert sort_even([-1, 2, 3, 4, -5, 6]) == [-5, 2, -1, 4, 3, 6]

    def test_duplicate_values_at_even_indices(self):
        # Even indices: 3, 1, 3 -> sorted: 1, 3, 3
        assert sort_even([3, 2, 1, 4, 3, 6]) == [1, 2, 3, 4, 3, 6]

    def test_all_same_values(self):
        assert sort_even([7, 7, 7, 7]) == [7, 7, 7, 7]

    def test_larger_list(self):
        # Even indices: 0, 2, 4, 6, 8 -> values 9, 7, 5, 3, 1 -> sorted: 1, 3, 5, 7, 9
        result = sort_even([9, 2, 7, 4, 5, 6, 3, 8, 1, 10])
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        assert result == expected

    def test_odd_length_list(self):
        # Even indices: 0, 2, 4 -> values 4, 2, 0 -> sorted: 0, 2, 4
        assert sort_even([4, 1, 2, 3, 0, 5]) == [0, 1, 2, 3, 4, 5]

    def test_even_length_list(self):
        # Even indices: 0, 2 -> values 6, 4 -> sorted: 4, 6
        assert sort_even([6, 1, 4, 3]) == [4, 1, 6, 3]

    def test_float_values(self):
        # Even indices: 0, 2 -> values 3.5, 1.2 -> sorted: 1.2, 3.5
        assert sort_even([3.5, 2, 1.2, 4]) == [1.2, 2, 3.5, 4]

    def test_mixed_positive_and_negative(self):
        # Even indices: 0, 2, 4 -> values -3, 0, 5 -> sorted: -3, 0, 5
        assert sort_even([-3, 1, 0, 2, 5, 3]) == [-3, 1, 0, 2, 5, 3]

    def test_returns_new_list(self):
        original = [5, 6, 3, 4]
        result = sort_even(original)
        assert result != original or result is not original
        assert original == [5, 6, 3, 4]  # original should be unchanged

    @pytest.mark.parametrize(
        "input_list, expected",
        [
            ([], []),
            ([1], [1]),
            ([2, 1], [2, 1]),
            ([1, 2, 3], [1, 2, 3]),
            ([5, 6, 3, 4], [3, 6, 5, 4]),
            ([3, 2, 1], [1, 2, 3]),
            ([4, 3, 2, 1], [2, 3, 4, 1]),
            ([10, 1, 8, 2, 6, 3, 4, 4], [4, 1, 6, 2, 8, 3, 10, 4]),
        ],
    )
    def test_parametrized(self, input_list, expected):
        assert sort_even(input_list) == expected
