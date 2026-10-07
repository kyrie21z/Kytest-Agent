"""
Unit tests for solution.minPath(grid, k).

Function behavior (from docstring):
  - Input: an N×N grid (N >= 2) containing a permutation of [1, N*N],
           and a positive integer k.
  - Algorithm: locate the cell with value 1, find the minimum value among
               its orthogonal neighbors, then return a path of length k
               alternating [1, mn, 1, mn, ...].
  - Output: list of length k.
"""

import pytest
from solution import minPath


# ──────────────────────────────────────────────
# 1. Normal / typical cases
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with typical, well-formed inputs."""

    def test_example_1_from_docstring(self):
        """grid = [[1,2,3],[4,5,6],[7,8,9]], k = 3 → [1, 2, 1]"""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_example_2_from_docstring(self):
        """grid = [[5,9,3],[4,1,6],[7,8,2]], k = 1 → [1]"""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]

    def test_k_even_path(self):
        """Even k produces [1, mn, 1, mn, ..., 1, mn]."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # 1 at (0,0), neighbors: 2(right), 4(down) → mn = 2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_k_large(self):
        """Large k still alternates correctly."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        expected = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        assert minPath(grid, 10) == expected

    def test_1_at_center(self):
        """Value 1 in the middle of a 3×3 grid."""
        grid = [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
        # 1 at (0,2), neighbors: 2(left), 4(down) → mn = 2
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_1_on_edge_not_corner(self):
        """Value 1 on an edge (not a corner) of a 3×3 grid."""
        grid = [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
        # Same as above — 1 is at (0,2), top-right edge
        assert minPath(grid, 2) == [1, 2]

    def test_1_at_bottom_right_corner(self):
        """Value 1 at bottom-right corner."""
        grid = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
        # 1 at (2,2), neighbors: 4(up), 2(left) → mn = 2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_at_top_left_corner(self):
        """Value 1 at top-left corner."""
        grid = [[1, 9, 8], [2, 7, 6], [3, 5, 4]]
        # 1 at (0,0), neighbors: 9(right), 2(down) → mn = 2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_minimum_neighbor_is_larger_value(self):
        """When all neighbors of 1 have large values."""
        grid = [[1, 100], [99, 98]]
        # 1 at (0,0), neighbors: 100(right), 99(down) → mn = 99
        assert minPath(grid, 3) == [1, 99, 1]

    def test_all_neighbors_equal(self):
        """Grid where two neighbors of 1 have the same minimum."""
        grid = [[1, 5, 6], [5, 4, 3], [2, 7, 8]]
        # 1 at (0,0), neighbors: 5(right), 5(down) → mn = 5
        assert minPath(grid, 2) == [1, 5]


# ──────────────────────────────────────────────
# 2. Boundary cases
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_min_grid_size_N2(self):
        """Minimum allowed grid size: 2×2."""
        grid = [[1, 2], [3, 4]]
        # 1 at (0,0), neighbors: 2(right), 3(down) → mn = 2
        assert minPath(grid, 1) == [1]

    def test_min_grid_size_N2_k2(self):
        """2×2 grid with k=2."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 2) == [1, 2]

    def test_min_grid_size_N2_k3(self):
        """2×2 grid with k=3."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_min_grid_size_N2_k4(self):
        """2×2 grid with k=4."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_min_grid_size_1_at_different_positions(self):
        """Test every position of 1 in a 2×2 grid."""
        # 1 at (0,1)
        grid = [[2, 1], [4, 3]]
        # neighbors: 2(left), 3(down) → mn = 2
        assert minPath(grid, 3) == [1, 2, 1]

        # 1 at (1,0)
        grid = [[3, 2], [1, 4]]
        # neighbors: 2(up), 4(right) → mn = 2
        assert minPath(grid, 3) == [1, 2, 1]

        # 1 at (1,1)
        grid = [[3, 2], [4, 1]]
        # neighbors: 4(left), 2(up) → mn = 2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_k_equals_1(self):
        """Smallest valid k; always returns [1]."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]

    def test_output_length_equals_k(self):
        """Output list length must equal k for various k values."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for k in range(1, 21):
            result = minPath(grid, k)
            assert len(result) == k

    def test_alternating_pattern_correct(self):
        """Every even index is 1, odd index is mn."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = minPath(grid, 15)
        for i in range(15):
            if i % 2 == 0:
                assert result[i] == 1
            else:
                assert result[i] == 2

    def test_large_grid(self):
        """A larger grid (5×5) with 1 somewhere inside."""
        grid = [
            [25, 24, 23, 22, 21],
            [20, 19, 18, 17, 16],
            [15, 14, 13, 12, 11],
            [10, 9,  8,  7,  6],
            [5,  4,  3,  2,  1],
        ]
        # 1 at (4,4), neighbors: 6(up), 2(left) → mn = 2
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]


# ──────────────────────────────────────────────
# 3. Edge cases: empty, null, zero-size inputs
# ──────────────────────────────────────────────

class TestEdgeCases:
    """Tests with unusual but possibly valid edge-case inputs."""

    def test_k_zero(self):
        """k=0 is not a positive integer per docstring, but test behavior."""
        grid = [[1, 2], [3, 4]]
        # Function will produce [] because range(0) is empty
        assert minPath(grid, 0) == []

    def test_single_cell_grid_not_allowed(self):
        """N < 2 violates the documented constraint N >= 2.
           This is technically invalid input; behavior is undefined.
           We test it anyway to document actual behavior."""
        # A 1×1 grid: only one cell, no neighbors.
        # The function finds 1 at (0,0), then checks bounds —
        # all neighbor checks fail (x>0, x<N-1, y>0, y<N-1 all false),
        # so mn stays at N*N = 1. Returns [1]*k.
        grid = [[1]]
        assert minPath(grid, 3) == [1, 1, 1]

    def test_none_grid_raises(self):
        """Passing None as grid should raise an error."""
        with pytest.raises(TypeError):
            minPath(None, 3)

    def test_empty_list_grid(self):
        """An empty list as grid should cause an error."""
        with pytest.raises(IndexError):
            minPath([], 3)

    def test_non_square_grid(self):
        """Non-square grid: function doesn't validate this explicitly.
           It uses len(grid) for N and iterates grid[i][j].
           If rows have different lengths, IndexError may occur."""
        grid = [[1, 2, 3], [4, 5]]  # ragged
        with pytest.raises(IndexError):
            minPath(grid, 3)


# ──────────────────────────────────────────────
# 4. Invalid inputs
# ──────────────────────────────────────────────

class TestInvalidInputs:
    """Tests with inputs that violate documented constraints."""

    def test_negative_k(self):
        """Negative k is not a positive integer."""
        grid = [[1, 2], [3, 4]]
        # range(-1) is empty → returns []
        assert minPath(grid, -1) == []

    def test_k_as_string(self):
        """k is not an integer — type mismatch."""
        grid = [[1, 2], [3, 4]]
        with pytest.raises(TypeError):
            minPath(grid, "3")

    def test_grid_with_missing_value_1(self):
        """Grid does not contain value 1.
           The function defaults to (0,0) and uses grid[0][0] as '1'."""
        grid = [[2, 3], [4, 5]]
        # 1 not found, so x=0, y=0. grid[0][0]=2.
        # Neighbors: 3(right), 4(down) → mn = 3
        # Returns [2, 3, 2, 3, ...]
        result = minPath(grid, 4)
        assert result == [2, 3, 2, 3]

    def test_grid_with_duplicate_values(self):
        """Grid contains duplicates (violates permutation constraint).
           The function finds the FIRST occurrence of 1."""
        grid = [[1, 1], [2, 3]]
        # First 1 at (0,0), neighbors: 1(right), 2(down) → mn = 1
        assert minPath(grid, 3) == [1, 1, 1]

    def test_grid_with_out_of_range_values(self):
        """Grid values outside [1, N*N]."""
        grid = [[0, 2], [3, 4]]
        # 1 not found, defaults to (0,0)=0.
        # Neighbors: 2(right), 3(down) → mn = 2
        result = minPath(grid, 3)
        assert result == [0, 2, 0]

    def test_empty_k_list_not_valid_input(self):
        """k must be an integer, not a list."""
        grid = [[1, 2], [3, 4]]
        with pytest.raises(TypeError):
            minPath(grid, [3])


# ──────────────────────────────────────────────
# 5. Exception cases
# ──────────────────────────────────────────────

class TestExceptionCases:
    """Tests where the function can raise exceptions."""

    def test_grid_row_too_short(self):
        """A row shorter than N causes IndexError when accessing grid[x][y+1]."""
        grid = [[1, 2], [3]]  # second row has only 1 element, N=2
        with pytest.raises(IndexError):
            minPath(grid, 3)

    def test_deeply_nested_invalid_structure(self):
        """Grid element is not a list."""
        grid = [1, 2]
        with pytest.raises(TypeError):
            minPath(grid, 3)

    def test_grid_with_non_integer_elements(self):
        """Grid contains non-integer elements."""
        grid = [["a", "b"], ["c", "d"]]
        # 1 not found, defaults to (0,0)="a". Comparison with integers fails.
        with pytest.raises(TypeError):
            minPath(grid, 3)

    def test_mixed_type_grid(self):
        """Grid with mixed types."""
        grid = [[1, "b"], [3, 4]]
        # 1 found at (0,0), neighbors: "b"(right), 3(down)
        # min(mn, "b") raises TypeError
        with pytest.raises(TypeError):
            minPath(grid, 3)
