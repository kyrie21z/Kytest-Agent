import pytest
from solution import strange_sort_list


class TestStrangeSortList:
    """Tests for the strange_sort_list function."""

    # --- Basic / canonical examples from docstring ---

    def test_example_1(self):
        assert strange_sort_list([1, 2, 3, 4]) == [1, 4, 2, 3]

    def test_example_2(self):
        assert strange_sort_list([5, 5, 5, 5]) == [5, 5, 5, 5]

    def test_example_3_empty(self):
        assert strange_sort_list([]) == []

    # --- Single element ---

    def test_single_element(self):
        assert strange_sort_list([42]) == [42]

    def test_single_zero(self):
        assert strange_sort_list([0]) == [0]

    # --- Two elements ---

    def test_two_elements_unsorted(self):
        assert strange_sort_list([3, 1]) == [1, 3]

    def test_two_elements_already_sorted(self):
        assert strange_sort_list([1, 2]) == [1, 2]

    def test_two_equal_elements(self):
        assert strange_sort_list([7, 7]) == [7, 7]

    # --- Even-length lists ---

    def test_even_length_four(self):
        assert strange_sort_list([4, 3, 2, 1]) == [1, 4, 2, 3]

    def test_even_length_six(self):
        result = strange_sort_list([6, 5, 4, 3, 2, 1])
        assert result == [1, 6, 2, 5, 3, 4]

    def test_even_length_with_duplicates(self):
        assert strange_sort_list([1, 2, 2, 1]) == [1, 2, 1, 2]

    # --- Odd-length lists ---

    def test_odd_length_three(self):
        assert strange_sort_list([3, 1, 2]) == [1, 3, 2]

    def test_odd_length_five(self):
        result = strange_sort_list([5, 1, 4, 2, 3])
        assert result == [1, 5, 2, 4, 3]

    def test_odd_length_one(self):
        assert strange_sort_list([10]) == [10]

    # --- Negative numbers ---

    def test_negative_numbers(self):
        result = strange_sort_list([-3, -1, -2])
        assert result == [-3, -1, -2]

    def test_mixed_positive_and_negative(self):
        result = strange_sort_list([-1, 3, -2, 2, -3, 1])
        assert result == [-3, 3, -2, 2, -1, 1]

    def test_all_negative(self):
        result = strange_sort_list([-5, -1, -3, -2, -4])
        assert result == [-5, -1, -4, -2, -3]

    # --- Zero values ---

    def test_with_zeros(self):
        result = strange_sort_list([0, 3, 0, 1, 0, 2])
        assert result == [0, 3, 0, 2, 0, 1]

    def test_all_zeros(self):
        assert strange_sort_list([0, 0, 0, 0]) == [0, 0, 0, 0]

    # --- Large duplicates ---

    def test_all_same_large(self):
        assert strange_sort_list([9, 9, 9, 9, 9]) == [9, 9, 9, 9, 9]

    # --- Already sorted input ---

    def test_already_sorted(self):
        assert strange_sort_list([1, 2, 3, 4, 5]) == [1, 5, 2, 4, 3]

    # --- Reverse sorted input ---

    def test_reverse_sorted(self):
        assert strange_sort_list([5, 4, 3, 2, 1]) == [1, 5, 2, 4, 3]

    # --- Larger lists ---

    def test_larger_list_ten_elements(self):
        lst = list(range(1, 11))
        result = strange_sort_list(lst)
        assert result == [1, 10, 2, 9, 3, 8, 4, 7, 5, 6]

    def test_larger_list_twenty_elements(self):
        lst = list(range(1, 21))
        result = strange_sort_list(lst)
        assert result == [1, 20, 2, 19, 3, 18, 4, 17, 5, 16, 6, 15, 7, 14, 8, 13, 9, 12, 10, 11]

    # --- Edge case: very large integers ---

    def test_large_integers(self):
        result = strange_sort_list([10**9, 1, 10**8, 2])
        assert result == [1, 10**9, 2, 10**8]

    # --- Return type checks ---

    def test_returns_list(self):
        assert isinstance(strange_sort_list([1, 2]), list)

    def test_empty_returns_list(self):
        assert isinstance(strange_sort_list([]), list)

    # --- Length preservation ---

    def test_preserves_length(self):
        for length in range(10):
            lst = list(range(length))
            assert len(strange_sort_list(lst)) == length

    # --- Contains all original elements (multiset equality) ---

    def test_contains_all_elements(self):
        lst = [3, 1, 4, 1, 5, 9, 2, 6]
        result = strange_sort_list(lst)
        assert sorted(result) == sorted(lst)

    def test_contains_all_elements_empty(self):
        assert strange_sort_list([]) == []

    def test_contains_all_elements_duplicates(self):
        lst = [7, 7, 3, 3, 7]
        result = strange_sort_list(lst)
        assert sorted(result) == sorted(lst)
