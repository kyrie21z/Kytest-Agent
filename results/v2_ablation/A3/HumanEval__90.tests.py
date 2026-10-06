import pytest
from solution import next_smallest


class TestNextSmallestNormalCases:
    """Test normal cases with typical inputs."""

    def test_simple_sorted_list(self):
        assert next_smallest([1, 2, 3, 4, 5]) == 2

    def test_unsorted_list(self):
        assert next_smallest([5, 1, 4, 3, 2]) == 2

    def test_two_elements(self):
        assert next_smallest([3, 1]) == 3

    def test_negative_numbers(self):
        assert next_smallest([-5, -3, -1, 0, 2]) == -3

    def test_mixed_positive_and_negative(self):
        assert next_smallest([-10, 0, 5, 3, -5]) == -5

    def test_larger_values(self):
        # [100, 200, 50, 75, 150] -> sorted: [50, 75, 100, 150, 200] -> 2nd smallest = 75
        assert next_smallest([100, 200, 50, 75, 150]) == 75

    def test_consecutive_integers(self):
        assert next_smallest([10, 11, 12, 13, 14]) == 11

    def test_single_duplicate_in_middle(self):
        assert next_smallest([1, 2, 2, 3, 4]) == 2


class TestNextSmallestBoundaryCases:
    """Test boundary cases at the edges of valid input ranges."""

    def test_minimal_distinct_list(self):
        # Exactly 2 distinct elements
        assert next_smallest([1, 5]) == 5

    def test_second_smallest_at_end(self):
        assert next_smallest([5, 4, 3, 2, 1]) == 2

    def test_second_smallest_at_start(self):
        assert next_smallest([2, 5, 4, 3, 1]) == 2

    def test_large_range_values(self):
        assert next_smallest([1, 1000000, 500000, 250000, 2]) == 2

    def test_all_same_value(self):
        assert next_smallest([7, 7, 7, 7, 7]) is None

    def test_two_identical_elements(self):
        assert next_smallest([1, 1]) is None


class TestNextSmallestEmptyAndSingleElement:
    """Test empty, null, or zero-size inputs."""

    def test_empty_list(self):
        assert next_smallest([]) is None

    def test_single_element(self):
        assert next_smallest([42]) is None


class TestNextSmallestDuplicates:
    """Test various duplicate scenarios."""

    def test_duplicates_at_beginning(self):
        assert next_smallest([1, 1, 1, 2, 3]) == 2

    def test_duplicates_at_end(self):
        assert next_smallest([1, 2, 3, 3, 3]) == 2

    def test_duplicates_everywhere(self):
        assert next_smallest([1, 1, 2, 2, 3, 3]) == 2

    def test_many_duplicates_one_unique(self):
        assert next_smallest([5, 5, 5, 5, 5, 6]) == 6

    def test_three_distinct_with_duplicates(self):
        assert next_smallest([10, 10, 20, 20, 30]) == 20

    def test_all_zeros(self):
        assert next_smallest([0, 0, 0]) is None

    def test_zero_and_nonzero(self):
        assert next_smallest([0, 0, 1, 2]) == 1


class TestNextSmallestEdgeValues:
    """Test edge cases involving extreme numeric values."""

    def test_single_negative(self):
        # [-1, -2, -3, -4] -> sorted: [-4, -3, -2, -1] -> 2nd smallest = -3
        assert next_smallest([-1, -2, -3, -4]) == -3

    def test_max_and_min(self):
        assert next_smallest([1, 2**31 - 1, 2, 3]) == 2

    def test_all_negative(self):
        assert next_smallest([-1, -2, -3, -4, -5]) == -4

    def test_large_negative_and_small_positive(self):
        assert next_smallest([-1000000, 1, 2, 3]) == 1


class TestNextSmallestInvalidInputs:
    """Test invalid inputs that may raise exceptions."""

    def test_none_input_raises_error(self):
        with pytest.raises(TypeError):
            next_smallest(None)

    def test_integer_input_raises_error(self):
        with pytest.raises(TypeError):
            next_smallest(42)

    def test_tuple_input_returns_result(self):
        # Tuples support len(), sorted(), and iteration — so they work
        assert next_smallest((3, 1, 2)) == 2

    def test_set_input_returns_result(self):
        # Sets are iterable and support sorted()
        result = next_smallest({5, 1, 3, 2, 4})
        assert result == 2

    def test_string_input_returns_char(self):
        # Strings are iterable; sorted("hello") = ['e','h','l','l','o'] -> 'h'
        assert next_smallest("hello") == "h"

    def test_dict_input_returns_none(self):
        # Dicts iterate over keys; {1: 2} -> sorted keys = [1], len=1 -> None
        assert next_smallest({1: 2}) is None
