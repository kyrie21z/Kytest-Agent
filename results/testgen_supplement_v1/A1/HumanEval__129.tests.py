"""
Unit tests for solution.minPath(grid, k).

Function summary:
  - Given an N x N grid (N >= 2) containing each integer in [1, N*N] exactly once,
    and a positive integer k, find the lexicographically smallest path of length k.
  - The optimal strategy: start at the cell with value 1, oscillate between 1 and
    the smallest-valued neighbor of that cell.
  - Returns [1, mn, 1, mn, ...] of length k, where mn = min value among 1's neighbors.
"""

import pytest
from solution import minPath


# ---------------------------------------------------------------------------
# 1. Normal / typical cases
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with typical, well-formed inputs."""

    def test_example_1(self):
        """Example from docstring: 3x3 grid, k=3 -> [1, 2, 1]."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_example_2(self):
        """Example from docstring: 3x3 grid, k=1 -> [1]."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]

    def test_3x3_k_even(self):
        """3x3 grid with 1 at corner, even k."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # 1 at (0,0); neighbors are 2 and 4; mn=2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_3x3_k_odd(self):
        """3x3 grid with 1 at center, odd k > 1."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        # 1 at (1,1); neighbors are 9, 8, 4, 6; mn=4
        assert minPath(grid, 5) == [1, 4, 1, 4, 1]

    def test_3x3_k_2(self):
        """3x3 grid, k=2."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 2) == [1, 4]

    def test_4x4_grid(self):
        """Larger grid: 4x4 with 1 not at a corner."""
        grid = [
            [16, 15, 14, 13],
            [11,  1, 12, 10],
            [ 7,  8,  9,  6],
            [ 3,  4,  5,  2],
        ]
        # 1 at (1,1); neighbors: 15, 12, 11, 8 => mn=8
        assert minPath(grid, 6) == [1, 8, 1, 8, 1, 8]

    def test_5x5_grid(self):
        """Even larger grid: 5x5 with 1 near the middle."""
        grid = [
            [25, 24, 23, 22, 21],
            [20, 19, 18, 17, 16],
            [15, 14,  1, 13, 12],
            [10, 11,  8,  9,  6],
            [ 5,  4,  7,  3,  2],
        ]
        # 1 at (2,2); neighbors: 18, 13, 14, 8 => mn=8
        assert minPath(grid, 3) == [1, 8, 1]

    def test_1_at_edge_not_corner(self):
        """1 on an edge (not corner) — fewer neighbors."""
        grid = [
            [10, 11, 12],
            [ 1,  2,  3],
            [ 7,  8,  9],
        ]
        # 1 at (1,0); neighbors: 10, 2, 7 => mn=2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_1_at_bottom_right_corner(self):
        """1 placed at bottom-right corner."""
        grid = [
            [ 9,  8,  7],
            [ 6,  5,  4],
            [ 3,  2,  1],
        ]
        # 1 at (2,2); neighbors: 5, 2 => mn=2
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]


# ---------------------------------------------------------------------------
# 2. Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries of valid inputs."""

    def test_minimum_grid_size_N2(self):
        """Smallest allowed grid: 2x2."""
        grid = [[1, 2], [3, 4]]
        # 1 at (0,0); neighbors: 2, 3 => mn=2
        assert minPath(grid, 1) == [1]

    def test_minimum_grid_size_N2_k2(self):
        """2x2 grid, k=2."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 2) == [1, 2]

    def test_minimum_grid_size_N2_k3(self):
        """2x2 grid, k=3."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_minimum_grid_size_N2_k4(self):
        """2x2 grid, k=4."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_k_equals_N_squared(self):
        """k equals total number of cells (large k)."""
        grid = [[1, 2], [3, 4]]
        # N*N = 4
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_large_k(self):
        """Very large k value."""
        grid = [[1, 2], [3, 4]]
        result = minPath(grid, 100)
        expected = [1 if i % 2 == 0 else 2 for i in range(100)]
        assert result == expected

    def test_k_is_one(self):
        """Minimum valid k."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 1) == [1]

    def test_k_is_two(self):
        """Second smallest valid k."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 2) == [1, 2]


# ---------------------------------------------------------------------------
# 3. Edge cases: zero-size or unusual k
# ---------------------------------------------------------------------------

class TestZeroAndEdgeK:
    """Tests with k=0 or other edge-case k values."""

    def test_k_zero(self):
        """k=0 should return an empty list (no cells visited)."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 0) == []

    def test_k_negative(self):
        """Negative k produces an empty list (range(negative) is empty)."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, -1) == []

    def test_k_negative_large(self):
        """Large negative k."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, -100) == []


# ---------------------------------------------------------------------------
# 4. Invalid inputs (grid constraints violated)
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests with inputs that violate documented preconditions."""

    def test_single_cell_grid(self):
        """N=1 violates the documented constraint N >= 2."""
        # The function will still run but has no neighbors for 1.
        grid = [[1]]
        # No neighbors exist, so mn stays at N*N = 1.
        assert minPath(grid, 3) == [1, 1, 1]

    def test_non_square_grid(self):
        """Non-square grid: rows != columns. Code uses len(grid) as N."""
        grid = [[1, 2, 3], [4, 5, 6]]
        # N = 2 (len(grid)), but grid has 3 columns.
        # 1 at (0,0); within N=2 bounds: neighbors grid[0][1]=2, grid[1][0]=4
        # mn = min(2, 4) = 2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_duplicate_values(self):
        """Grid with duplicate values (violates uniqueness constraint)."""
        grid = [[1, 1], [3, 4]]
        # First occurrence of 1 found at (0,0); neighbors: 1, 3 => mn=1
        assert minPath(grid, 3) == [1, 1, 1]

    def test_missing_value_1(self):
        """Grid without value 1. Function will never find 1, so x,y=(0,0)."""
        grid = [[2, 3], [4, 5]]
        # x=0, y=0; grid[0][0]=2 (not 1). Neighbors: grid[0][1]=3, grid[1][0]=4
        # mn = min(3, 4) = 3
        assert minPath(grid, 3) == [1, 3, 1]

    def test_empty_grid(self):
        """Empty grid — len(grid)=0, N=0, loops don't execute, mn=0.
        The function does NOT raise; it returns [1, 0, 1, 0, ...]."""
        grid = []
        assert minPath(grid, 4) == [1, 0, 1, 0]

    def test_row_with_different_lengths(self):
        """Jagged array: rows have different lengths."""
        grid = [[1, 2, 3], [4, 5]]
        # N = 2; 1 at (0,0); neighbors within N=2: grid[0][1]=2, grid[1][0]=4
        assert minPath(grid, 3) == [1, 2, 1]


# ---------------------------------------------------------------------------
# 5. Exception cases
# ---------------------------------------------------------------------------

class TestExceptions:
    """Tests that verify exceptions are raised for clearly invalid inputs."""

    def test_none_grid(self):
        """Passing None as grid should raise an exception."""
        with pytest.raises(TypeError):
            minPath(None, 1)

    def test_none_k(self):
        """Passing None as k should raise an exception."""
        grid = [[1, 2], [3, 4]]
        with pytest.raises(TypeError):
            minPath(grid, None)

    def test_empty_list_as_k(self):
        """Passing a list as k should raise TypeError when used in range()."""
        grid = [[1, 2], [3, 4]]
        with pytest.raises(TypeError):
            minPath(grid, [])

    def test_string_k(self):
        """Passing a string as k should raise TypeError."""
        grid = [[1, 2], [3, 4]]
        with pytest.raises(TypeError):
            minPath(grid, "abc")

    def test_float_k(self):
        """Passing a float as k should raise TypeError in range()."""
        grid = [[1, 2], [3, 4]]
        with pytest.raises(TypeError):
            minPath(grid, 3.5)


# ---------------------------------------------------------------------------
# 6. Additional correctness / structural tests
# ---------------------------------------------------------------------------

class TestCorrectnessProperties:
    """Tests based on properties of the returned result."""

    def test_result_length_equals_k(self):
        """Result list always has length equal to k (for non-negative k)."""
        for k in [1, 2, 5, 10, 50]:
            grid = [[1, 2], [3, 4]]
            assert len(minPath(grid, k)) == k

    def test_result_alternates_1_and_mn(self):
        """For k >= 2, elements at even indices are 1, odd indices are mn."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        result = minPath(grid, 7)
        for i in range(len(result)):
            if i % 2 == 0:
                assert result[i] == 1
            else:
                assert result[i] == 4  # mn for this grid

    def test_first_element_always_1_for_k_ge_1(self):
        """When k >= 1, the first element of the path is always 1."""
        grids = [
            [[1, 2], [3, 4]],
            [[5, 9, 3], [4, 1, 6], [7, 8, 2]],
            [[16, 15, 14, 13], [11, 1, 12, 10], [7, 8, 9, 6], [3, 4, 5, 2]],
        ]
        for grid in grids:
            assert minPath(grid, 1)[0] == 1
            assert minPath(grid, 3)[0] == 1

    def test_second_element_is_min_neighbor_of_1(self):
        """For k >= 2, the second element is the minimum neighbor of the cell with 1."""
        # Verify by brute-force: check that mn is indeed the smallest neighbor
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        # Find position of 1
        N = len(grid)
        pos = None
        for i in range(N):
            for j in range(N):
                if grid[i][j] == 1:
                    pos = (i, j)
        neighbors = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = pos[0] + di, pos[1] + dj
            if 0 <= ni < N and 0 <= nj < N:
                neighbors.append(grid[ni][nj])
        mn = min(neighbors)
        assert minPath(grid, 2)[1] == mn
