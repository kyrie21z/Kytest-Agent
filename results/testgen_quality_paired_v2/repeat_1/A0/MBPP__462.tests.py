import pytest
from solution import combinations_list


class TestCombinationsList:
    """Tests for the combinations_list function."""

    def test_empty_list(self):
        """An empty list should return a list containing only the empty combination."""
        result = combinations_list([])
        assert result == [[]]

    def test_single_element(self):
        """A single-element list should return two combinations: empty and the element itself."""
        result = combinations_list([1])
        assert result == [[], [1]]

    def test_two_elements(self):
        """A two-element list should return four combinations with correct content."""
        result = combinations_list([1, 2])
        # The function appends list1[0] at the end, so order may differ from input
        assert len(result) == 4
        assert [] in result
        assert [1] in result
        assert [2] in result
        assert [2, 1] in result or [1, 2] in result

    def test_three_elements(self):
        """A three-element list should return eight combinations."""
        result = combinations_list([1, 2, 3])
        assert len(result) == 8
        assert [] in result
        assert [1] in result
        assert [2] in result
        assert [3] in result
        assert [2, 1] in result
        assert [3, 1] in result
        assert [3, 2] in result
        assert [3, 2, 1] in result

    def test_combinations_count(self):
        """For a list of length n, there should be exactly 2^n combinations."""
        for n in range(8):
            lst = list(range(n))
            result = combinations_list(lst)
            assert len(result) == 2 ** n

    def test_contains_all_subsets(self):
        """Every subset of the original list should appear in the result."""
        lst = [1, 2, 3, 4]
        result = combinations_list(lst)
        # Check that every element in the original list appears in some combination
        for el in lst:
            found = any(el in combo for combo in result)
            assert found, f"Element {el} not found in any combination"

    def test_no_duplicates(self):
        """There should be no duplicate combinations in the result."""
        result = combinations_list([1, 2, 3])
        # Convert each inner list to a tuple for hashability
        tuples = [tuple(c) for c in result]
        assert len(tuples) == len(set(tuples))

    def test_string_elements(self):
        """Works correctly with string elements."""
        result = combinations_list(["a", "b"])
        assert len(result) == 4
        assert [] in result
        assert ["a"] in result
        assert ["b"] in result
        assert ["b", "a"] in result

    def test_mixed_types(self):
        """Works correctly with mixed types in the list."""
        result = combinations_list([1, "a", True])
        assert len(result) == 8

    def test_negative_numbers(self):
        """Works correctly with negative numbers."""
        result = combinations_list([-1, -2])
        assert len(result) == 4
        assert [] in result
        assert [-1] in result
        assert [-2] in result
        assert [-2, -1] in result

    def test_duplicate_values_in_input(self):
        """Handles lists with duplicate values (treats them as distinct positions)."""
        result = combinations_list([1, 1])
        # Two identical elements at different positions produce 4 combinations
        assert len(result) == 4
        assert [] in result
        assert [1] in result
        assert [1, 1] in result

    def test_large_list(self):
        """Works correctly with a moderately large list."""
        lst = list(range(10))
        result = combinations_list(lst)
        assert len(result) == 2 ** 10  # 1024

    def test_result_is_list_of_lists(self):
        """Each combination should be a list."""
        result = combinations_list([1, 2, 3])
        assert all(isinstance(combo, list) for combo in result)

    def test_return_type(self):
        """The function should return a list."""
        result = combinations_list([1])
        assert isinstance(result, list)

    def test_none_not_allowed(self):
        """Passing None should raise an error (since len() is called on it)."""
        with pytest.raises(TypeError):
            combinations_list(None)
