import pytest
from solution import find_closest_elements


class TestFindClosestElements:
    """Tests for the find_closest_elements function."""

    # --- Basic functionality from docstring examples ---

    def test_docstring_example_1(self):
        result = find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.2])
        assert result == (2.0, 2.2)

    def test_docstring_example_2(self):
        result = find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0])
        assert result == (2.0, 2.0)

    # --- Minimum length input (exactly two elements) ---

    def test_two_elements(self):
        result = find_closest_elements([1.0, 5.0])
        assert result == (1.0, 5.0)

    def test_two_elements_reversed(self):
        result = find_closest_elements([5.0, 1.0])
        assert result == (1.0, 5.0)

    def test_two_identical_elements(self):
        result = find_closest_elements([3.0, 3.0])
        assert result == (3.0, 3.0)

    # --- Already sorted list ---

    def test_already_sorted(self):
        result = find_closest_elements([1.0, 2.0, 3.0, 4.0])
        assert result == (1.0, 2.0)

    # --- Reverse sorted list ---

    def test_reverse_sorted(self):
        result = find_closest_elements([5.0, 4.0, 3.0, 2.0, 1.0])
        assert result == (1.0, 2.0)

    # --- Unsorted list ---

    def test_unsorted_list(self):
        # Sorted: [1.0, 3.0, 5.0, 8.0, 10.0]; diffs: 2, 2, 3, 2 -> first min is (1.0, 3.0)
        result = find_closest_elements([10.0, 1.0, 5.0, 3.0, 8.0])
        assert result == (1.0, 3.0)

    # --- Closest pair at the beginning ---

    def test_closest_at_start(self):
        result = find_closest_elements([1.0, 1.5, 10.0, 20.0])
        assert result == (1.0, 1.5)

    # --- Closest pair at the end ---

    def test_closest_at_end(self):
        result = find_closest_elements([1.0, 10.0, 20.0, 20.5])
        assert result == (20.0, 20.5)

    # --- Closest pair in the middle ---

    def test_closest_in_middle(self):
        result = find_closest_elements([1.0, 10.0, 10.3, 20.0])
        assert result == (10.0, 10.3)

    # --- Duplicate values ---

    def test_duplicates_multiple(self):
        result = find_closest_elements([1.0, 2.0, 2.0, 3.0])
        assert result == (2.0, 2.0)

    def test_all_same_values(self):
        result = find_closest_elements([7.0, 7.0, 7.0, 7.0])
        assert result == (7.0, 7.0)

    # --- Negative numbers ---

    def test_negative_numbers(self):
        result = find_closest_elements([-5.0, -1.0, -3.0, -2.0])
        assert result == (-3.0, -2.0)

    def test_mixed_positive_negative(self):
        result = find_closest_elements([-1.0, 0.0, 1.0, 2.0])
        assert result == (-1.0, 0.0)

    def test_closest_across_zero(self):
        result = find_closest_elements([-0.5, 0.5, 10.0, 20.0])
        assert result == (-0.5, 0.5)

    # --- Floating point precision ---

    def test_floating_point_precision(self):
        result = find_closest_elements([1.0, 1.0001, 5.0, 10.0])
        assert result == (1.0, 1.0001)

    def test_small_differences(self):
        result = find_closest_elements([0.0, 0.000001, 1.0, 2.0])
        assert result == (0.0, 0.000001)

    # --- Larger lists ---

    def test_larger_list(self):
        numbers = list(range(1, 101))
        result = find_closest_elements(numbers)
        assert result == (1.0, 2.0)

    def test_larger_list_with_close_pair(self):
        numbers = [1.0, 2.0, 3.0, 99.0, 99.5]
        result = find_closest_elements(numbers)
        assert result == (99.0, 99.5)

    # --- Return type checks ---

    def test_returns_tuple(self):
        result = find_closest_elements([1.0, 2.0])
        assert isinstance(result, tuple)

    def test_returns_two_elements(self):
        result = find_closest_elements([1.0, 2.0, 3.0])
        assert len(result) == 2

    def test_first_element_smaller_or_equal(self):
        result = find_closest_elements([1.0, 2.0, 3.0])
        assert result[0] <= result[1]

    # --- Edge case: closest pair has zero difference ---

    def test_zero_difference(self):
        result = find_closest_elements([5.0, 5.0, 1.0, 2.0])
        assert result == (5.0, 5.0)
