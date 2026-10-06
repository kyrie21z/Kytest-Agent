"""Unit tests for next_smallest() in solution.py.

The function returns the 2nd smallest *distinct* element of a list of integers,
or None when no such element exists.
"""

import pytest
from solution import next_smallest


# ── Normal cases ──────────────────────────────────────────────────────────────

class TestNormalCases:
    """Typical inputs with clear expected results."""

    def test_sorted_list(self):
        assert next_smallest([1, 2, 3, 4, 5]) == 2

    def test_unsorted_list(self):
        assert next_smallest([5, 1, 4, 3, 2]) == 2

    def test_five_elements_middle(self):
        assert next_smallest([10, 5, 8, 3, 7]) == 5

    def test_larger_list(self):
        assert next_smallest([1, 100, 50, 25, 75, 10]) == 10

    def test_three_elements(self):
        assert next_smallest([1, 3, 2]) == 2

    def test_four_elements_with_duplicates(self):
        # distinct values: 1, 2, 3 → 2nd smallest = 2
        assert next_smallest([1, 2, 2, 3]) == 2


# ── Boundary cases ────────────────────────────────────────────────────────────

class TestBoundaryCases:
    """Edges of valid input ranges."""

    def test_two_distinct_elements(self):
        assert next_smallest([1, 2]) == 2

    def test_two_elements_reversed(self):
        # sorted: [1, 2], first=1, 2nd distinct=2
        assert next_smallest([2, 1]) == 2

    def test_all_same_elements_three(self):
        assert next_smallest([7, 7, 7]) is None

    def test_all_same_elements_many(self):
        assert next_smallest([42, 42, 42, 42]) is None

    def test_negative_numbers(self):
        # sorted distinct: -5, -4, -3, -1 → 2nd smallest = -4
        assert next_smallest([-5, -3, -1, -4]) == -4

    def test_mixed_positive_and_negative(self):
        # sorted distinct: -1, 0, 2, 3, 5 → 2nd smallest = 0
        assert next_smallest([-1, 5, 3, 0, 2]) == 0

    def test_single_duplicate_pair(self):
        assert next_smallest([1, 1]) is None

    def test_large_values(self):
        assert next_smallest([10**9, 10**9 + 1, 0]) == 10**9


# ── Empty / single-element inputs ─────────────────────────────────────────────

class TestEmptyAndSingleElement:
    """Inputs that cannot produce a 2nd smallest value."""

    def test_empty_list(self):
        assert next_smallest([]) is None

    def test_single_element(self):
        assert next_smallest([42]) is None

    def test_single_zero(self):
        assert next_smallest([0]) is None


# ── Edge cases with duplicates ────────────────────────────────────────────────

class TestDuplicateEdgeCases:
    """Lists where duplicates may mask the 2nd smallest."""

    def test_first_two_same(self):
        # distinct: 1, 3, 4, 5 → 2nd smallest = 3
        assert next_smallest([1, 1, 3, 4, 5]) == 3

    def test_last_two_same(self):
        # distinct: 1, 2, 3, 4 → 2nd smallest = 2
        assert next_smallest([1, 2, 3, 4, 4]) == 2

    def test_all_but_one_same(self):
        # distinct: 1, 5 → 2nd smallest = 5
        assert next_smallest([1, 5, 1, 1, 1]) == 5

    def test_alternating_duplicates(self):
        # distinct: 2, 4, 6 → 2nd smallest = 4
        assert next_smallest([2, 4, 2, 4, 6]) == 4

    def test_three_distinct_with_many_dupes(self):
        # distinct: 10, 20, 30 → 2nd smallest = 20
        assert next_smallest([10, 20, 10, 30, 10, 20]) == 20


# ── Invalid-input handling ────────────────────────────────────────────────────

class TestInvalidInputs:
    """Behavior with inputs outside the documented contract."""

    def test_none_input_raises(self):
        with pytest.raises(TypeError):
            next_smallest(None)

    def test_string_input(self):
        # Strings are iterable and have len(). sorted("abc") → ['a','b','c'].
        # The function does NOT raise; it treats each character as an element.
        # 'a' < 'b' < 'c', so 2nd smallest char = 'b'.
        result = next_smallest("abc")
        assert result == "b"

    def test_tuple_input(self):
        # A tuple is iterable; sorted() works on it.
        result = next_smallest((1, 2, 3))
        assert result == 2

    def test_generator_input_raises(self):
        # Generators lack len(), so the function raises TypeError.
        with pytest.raises(TypeError):
            next_smallest(x for x in [5, 3, 1, 4, 2])
