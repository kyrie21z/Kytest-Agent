import pytest
from solution import next_smallest


class TestNextSmallestNormalCases:
    """Tests for normal inputs with clear 2nd smallest element."""

    def test_basic_sorted(self):
        assert next_smallest([1, 2, 3, 4, 5]) == 2

    def test_basic_unsorted(self):
        assert next_smallest([5, 1, 4, 3, 2]) == 2

    def test_two_elements(self):
        assert next_smallest([1, 2]) == 2

    def test_two_elements_reversed(self):
        # sorted([2,1]) -> [1,2]; 2nd distinct = 2
        assert next_smallest([2, 1]) == 2

    def test_three_elements(self):
        assert next_smallest([3, 1, 2]) == 2

    def test_negative_numbers(self):
        # sorted([-5,-1,-3,-2,-4]) -> [-5,-4,-3,-2,-1]; 2nd distinct = -4
        assert next_smallest([-5, -1, -3, -2, -4]) == -4

    def test_mixed_positive_negative(self):
        # sorted([-1,0,1,2,3]) -> [-1,0,1,2,3]; 2nd distinct = 0
        assert next_smallest([-1, 0, 1, 2, 3]) == 0

    def test_larger_list(self):
        assert next_smallest([10, 20, 30, 40, 50, 60, 70]) == 20

    def test_duplicates_in_middle(self):
        # sorted([1,5,5,5,2]) -> [1,2,5,5,5]; 2nd distinct = 2
        assert next_smallest([1, 5, 5, 5, 2]) == 2

    def test_duplicates_at_start(self):
        # sorted([1,1,2,3,4]) -> [1,1,2,3,4]; 2nd distinct = 2
        assert next_smallest([1, 1, 2, 3, 4]) == 2

    def test_duplicates_at_end(self):
        # sorted([1,2,3,4,4]) -> [1,2,3,4,4]; 2nd distinct = 2
        assert next_smallest([1, 2, 3, 4, 4]) == 2

    def test_all_same_except_one(self):
        # sorted([5,5,5,5,1]) -> [1,5,5,5,5]; 2nd distinct = 5
        assert next_smallest([5, 5, 5, 5, 1]) == 5

    def test_single_duplicate_pair(self):
        # sorted([3,3,1,1,2,2]) -> [1,1,2,2,3,3]; 2nd distinct = 2
        assert next_smallest([3, 3, 1, 1, 2, 2]) == 2


class TestNextSmallestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_empty_list(self):
        assert next_smallest([]) is None

    def test_single_element(self):
        assert next_smallest([42]) is None

    def test_two_identical_elements(self):
        assert next_smallest([7, 7]) is None

    def test_all_identical_elements(self):
        assert next_smallest([3, 3, 3, 3, 3]) is None

    def test_only_two_distinct_values(self):
        # sorted([1,1,2,2]) -> [1,1,2,2]; 2nd distinct = 2
        assert next_smallest([1, 1, 2, 2]) == 2

    def test_min_integer_value(self):
        assert next_smallest([0, 1]) == 1

    def test_large_range_with_2nd_smallest_near_bottom(self):
        lst = [1000000] + list(range(1, 100))
        # sorted: [1, 2, 3, ..., 99, 1000000]; 2nd distinct = 2
        assert next_smallest(lst) == 2

    def test_large_range_with_2nd_smallest_near_top(self):
        lst = list(range(1, 100)) + [1000000]
        # sorted: [1, 2, 3, ..., 99, 1000000]; 2nd distinct = 2
        assert next_smallest(lst) == 2


class TestNextSmallestEdgeValues:
    """Tests involving edge numeric values."""

    def test_zero_and_positive(self):
        assert next_smallest([0, 1, 2, 3]) == 1

    def test_zero_as_2nd_smallest(self):
        # sorted([-1,0,1,2]) -> [-1,0,1,2]; 2nd distinct = 0
        assert next_smallest([-1, 0, 1, 2]) == 0

    def test_all_negative(self):
        # sorted([-10,-5,-3,-1]) -> [-10,-5,-3,-1]; 2nd distinct = -5
        assert next_smallest([-10, -5, -3, -1]) == -5

    def test_two_negative(self):
        # sorted([-3,-1]) -> [-3,-1]; 2nd distinct = -1
        assert next_smallest([-3, -1]) == -1

    def test_negative_duplicates(self):
        # sorted([-2,-2,-1,-1]) -> [-2,-2,-1,-1]; 2nd distinct = -1
        assert next_smallest([-2, -2, -1, -1]) == -1

    def test_zero_duplicates(self):
        # sorted([0,0,1,2]) -> [0,0,1,2]; 2nd distinct = 1
        assert next_smallest([0, 0, 1, 2]) == 1

    def test_many_zeros(self):
        # sorted([0,0,0,0,1]) -> [0,0,0,0,1]; 2nd distinct = 1
        assert next_smallest([0, 0, 0, 0, 1]) == 1


class TestNextSmallestInvalidInputs:
    """Tests for invalid or unexpected input types."""

    def test_none_input(self):
        with pytest.raises(TypeError):
            next_smallest(None)

    def test_string_input(self):
        # Strings are iterable; sorted("abc") -> ['a','b','c']; returns 'b'
        result = next_smallest("abc")
        assert result == 'b'

    def test_tuple_input(self):
        # Tuples are iterable; len() and sorted() work
        result = next_smallest((1, 2, 3))
        assert result == 2

    def test_set_input(self):
        # Sets are iterable
        result = next_smallest({3, 1, 2})
        assert result == 2

    def test_dict_input(self):
        # Dicts iterate over keys (ints); sorted({1,2}) -> [1,2]; returns 2
        result = next_smallest({1: 'a', 2: 'b'})
        assert result == 2

    def test_nested_list(self):
        # Python 3 can compare lists element-wise: [1] < [2] is True
        # sorted([[1],[2]]) -> [[1],[2]]; returns [2]
        result = next_smallest([[1], [2]])
        assert result == [2]

    def test_float_values(self):
        result = next_smallest([1.5, 2.5, 3.5])
        assert result == 2.5

    def test_mixed_int_float(self):
        result = next_smallest([1, 2.5, 3])
        assert result == 2.5


class TestNextSmallestLargeLists:
    """Tests with larger lists to ensure correctness scales."""

    def test_100_elements(self):
        lst = list(range(1, 101))
        assert next_smallest(lst) == 2

    def test_100_elements_reverse(self):
        lst = list(range(100, 0, -1))
        assert next_smallest(lst) == 2

    def test_1000_elements(self):
        lst = list(range(1, 1001))
        assert next_smallest(lst) == 2

    def test_large_list_with_duplicates(self):
        lst = [1] * 500 + [2] * 500
        assert next_smallest(lst) == 2

    def test_large_list_all_unique(self):
        # range(-500, 500) -> -500, -499, ..., 499
        # sorted: [-500, -499, ...]; 2nd distinct = -499
        lst = list(range(-500, 500))
        assert next_smallest(lst) == -499
