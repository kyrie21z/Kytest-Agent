import pytest
from solution import next_smallest


class TestNextSmallest:
    """Tests for the next_smallest function."""

    # --- Basic happy-path cases ---

    def test_basic_increasing(self):
        assert next_smallest([1, 2, 3, 4, 5]) == 2

    def test_basic_unsorted(self):
        assert next_smallest([5, 1, 4, 3, 2]) == 2

    def test_two_elements(self):
        assert next_smallest([1, 2]) == 2

    def test_two_elements_reversed(self):
        # [2, 1] -> sorted [1, 2] -> second smallest is 2
        assert next_smallest([2, 1]) == 2

    def test_three_elements(self):
        assert next_smallest([3, 1, 2]) == 2

    # --- Edge case: empty list ---

    def test_empty_list(self):
        assert next_smallest([]) is None

    # --- Edge case: single element ---

    def test_single_element(self):
        assert next_smallest([42]) is None

    # --- All identical elements ---

    def test_all_identical(self):
        assert next_smallest([7, 7, 7]) is None

    def test_all_identical_two(self):
        assert next_smallest([1, 1]) is None

    # --- Duplicates with distinct second smallest ---

    def test_duplicates_with_second_smallest(self):
        assert next_smallest([3, 3, 1, 2, 1]) == 2

    def test_duplicate_minimum(self):
        assert next_smallest([1, 1, 2, 3]) == 2

    def test_duplicate_maximum(self):
        assert next_smallest([1, 2, 3, 3]) == 2

    def test_many_duplicates(self):
        assert next_smallest([5, 5, 5, 1, 2, 1, 5]) == 2

    # --- Negative numbers ---

    def test_negative_numbers(self):
        assert next_smallest([-3, -1, -2]) == -2

    def test_mixed_positive_negative(self):
        assert next_smallest([-1, 0, 1]) == 0

    def test_all_negative(self):
        assert next_smallest([-5, -3, -4, -1, -2]) == -4

    # --- Large values ---

    def test_large_values(self):
        assert next_smallest([1000000, 999999, 1000001]) == 1000000

    # --- Two-element lists with duplicates ---

    def test_two_identical_elements(self):
        assert next_smallest([5, 5]) is None

    # --- Larger lists with varied data ---

    def test_ten_elements(self):
        result = next_smallest([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
        assert result == 2

    def test_larger_list_with_gaps(self):
        assert next_smallest([10, 20, 30, 40, 50]) == 20

    # --- Type / input validation (if applicable) ---
    # The docstring says "list of integers", but we test common edge inputs.

    def test_list_with_zero(self):
        assert next_smallest([0, 1, 2]) == 1

    def test_zero_and_negatives(self):
        assert next_smallest([-1, 0, 1]) == 0

    # --- Return type checks ---

    def test_returns_int(self):
        assert isinstance(next_smallest([1, 2, 3]), int)

    def test_returns_none_for_empty(self):
        assert next_smallest([]) is None

    def test_returns_none_for_no_second(self):
        assert next_smallest([1, 1, 1]) is None
