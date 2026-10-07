import pytest
from solution import combinations_list


class TestCombinationsList:
    """Tests for the combinations_list function."""

    def test_empty_list(self):
        """Empty input should return a list containing only the empty combination."""
        assert combinations_list([]) == [[]]

    def test_single_element(self):
        """A single-element list should yield two combinations: empty and itself."""
        assert combinations_list([1]) == [[], [1]]

    def test_two_elements(self):
        """Two elements should produce 4 combinations."""
        result = combinations_list([1, 2])
        assert len(result) == 4
        # Elements are appended in reverse order due to how the recursion works
        assert [] in result
        assert [1] in result
        assert [2] in result
        assert [2, 1] in result

    def test_three_elements(self):
        """Three elements should produce 8 combinations."""
        result = combinations_list([1, 2, 3])
        assert len(result) == 8
        # All 2^3 subsets present; order within each subset follows the function's logic
        assert [] in result
        assert [1] in result
        assert [2] in result
        assert [3] in result
        assert [2, 1] in result
        assert [3, 1] in result
        assert [3, 2] in result
        assert [3, 2, 1] in result

    def test_four_elements(self):
        """Four elements should produce 16 combinations."""
        result = combinations_list([1, 2, 3, 4])
        assert len(result) == 16

    def test_string_elements(self):
        """Works with string elements."""
        result = combinations_list(["a", "b"])
        assert len(result) == 4
        assert [] in result
        assert ["a"] in result
        assert ["b"] in result
        assert ["b", "a"] in result

    def test_mixed_types(self):
        """Works with mixed-type elements."""
        result = combinations_list([1, "a"])
        assert len(result) == 4
        assert [] in result
        assert [1] in result
        assert ["a"] in result
        assert ["a", 1] in result

    def test_duplicate_elements(self):
        """Duplicates are treated as distinct positions; no deduplication."""
        result = combinations_list([1, 1])
        assert len(result) == 4
        # The two [1] entries come from choosing first or second element
        assert result.count([1]) == 2

    def test_negative_numbers(self):
        """Works with negative numbers."""
        result = combinations_list([-1, -2])
        assert len(result) == 4
        assert [] in result
        assert [-1] in result
        assert [-2] in result
        assert [-2, -1] in result

    def test_nested_lists(self):
        """Works when elements themselves are lists."""
        result = combinations_list([[1], [2]])
        assert len(result) == 4
        assert [] in result
        assert [[1]] in result
        assert [[2]] in result
        assert [[2], [1]] in result

    def test_returns_list(self):
        """Return type is always a list."""
        assert isinstance(combinations_list([]), list)
        assert isinstance(combinations_list([1]), list)

    def test_all_subsets_present(self):
        """Every subset of the original list appears in the result (with elements
        in the order produced by the function, which reverses relative order)."""
        original = [10, 20, 30]
        result = combinations_list(original)
        # Check every possible subset exists; the function builds them with
        # elements in reverse order, so we compare against the reversed subset.
        for mask in range(2 ** len(original)):
            subset = [original[i] for i in range(len(original)) if mask & (1 << i)]
            # The function appends elements from front to back, reversing their order
            expected = subset[::-1]
            assert expected in result

    def test_no_extra_combinations(self):
        """Result contains exactly 2^n combinations, nothing more."""
        for n in range(6):
            lst = list(range(n))
            result = combinations_list(lst)
            assert len(result) == 2 ** n

    def test_order_consistency(self):
        """Each combination preserves the relative order of chosen elements
        as they appear in the recursive construction (first element last)."""
        result = combinations_list([1, 2, 3, 4])
        # The full set should have elements in reverse order
        assert [4, 3, 2, 1] in result
