"""Unit tests for minPath(grid, k) in solution.py."""

import pytest
from solution import minPath


class TestMinPathNormalCases:
    """Tests covering normal, typical inputs as described in the docstring."""

    def test_example_1(self):
        """Example 1 from docstring: 3x3 grid, k=3."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_example_2(self):
        """Example 2 from docstring: 3x3 grid, k=1."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]

    def test_k_equals_2(self):
        """Path of length 2: [1, smallest_neighbor_of_1]."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # 1 is at (0,0); neighbors: 2(right), 4(down); min neighbor = 2
        assert minPath(grid, 2) == [1, 2]

    def test_k_equals_4_even(self):
        """Path of length 4: [1, mn, 1, mn]."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_k_equals_5_odd(self):
        """Path of length 5: [1, mn, 1, mn, 1]."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_1_not_at_corner(self):
        """1 is in the middle; all four neighbors exist."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        # 1 is at (1,1); neighbors: 9(up), 6(right), 8(down), 4(left); min=4
        assert minPath(grid, 3) == [1, 4, 1]

    def test_1_at_top_left(self):
        """1 at top-left corner; two neighbors."""
        grid = [[1, 3], [2, 4]]
        # 1 at (0,0); neighbors: 3(right), 2(down); min=2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_1_at_bottom_right(self):
        """1 at bottom-right corner; two neighbors."""
        grid = [[4, 3], [2, 1]]
        # 1 at (1,1); neighbors: 3(up), 2(left); min=2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_at_top_right(self):
        """1 at top-right corner; two neighbors (down and left)."""
        grid = [[3, 1], [2, 4]]
        # 1 at (0,1); valid neighbors: down=grid[1][1]=4, left=grid[0][0]=3
        # Function checks in order: up(skip), down(4), left(3), right(skip)
        # mn = min(4, 4, 3) = 3
        assert minPath(grid, 2) == [1, 3]

    def test_1_at_bottom_left(self):
        """1 at bottom-left corner; two neighbors."""
        grid = [[4, 3], [1, 2]]
        # 1 at (1,0); neighbors: 4(up), 2(right); min=2
        assert minPath(grid, 6) == [1, 2, 1, 2, 1, 2]

    def test_larger_grid_4x4(self):
        """4x4 grid with 1 somewhere inside."""
        grid = [
            [16, 15, 14, 13],
            [11, 10, 9, 12],
            [6, 7, 8, 5],
            [1, 2, 3, 4],
        ]
        # 1 at (3,0); neighbors: 6(up), 2(right); min=2
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_min_neighbor_is_large(self):
        """Smallest neighbor of 1 is relatively large."""
        grid = [[10, 1], [2, 3]]
        # 1 at (0,1); neighbors: down=grid[1][1]=3, left=grid[0][0]=10
        # mn = min(4, 3, 10) = 3
        assert minPath(grid, 3) == [1, 3, 1]


class TestMinPathBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_minimum_k(self):
        """Minimum valid k=1."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 1) == [1]

    def test_minimum_n(self):
        """Minimum grid size N=2."""
        grid = [[1, 2], [3, 4]]
        # 1 at (0,0); neighbors: 2(right), 3(down); min=2
        assert minPath(grid, 2) == [1, 2]

    def test_maximum_k_for_small_grid(self):
        """Large k relative to grid size."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 100) == [1, 2] * 50

    def test_k_one_less_than_twice_mn(self):
        """Verify exact alternation pattern at boundary."""
        grid = [[1, 5], [3, 4]]
        # 1 at (0,0); neighbors: down=3, right=5; min=3
        assert minPath(grid, 7) == [1, 3, 1, 3, 1, 3, 1]

    def test_k_exactly_double(self):
        """Even k that is exactly double some value."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 6) == [1, 2, 1, 2, 1, 2]

    def test_k_exactly_triple(self):
        """Odd k that is triple."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 3) == [1, 2, 1]


class TestMinPathEdgeCases:
    """Tests for empty, zero-size, or unusual inputs."""

    def test_k_zero(self):
        """k=0 should return empty list (no cells visited)."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 0) == []

    def test_k_negative(self):
        """Negative k: range(negative) is empty, returns []."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, -1) == []

    def test_k_very_large(self):
        """Very large k still produces correct alternating pattern."""
        grid = [[1, 2], [3, 4]]
        expected = [1, 2] * 500
        assert minPath(grid, 1000) == expected

    def test_1_has_only_one_neighbor(self):
        """Grid where 1 truly has only one neighbor (shouldn't happen for N>=2,
        but verify behavior when 1 is at a position with minimal neighbors)."""
        # In a 2x2 grid, every cell has exactly 2 neighbors, so this tests
        # the corner case logic.
        grid = [[1, 2], [3, 4]]
        assert len(minPath(grid, 1)) == 1
        assert minPath(grid, 1)[0] == 1


class TestMinPathInvalidInputs:
    """Tests for inputs that violate documented constraints."""

    def test_non_positive_k_type_error(self):
        """k=0 is technically not a 'positive integer' per docstring."""
        grid = [[1, 2], [3, 4]]
        # Function doesn't raise, but returns [] for k=0
        result = minPath(grid, 0)
        assert result == []

    def test_empty_grid(self):
        """Empty grid: N=0, loops don't run, x=0,y=0 stays, no neighbor checks pass.
        mn stays at N*N=0. Return uses hardcoded 1 at even indices.
        Returns [1] for k=1."""
        grid = []
        assert minPath(grid, 1) == [1]

    def test_single_row_grid(self):
        """Non-square grid (single row) — violates N>=2 square constraint.
        N=1, loop finds 1 at (0,0), no neighbors exist, mn stays 1.
        Returns [1, 1, ...] since mn=1."""
        grid = [[1, 2, 3]]
        assert minPath(grid, 3) == [1, 1, 1]

    def test_single_column_grid(self):
        """Non-square grid (single column) — violates square constraint.
        Function assumes N rows and N columns, so accessing grid[i][j]
        where j >= 1 raises IndexError."""
        grid = [[1], [2], [3]]
        with pytest.raises(IndexError):
            minPath(grid, 3)

    def test_grid_with_duplicate_values(self):
        """Grid with duplicate values — violates uniqueness constraint.
        Function will find the FIRST occurrence of 1."""
        grid = [[1, 1], [2, 3]]
        # First 1 found at (0,0); neighbors: right=1, down=2; min=1
        assert minPath(grid, 3) == [1, 1, 1]

    def test_grid_with_value_out_of_range(self):
        """Grid with values outside [1, N*N]. Function still works.
        No 1 found, so x=0,y=0 stays. Return uses hardcoded 1 at even indices.
        mn computed from neighbors of (0,0): grid[1][0]=3, grid[0][1]=2 → mn=2."""
        grid = [[0, 2], [3, 4]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_none_as_grid(self):
        """Passing None as grid should raise an error."""
        with pytest.raises(TypeError):
            minPath(None, 1)

    def test_none_as_k(self):
        """Passing None as k should raise an error."""
        grid = [[1, 2], [3, 4]]
        with pytest.raises(TypeError):
            minPath(grid, None)

    def test_string_as_k(self):
        """Passing a string as k should raise TypeError."""
        grid = [[1, 2], [3, 4]]
        with pytest.raises(TypeError):
            minPath(grid, "3")

    def test_list_as_k(self):
        """Passing a list as k should raise TypeError."""
        grid = [[1, 2], [3, 4]]
        with pytest.raises(TypeError):
            minPath(grid, [3])


class TestMinPathPatternCorrectness:
    """Tests verifying the alternating pattern [1, mn, 1, mn, ...]."""

    def test_pattern_length_matches_k(self):
        """Output length always equals k."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for k in range(1, 20):
            result = minPath(grid, k)
            assert len(result) == k

    def test_alternating_pattern_odd_k(self):
        """For odd k, last element is always 1."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for k in range(1, 20, 2):
            result = minPath(grid, k)
            assert result[-1] == 1

    def test_alternating_pattern_even_k(self):
        """For even k, last element is always the min neighbor."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for k in range(2, 20, 2):
            result = minPath(grid, k)
            assert result[-1] == 2  # mn = 2

    def test_all_even_indices_are_1(self):
        """All elements at even indices (0-based) are 1."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = minPath(grid, 10)
        for i in range(0, 10, 2):
            assert result[i] == 1

    def test_all_odd_indices_are_mn(self):
        """All elements at odd indices (0-based) are the min neighbor."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = minPath(grid, 10)
        for i in range(1, 10, 2):
            assert result[i] == 2  # mn = 2

    def test_different_grids_same_pattern_structure(self):
        """Different grids produce same structural pattern, different mn."""
        grid_a = [[1, 5], [3, 4]]  # mn = 3
        grid_b = [[1, 10], [3, 4]]  # mn = 3
        grid_c = [[1, 2], [3, 4]]  # mn = 2

        assert minPath(grid_a, 4) == [1, 3, 1, 3]
        assert minPath(grid_b, 4) == [1, 3, 1, 3]
        assert minPath(grid_c, 4) == [1, 2, 1, 2]
