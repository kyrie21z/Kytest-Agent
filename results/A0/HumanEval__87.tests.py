import pytest
from solution import get_row


class TestGetRow:
    """Unit tests for the get_row function."""

    # --- Examples from docstring ---

    def test_docstring_example_1(self):
        lst = [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 1, 6],
            [1, 2, 3, 4, 5, 1],
        ]
        assert get_row(lst, 1) == [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]

    def test_docstring_example_2(self):
        assert get_row([], 1) == []

    def test_docstring_example_3(self):
        assert get_row([[], [1], [1, 2, 3]], 3) == [(2, 2)]

    # --- Empty / edge cases ---

    def test_empty_list(self):
        assert get_row([], 5) == []

    def test_list_with_empty_rows(self):
        assert get_row([[], [], []], 1) == []

    def test_single_empty_row(self):
        assert get_row([[]], 1) == []

    def test_no_match(self):
        assert get_row([[1, 2, 3], [4, 5, 6]], 99) == []

    def test_value_not_present_in_any_row(self):
        assert get_row([[1, 2], [3, 4]], 0) == []

    # --- Single element searches ---

    def test_single_occurrence(self):
        assert get_row([[5]], 5) == [(0, 0)]

    def test_single_occurrence_not_first(self):
        assert get_row([[1, 2, 5, 4]], 5) == [(0, 2)]

    def test_single_row_multiple_values(self):
        assert get_row([[3, 1, 3, 2, 3]], 3) == [(0, 4), (0, 2), (0, 0)]

    # --- Sorting behavior ---

    def test_sort_by_row_ascending(self):
        """Coordinates should be ordered by row index in ascending order."""
        lst = [[1, 2, 3], [4, 1, 6]]
        # row 0: 1 is at index 0; row 1: 1 is at index 1
        assert get_row(lst, 1) == [(0, 0), (1, 1)]

    def test_sort_by_column_descending_within_row(self):
        """Within the same row, columns should be in descending order."""
        lst = [[1, 2, 1, 3, 1]]
        assert get_row(lst, 1) == [(0, 4), (0, 2), (0, 0)]

    def test_mixed_rows_with_same_value(self):
        """Multiple rows with value; rows ascending, cols descending."""
        lst = [
            [1, 2, 1],
            [1, 1, 1],
            [2, 1],
        ]
        # row 0: 1 at cols 2, 0; row 1: 1 at cols 2, 1, 0; row 2: 1 at col 1
        result = get_row(lst, 1)
        assert result == [(0, 2), (0, 0), (1, 2), (1, 1), (1, 0), (2, 1)]

    # --- Jagged / irregular rows ---

    def test_jagged_rows(self):
        """Each row can have a different number of columns."""
        lst = [
            [1, 2, 3, 4, 5],
            [1, 2],
            [1, 2, 3],
        ]
        assert get_row(lst, 1) == [(0, 0), (1, 0), (2, 0)]

    def test_jagged_rows_with_later_matches(self):
        lst = [
            [10, 20, 30],
            [1, 2, 3, 4, 5],
            [6, 7],
        ]
        assert get_row(lst, 3) == [(1, 2)]

    # --- Negative numbers and zero ---

    def test_negative_target(self):
        # row 0: [-1, -2, -1] -> -1 at cols 2, 0; row 1: [0, -1] -> -1 at col 1
        assert get_row([[-1, -2, -1], [0, -1]], -1) == [(0, 2), (0, 0), (1, 1)]

    def test_zero_target(self):
        assert get_row([[0, 1, 0], [2, 0]], 0) == [(0, 2), (0, 0), (1, 1)]

    # --- Large values ---

    def test_large_integer(self):
        assert get_row([[10**9, 10**9]], 10**9) == [(0, 1), (0, 0)]

    # --- Return type checks ---

    def test_returns_list_of_tuples(self):
        result = get_row([[1, 2, 1]], 1)
        assert isinstance(result, list)
        assert all(isinstance(t, tuple) and len(t) == 2 for t in result)

    def test_returns_empty_list_when_no_match(self):
        result = get_row([[1, 2, 3]], 99)
        assert isinstance(result, list)
        assert result == []

    # --- Comprehensive mixed test ---

    def test_comprehensive(self):
        lst = [
            [5, 3, 5, 1],
            [2, 5],
            [5, 5, 5],
            [8, 9],
        ]
        result = get_row(lst, 5)
        expected = [
            (0, 2), (0, 0),   # row 0: cols 2, 0 (descending)
            (1, 1),           # row 1: col 1
            (2, 2), (2, 1), (2, 0),  # row 2: cols 2, 1, 0 (descending)
        ]
        assert result == expected
