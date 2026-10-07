import pytest
from solution import combinations_list


class TestCombinationsList:
    """Tests for the combinations_list function."""

    def test_empty_list(self):
        """Empty input should return a list containing only the empty combination."""
        assert combinations_list([]) == [[]]

    def test_single_element(self):
        """A single-element list should yield two combinations: empty and itself."""
        result = combinations_list([1])
        assert result == [[], [1]]

    def test_two_elements(self):
        """Two elements should produce 4 combinations."""
        result = combinations_list([1, 2])
        assert len(result) == 4
        # The function prepends elements, so order within combos is reversed
        assert [] in result
        assert [1] in result
        assert [2] in result
        assert [2, 1] in result

    def test_three_elements(self):
        """Three elements should produce 8 combinations."""
        result = combinations_list([1, 2, 3])
        assert len(result) == 8
        # Verify all expected combinations are present (order may vary)
        expected_sets = [
            set(),
            {1},
            {2},
            {3},
            {1, 2},
            {1, 3},
            {2, 3},
            {1, 2, 3},
        ]
        result_sets = [set(c) for c in result]
        for exp in expected_sets:
            assert exp in result_sets

    def test_four_elements(self):
        """Four elements should produce 16 combinations."""
        result = combinations_list([1, 2, 3, 4])
        assert len(result) == 16

    def test_string_elements(self):
        """Function should work with string elements."""
        result = combinations_list(["a", "b"])
        assert len(result) == 4
        assert ["a"] in result
        assert ["b"] in result
        assert ["b", "a"] in result
        assert [] in result

    def test_mixed_types(self):
        """Function should handle lists with mixed element types."""
        result = combinations_list([1, "a", True])
        assert len(result) == 8

    def test_duplicate_elements(self):
        """Duplicates are treated as distinct items by position."""
        result = combinations_list([1, 1])
        assert len(result) == 4
        assert [1] in result
        assert [1, 1] in result

    def test_negative_numbers(self):
        """Function should handle negative numbers correctly."""
        result = combinations_list([-1, -2])
        assert len(result) == 4
        assert [-2, -1] in result

    def test_nested_lists(self):
        """Function should handle nested lists as elements."""
        result = combinations_list([[1], [2]])
        assert len(result) == 4
        assert [[2], [1]] in result

    def test_large_list(self):
        """Larger lists should still complete in reasonable time."""
        data = list(range(10))
        result = combinations_list(data)
        assert len(result) == 2 ** 10  # 1024

    def test_return_type(self):
        """Result should always be a list."""
        assert isinstance(combinations_list([]), list)
        assert isinstance(combinations_list([1]), list)

    def test_each_combination_is_a_list(self):
        """Every item in the result should itself be a list."""
        result = combinations_list([1, 2, 3])
        for combo in result:
            assert isinstance(combo, list)

    def test_no_duplicates_in_result(self):
        """Each unique combination should appear exactly once."""
        result = combinations_list([1, 2, 3])
        # Convert each inner list to a tuple for hashable comparison
        tuples = [tuple(c) for c in result]
        assert len(tuples) == len(set(tuples))

    def test_all_subsets_present(self):
        """Every subset of the input must be present in the result."""
        from itertools import combinations

        data = [1, 2, 3, 4]
        result = combinations_list(data)
        result_sets = {frozenset(c) for c in result}

        for r in range(len(data) + 1):
            for combo in combinations(data, r):
                assert frozenset(combo) in result_sets

    def test_consistent_with_power_set_size(self):
        """For any list of length n, the result should have 2^n combinations."""
        for n in range(11):
            data = list(range(n))
            result = combinations_list(data)
            assert len(result) == 2 ** n
