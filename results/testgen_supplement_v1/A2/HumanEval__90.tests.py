"""Unit tests for next_smallest() in solution.py."""

import pytest
from solution import next_smallest


class TestNextSmallestNormalCases:
    """Tests with typical inputs containing at least two distinct values."""

    def test_sorted_ascending(self):
        assert next_smallest([1, 2, 3, 4, 5]) == 2

    def test_unordered(self):
        assert next_smallest([5, 1, 4, 3, 2]) == 2

    def test_two_elements_different(self):
        assert next_smallest([10, 20]) == 20

    def test_two_elements_reversed(self):
        # sorted: [10, 20], second smallest is 20
        assert next_smallest([20, 10]) == 20

    def test_three_elements(self):
        assert next_smallest([3, 1, 2]) == 2

    def test_with_duplicates_at_start(self):
        assert next_smallest([1, 1, 2]) == 2

    def test_with_duplicates_at_end(self):
        assert next_smallest([1, 2, 2]) == 2

    def test_large_values(self):
        assert next_smallest([1000000, 999999, 1]) == 999999

    def test_negative_and_positive(self):
        assert next_smallest([-5, 0, 5]) == 0

    def test_all_negative(self):
        assert next_smallest([-1, -2, -3]) == -2

    def test_mixed_negatives(self):
        assert next_smallest([-5, -1, -3]) == -3

    def test_many_duplicates(self):
        assert next_smallest([1, 1, 1, 2, 2, 3]) == 2

    def test_single_duplicate_pair(self):
        assert next_smallest([7, 7, 8]) == 8

    def test_second_smallest_in_middle_of_list(self):
        # sorted: [3, 5, 6, 8, 10], second smallest is 5
        assert next_smallest([10, 5, 8, 3, 6]) == 5


class TestNextSmallestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_empty_list(self):
        assert next_smallest([]) is None

    def test_single_element(self):
        assert next_smallest([42]) is None

    def test_two_identical_elements(self):
        assert next_smallest([5, 5]) is None

    def test_all_same_elements_three(self):
        assert next_smallest([7, 7, 7]) is None

    def test_all_same_elements_many(self):
        assert next_smallest([3, 3, 3, 3, 3]) is None

    def test_min_max_boundary(self):
        # Smallest possible distinct pair
        assert next_smallest([0, 1]) == 1

    def test_zero_present(self):
        assert next_smallest([0, 0, 1]) == 1

    def test_only_zeros(self):
        assert next_smallest([0, 0, 0]) is None


class TestNextSmallestEdgeInputs:
    """Tests with edge-case inputs that may cause unexpected behavior."""

    def test_list_with_one_element_repeated(self):
        assert next_smallest([1, 1]) is None

    def test_larger_list_all_same(self):
        assert next_smallest([99, 99, 99, 99, 99, 99]) is None

    def test_extreme_negative_values(self):
        assert next_smallest([-1000000, -999999, -1]) == -999999

    def test_wide_range(self):
        assert next_smallest([1, 1000000000, 500000000]) == 500000000

    def test_multiple_distinct_values_many_duplicates(self):
        assert next_smallest([2, 2, 2, 2, 3, 3, 3, 4]) == 3


class TestNextSmallestTypeAndStructure:
    """Tests verifying return type and structural correctness."""

    def test_return_type_int(self):
        result = next_smallest([1, 2])
        assert isinstance(result, int)

    def test_return_type_none(self):
        result = next_smallest([])
        assert result is None

    def test_does_not_modify_input(self):
        lst = [3, 1, 2]
        original = list(lst)
        next_smallest(lst)
        assert lst == original
