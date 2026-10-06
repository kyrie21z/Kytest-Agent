import pytest
from solution import sort_array


class TestSortArray:
    """Tests for the sort_array function."""

    # --- Empty input ---
    def test_empty_array(self):
        assert sort_array([]) == []

    # --- Single element ---
    def test_single_element(self):
        assert sort_array([5]) == [5]

    def test_single_zero(self):
        assert sort_array([0]) == [0]

    # --- Two elements: sum is odd → ascending ---
    def test_two_elements_sum_odd_ascending(self):
        # 2 + 3 = 5 (odd) → ascending
        assert sort_array([2, 3]) == [2, 3]

    def test_two_elements_sum_odd_ascending_unsorted(self):
        # 3 + 2 = 5 (odd) → ascending
        assert sort_array([3, 2]) == [2, 3]

    # --- Two elements: sum is even → descending ---
    def test_two_elements_sum_even_descending(self):
        # 2 + 4 = 6 (even) → descending
        assert sort_array([2, 4]) == [4, 2]

    def test_two_elements_sum_even_descending_reversed(self):
        # 4 + 2 = 6 (even) → descending
        assert sort_array([4, 2]) == [4, 2]

    # --- Already sorted ascending, sum odd → stays ascending ---
    def test_already_sorted_ascending_sum_odd(self):
        # 0 + 5 = 5 (odd) → ascending
        assert sort_array([0, 1, 2, 3, 4, 5]) == [0, 1, 2, 3, 4, 5]

    # --- Already sorted descending, sum even → stays descending ---
    def test_already_sorted_descending_sum_even(self):
        # 6 + 0 = 6 (even) → descending
        assert sort_array([6, 5, 4, 3, 2, 1, 0]) == [6, 5, 4, 3, 2, 1, 0]

    # --- Unsorted array, sum odd → ascending ---
    def test_unsorted_sum_odd_ascending(self):
        # 2 + 5 = 7 (odd) → ascending
        assert sort_array([2, 4, 3, 0, 1, 5]) == [0, 1, 2, 3, 4, 5]

    # --- Unsorted array, sum even → descending ---
    def test_unsorted_sum_even_descending(self):
        # 2 + 6 = 8 (even) → descending
        assert sort_array([2, 4, 3, 0, 1, 5, 6]) == [6, 5, 4, 3, 2, 1, 0]

    # --- Duplicates ---
    def test_duplicates_sum_odd(self):
        # first=3, last=2, sum=5 (odd) → ascending
        assert sort_array([3, 1, 3, 2]) == [1, 2, 3, 3]

    def test_duplicates_sum_even(self):
        # first=3, last=2, sum=5 (odd) → ascending
        assert sort_array([3, 1, 3, 2]) == [1, 2, 3, 3]

    def test_all_same_elements(self):
        # 5 + 5 = 10 (even) → descending (same result)
        assert sort_array([5, 5, 5, 5]) == [5, 5, 5, 5]

    # --- Large numbers ---
    def test_large_numbers_sum_odd(self):
        # first=1000000, last=500000, sum=1500000 (even) → descending
        assert sort_array([1000000, 999999, 500000]) == [1000000, 999999, 500000]

    def test_large_numbers_sum_even(self):
        # first=1000000, last=1000000, sum=2000000 (even) → descending
        assert sort_array([1000000, 500000, 1000000]) == [1000000, 1000000, 500000]

    # --- Original array not modified ---
    def test_original_not_modified(self):
        original = [3, 1, 4, 1, 5, 9]
        result = sort_array(original)
        assert result != original  # should be sorted differently
        assert original == [3, 1, 4, 1, 5, 9]  # unchanged

    def test_original_not_modified_empty(self):
        original = []
        result = sort_array(original)
        assert result == []
        assert original == []

    # --- Edge cases with zero ---
    def test_with_zeros_sum_odd(self):
        # first=0, last=1, sum=1 (odd) → ascending
        assert sort_array([0, 0, 1]) == [0, 0, 1]

    def test_with_zeros_sum_even(self):
        # first=0, last=0, sum=0 (even) → descending
        assert sort_array([0, 0, 0]) == [0, 0, 0]

    def test_only_zeros(self):
        assert sort_array([0, 0, 0, 0]) == [0, 0, 0, 0]

    # --- Three element arrays ---
    def test_three_elements_sum_odd(self):
        # first=1, last=2, sum=3 (odd) → ascending
        assert sort_array([1, 3, 2]) == [1, 2, 3]

    def test_three_elements_sum_even(self):
        # first=1, last=3, sum=4 (even) → descending
        assert sort_array([1, 2, 3]) == [3, 2, 1]

    # --- Return type check ---
    def test_returns_list(self):
        assert isinstance(sort_array([3, 1, 2]), list)

    def test_returns_new_list(self):
        original = [3, 1, 2]
        result = sort_array(original)
        assert result is not original

    # --- Comprehensive examples from docstring ---
    def test_docstring_example_empty(self):
        assert sort_array([]) == []

    def test_docstring_example_single(self):
        assert sort_array([5]) == [5]

    def test_docstring_example_ascending(self):
        assert sort_array([2, 4, 3, 0, 1, 5]) == [0, 1, 2, 3, 4, 5]

    def test_docstring_example_descending(self):
        assert sort_array([2, 4, 3, 0, 1, 5, 6]) == [6, 5, 4, 3, 2, 1, 0]
