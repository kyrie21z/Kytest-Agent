import pytest
from solution import next_smallest


class TestNextSmallest:
    """Tests for the next_smallest function."""

    # --- Basic functionality ---

    def test_basic_increasing(self):
        assert next_smallest([1, 2, 3, 4, 5]) == 2

    def test_basic_unordered(self):
        assert next_smallest([5, 1, 4, 3, 2]) == 2

    def test_basic_decreasing(self):
        assert next_smallest([5, 4, 3, 2, 1]) == 2

    def test_two_distinct_elements(self):
        assert next_smallest([1, 2]) == 2

    def test_two_distinct_elements_reversed(self):
        # sorted([2, 1]) = [1, 2], 2nd smallest is 2
        assert next_smallest([2, 1]) == 2

    # --- Edge cases: no second smallest ---

    def test_empty_list(self):
        assert next_smallest([]) is None

    def test_single_element(self):
        assert next_smallest([1]) is None

    def test_all_identical_elements(self):
        assert next_smallest([1, 1]) is None

    def test_all_identical_multiple(self):
        assert next_smallest([3, 3, 3, 3]) is None

    # --- Negative numbers ---

    def test_negative_numbers(self):
        assert next_smallest([-5, -1, -3, -2, -4]) == -4

    def test_mixed_positive_negative(self):
        assert next_smallest([-1, 0, 1, 2]) == 0

    def test_only_negatives(self):
        assert next_smallest([-3, -2, -1]) == -2

    # --- Duplicates with distinct second smallest ---

    def test_duplicates_with_second_smallest(self):
        assert next_smallest([1, 1, 2, 3]) == 2

    def test_duplicates_at_bottom(self):
        assert next_smallest([1, 1, 1, 2, 3]) == 2

    def test_duplicates_not_at_bottom(self):
        assert next_smallest([1, 2, 2, 3]) == 2

    def test_many_duplicates(self):
        assert next_smallest([1, 1, 1, 1, 2]) == 2

    # --- Larger lists ---

    def test_larger_list(self):
        lst = list(range(1, 101))
        assert next_smallest(lst) == 2

    def test_larger_list_with_duplicate_min(self):
        lst = [0] + list(range(1, 101))
        assert next_smallest(lst) == 1

    # --- Single pair returning None ---

    def test_two_same_elements(self):
        assert next_smallest([7, 7]) is None

    # --- Three elements ---

    def test_three_distinct(self):
        assert next_smallest([10, 5, 8]) == 8

    def test_three_with_duplicate_min(self):
        assert next_smallest([1, 1, 2]) == 2

    def test_three_all_same(self):
        assert next_smallest([5, 5, 5]) is None

    # --- Zero values ---

    def test_with_zero(self):
        assert next_smallest([0, 1, 2]) == 1

    def test_zero_and_negative(self):
        assert next_smallest([-1, 0, 1]) == 0

    def test_only_zeros(self):
        assert next_smallest([0, 0, 0]) is None
