import pytest
from solution import next_smallest


class TestNextSmallest:
    """Tests for the next_smallest function."""

    # --- Basic positive cases ---

    def test_basic_increasing(self):
        assert next_smallest([1, 2, 3, 4, 5]) == 2

    def test_basic_unsorted(self):
        assert next_smallest([5, 1, 4, 3, 2]) == 2

    def test_two_elements(self):
        assert next_smallest([1, 2]) == 2

    def test_two_elements_reversed(self):
        # Sorted: [1, 2], second smallest distinct = 2
        assert next_smallest([2, 1]) == 2

    def test_larger_list(self):
        assert next_smallest([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) == 2

    def test_negative_numbers(self):
        # Sorted: [-5, -4, -3, -2, -1], second smallest distinct = -4
        assert next_smallest([-5, -2, -3, -1, -4]) == -4

    def test_mixed_positive_negative(self):
        # Sorted: [-1, 0, 1, 2, 3], second smallest distinct = 0
        assert next_smallest([-1, 0, 1, 2, 3]) == 0

    def test_duplicates_not_second(self):
        # Sorted: [1, 1, 2, 3], second smallest distinct = 2
        assert next_smallest([1, 1, 2, 3]) == 2

    def test_all_same_elements(self):
        assert next_smallest([3, 3, 3, 3]) is None

    def test_two_same_elements(self):
        assert next_smallest([1, 1]) is None

    # --- Edge cases returning None ---

    def test_empty_list(self):
        assert next_smallest([]) is None

    def test_single_element(self):
        assert next_smallest([42]) is None

    def test_single_duplicate(self):
        assert next_smallest([7]) is None

    # --- Additional edge cases ---

    def test_large_values(self):
        # Sorted: [999999998, 999999999, 1000000000], second smallest distinct = 999999999
        assert next_smallest([10**9, 10**9 - 1, 10**9 - 2]) == 10**9 - 1

    def test_zero_in_list(self):
        assert next_smallest([0, 1, 2, 3]) == 1

    def test_zero_as_second_smallest(self):
        # Sorted: [-1, 0, 1], second smallest distinct = 0
        assert next_smallest([-1, 0, 1]) == 0

    def test_many_duplicates_one_different(self):
        # Sorted: [1, 5, 5, 5, 5], second smallest distinct = 5
        assert next_smallest([5, 5, 5, 5, 1]) == 5

    def test_second_smallest_at_end(self):
        assert next_smallest([1, 3, 4, 5, 2]) == 2

    def test_second_smallest_at_start(self):
        assert next_smallest([2, 5, 4, 3, 1]) == 2

    def test_three_unique_elements(self):
        # Sorted: [5, 10, 20], second smallest distinct = 10
        assert next_smallest([10, 20, 5]) == 10

    def test_three_elements_all_same(self):
        assert next_smallest([7, 7, 7]) is None

    def test_four_elements_two_pairs(self):
        # Sorted: [1, 1, 2, 2], second smallest distinct = 2
        assert next_smallest([1, 1, 2, 2]) == 2

    def test_negative_and_positive(self):
        # Sorted: [-10, -5, 0, 5, 10], second smallest distinct = -5
        assert next_smallest([-10, -5, 0, 5, 10]) == -5

    def test_return_type_is_none_for_no_result(self):
        result = next_smallest([])
        assert result is None
        result = next_smallest([1, 1])
        assert result is None

    def test_return_type_is_int_for_valid_result(self):
        result = next_smallest([3, 1, 2])
        assert isinstance(result, int)
        assert result == 2
