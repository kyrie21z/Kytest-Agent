import pytest
from solution import pluck


class TestPluckBasicCases:
    """Test basic functionality from the docstring examples."""

    def test_example_1(self):
        """[4,2,3] -> [2, 1]"""
        assert pluck([4, 2, 3]) == [2, 1]

    def test_example_2(self):
        """[1,2,3] -> [2, 1]"""
        assert pluck([1, 2, 3]) == [2, 1]

    def test_example_3_empty(self):
        """[] -> []"""
        assert pluck([]) == []

    def test_example_4(self):
        """[5, 0, 3, 0, 4, 2] -> [0, 1]"""
        assert pluck([5, 0, 3, 0, 4, 2]) == [0, 1]


class TestPluckSingleElement:
    """Test arrays with a single element."""

    def test_single_even(self):
        assert pluck([4]) == [4, 0]

    def test_single_odd(self):
        assert pluck([3]) == []

    def test_single_zero(self):
        assert pluck([0]) == [0, 0]


class TestPluckNoEvenValues:
    """Test arrays where all values are odd."""

    def test_all_odd(self):
        assert pluck([1, 3, 5, 7]) == []

    def test_mixed_no_even(self):
        assert pluck([9, 11, 13]) == []

    def test_single_odd_element(self):
        assert pluck([7]) == []


class TestPluckMultipleEvens:
    """Test arrays with multiple even values — pick the smallest."""

    def test_smallest_even_not_first(self):
        assert pluck([8, 6, 4, 2]) == [2, 3]

    def test_smallest_even_in_middle(self):
        assert pluck([10, 4, 8, 2, 6]) == [2, 3]

    def test_smallest_even_at_start(self):
        assert pluck([2, 4, 6, 8]) == [2, 0]

    def test_large_values(self):
        assert pluck([100, 50, 200, 10]) == [10, 3]


class TestPluckDuplicateSmallestEven:
    """Test that the first occurrence (smallest index) is returned."""

    def test_duplicate_zeros(self):
        assert pluck([5, 0, 3, 0, 4, 2]) == [0, 1]

    def test_duplicate_twos(self):
        assert pluck([4, 2, 6, 2, 8]) == [2, 1]

    def test_duplicate_at_end(self):
        assert pluck([2, 4, 6, 2]) == [2, 0]

    def test_multiple_duplicates(self):
        assert pluck([4, 2, 2, 2, 6]) == [2, 1]


class TestPluckZeroHandling:
    """Test edge cases involving zero as an even value."""

    def test_zero_is_smallest(self):
        assert pluck([10, 8, 0, 6]) == [0, 2]

    def test_only_zeros(self):
        assert pluck([0, 0, 0]) == [0, 0]

    def test_zero_with_odds(self):
        assert pluck([1, 3, 0, 5]) == [0, 2]


class TestPluckLargerArrays:
    """Test with larger arrays to ensure correctness at scale."""

    def test_sorted_descending_evens(self):
        arr = list(range(20, 0, -2))  # [20, 18, ..., 2], length 10
        assert pluck(arr) == [2, 9]

    def test_sorted_ascending_evens(self):
        arr = list(range(2, 22, 2))  # [2, 4, ..., 20]
        assert pluck(arr) == [2, 0]

    def test_random_order(self):
        arr = [12, 7, 3, 8, 1, 4, 9, 2, 6]
        assert pluck(arr) == [2, 7]

    def test_many_odds_one_even(self):
        arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 2, 19]
        assert pluck(arr) == [2, 9]

    def test_many_evens_one_odd(self):
        arr = [10, 8, 6, 4, 2, 1, 0]
        assert pluck(arr) == [0, 6]


class TestPluckEdgeCases:
    """Additional edge cases."""

    def test_two_elements_both_even(self):
        assert pluck([6, 4]) == [4, 1]

    def test_two_elements_one_even(self):
        assert pluck([3, 4]) == [4, 1]

    def test_two_elements_first_even(self):
        assert pluck([4, 3]) == [4, 0]

    def test_two_elements_both_odd(self):
        assert pluck([3, 5]) == []

    def test_large_uniform_array(self):
        arr = [4] * 10000
        assert pluck(arr) == [4, 0]

    def test_alternating_odd_even(self):
        arr = [1, 2, 3, 4, 5, 6]
        assert pluck(arr) == [2, 1]
