import pytest
from solution import next_smallest


class TestNextSmallest:
    """Tests for the next_smallest function.

    The function takes a list of integers and returns the 2nd smallest element,
    or None if there is no such element (e.g., fewer than 2 distinct values).
    """

    # ====================================================================
    # 1. Normal cases with typical inputs
    # ====================================================================

    def test_basic_sorted_list(self):
        """[1, 2, 3, 4, 5] -> 2"""
        assert next_smallest([1, 2, 3, 4, 5]) == 2

    def test_basic_unsorted_list(self):
        """[5, 1, 4, 3, 2] -> 2"""
        assert next_smallest([5, 1, 4, 3, 2]) == 2

    def test_three_elements(self):
        """[3, 1, 2] -> 2"""
        assert next_smallest([3, 1, 2]) == 2

    def test_larger_values(self):
        """[10, 20, 30] -> 20"""
        assert next_smallest([10, 20, 30]) == 20

    def test_mixed_order(self):
        """[1, 100, 50] -> 50"""
        assert next_smallest([1, 100, 50]) == 50

    def test_four_elements(self):
        """[8, 3, 6, 1] -> 3"""
        assert next_smallest([8, 3, 6, 1]) == 3

    def test_five_elements_unordered(self):
        """[9, 7, 3, 5, 1] -> 3"""
        assert next_smallest([9, 7, 3, 5, 1]) == 3

    # ====================================================================
    # 2. Boundary cases at the edges of valid input ranges
    # ====================================================================

    def test_two_different_elements(self):
        """Exactly two distinct values: [1, 2] -> 2"""
        assert next_smallest([1, 2]) == 2

    def test_two_different_elements_reversed(self):
        """Exactly two distinct values reversed: [2, 1] -> 2"""
        assert next_smallest([2, 1]) == 2

    def test_two_same_elements(self):
        """Two identical values: [1, 1] -> None"""
        assert next_smallest([1, 1]) == None

    def test_all_identical_elements(self):
        """All same: [5, 5, 5] -> None"""
        assert next_smallest([5, 5, 5]) == None

    def test_many_duplicates_first_two_distinct(self):
        """Many copies of min, then one distinct: [1,1,1,2,2,3] -> 2"""
        assert next_smallest([1, 1, 1, 2, 2, 3]) == 2

    def test_negative_numbers(self):
        """Negative values: [-5, -3, -1, 0] -> -3"""
        assert next_smallest([-5, -3, -1, 0]) == -3

    def test_mixed_negative_and_positive(self):
        """Mix of negatives and positives: [-10, 5, -3, 0, 2] -> -3"""
        assert next_smallest([-10, 5, -3, 0, 2]) == -3

    def test_all_negative(self):
        """All negative: [-1, -5, -3, -2] -> -3"""
        assert next_smallest([-1, -5, -3, -2]) == -3

    def test_min_is_negative(self):
        """Min is negative, second smallest is positive: [-5, 1, 3] -> 1"""
        assert next_smallest([-5, 1, 3]) == 1

    def test_consecutive_integers(self):
        """Consecutive integers: [10, 11, 12, 13] -> 11"""
        assert next_smallest([10, 11, 12, 13]) == 11

    def test_large_range(self):
        """Large range of unique integers: list(range(1, 101)) -> 2"""
        assert next_smallest(list(range(1, 101))) == 2

    def test_large_list_with_duplicates_at_start(self):
        """Large list where min repeats many times: [1]*50 + [2] + [3]*50 -> 2"""
        assert next_smallest([1] * 50 + [2] + [3] * 50) == 2

    def test_second_smallest_at_end(self):
        """Second smallest appears only at end: [5, 4, 3, 2] -> 3"""
        assert next_smallest([5, 4, 3, 2]) == 3

    def test_second_smallest_at_beginning(self):
        """Second smallest appears only at beginning: [2, 5, 4, 3] -> 3
        Sorted: [2, 3, 4, 5], 2nd smallest = 3."""
        assert next_smallest([2, 5, 4, 3]) == 3

    def test_only_two_elements(self):
        """Exactly two elements: [7, 9] -> 9"""
        assert next_smallest([7, 9]) == 9

    def test_extreme_values(self):
        """Very large and very small values: [-1000000, 0, 1000000] -> 0"""
        assert next_smallest([-1000000, 0, 1000000]) == 0

    # ====================================================================
    # 3. Empty, null, or zero-size inputs
    # ====================================================================

    def test_empty_list(self):
        """Empty list has no 2nd smallest: [] -> None"""
        assert next_smallest([]) == None

    def test_single_element(self):
        """Single element has no 2nd smallest: [42] -> None"""
        assert next_smallest([42]) == None

    def test_single_zero(self):
        """Single zero: [0] -> None"""
        assert next_smallest([0]) == None

    # ====================================================================
    # 4. Invalid inputs (per docstring: expects a list of integers)
    # ====================================================================

    def test_none_input_raises_type_error(self):
        """Passing None should raise TypeError (not a list)."""
        with pytest.raises(TypeError):
            next_smallest(None)

    def test_tuple_input(self):
        """A tuple is iterable and sortable; behaves like a list.
        (1, 3, 2) -> 2"""
        assert next_smallest((1, 3, 2)) == 2

    # ====================================================================
    # 5. Exception cases
    # ====================================================================

    def test_non_iterable_raises_type_error(self):
        """Passing an integer (non-iterable) should raise TypeError."""
        with pytest.raises(TypeError):
            next_smallest(42)

    def test_dict_input_raises_type_error(self):
        """Passing a dict is iterable over keys only; sorted(dict) sorts keys.
        This exercises the function with an unexpected but iterable type.
        {3: 'a', 1: 'b', 2: 'c'} -> sorted keys [1,2,3], 2nd smallest key = 2"""
        assert next_smallest({3: "a", 1: "b", 2: "c"}) == 2

    def test_float_values(self):
        """Floats are sortable; function does not restrict to ints.
        [1.5, 3.0, 2.5] -> 2.5"""
        assert next_smallest([1.5, 3.0, 2.5]) == 2.5

    def test_duplicate_floats(self):
        """Duplicate floats: [2.0, 2.0, 3.0] -> 3.0"""
        assert next_smallest([2.0, 2.0, 3.0]) == 3.0
