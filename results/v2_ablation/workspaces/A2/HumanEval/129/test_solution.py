"""Unit tests for minPath(grid, k) in solution.py.

The function finds the lexicographically smallest path of length k in an N×N grid
(N >= 2) containing each value from 1 to N*N exactly once. It starts at the cell
with value 1 and oscillates between 1 and the minimum-valued neighbor of that cell.

Expected output: [1, mn, 1, mn, ...] where mn is the minimum neighbor of the cell
containing 1, and the list has exactly k elements.

Note: mn is initialized to N*N before checking neighbors, so if all neighbors
exceed N*N, mn remains N*N.
"""

import pytest
from solution import minPath


# ──────────────────────────────────────────────
# Normal / typical cases
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with typical inputs matching the documented examples."""

    def test_example_1(self):
        """Example 1 from docstring: 3x3 grid, k=3."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_example_2(self):
        """Example 2 from docstring: 3x3 grid, k=1."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]

    def test_1_at_corner_top_left(self):
        """Value 1 at top-left corner; two neighbors."""
        grid = [[1, 3, 5], [2, 4, 6], [7, 8, 9]]
        # 1 at (0,0); neighbors: (0,1)=3, (1,0)=2 -> min = 2
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_1_at_corner_bottom_right(self):
        """Value 1 at bottom-right corner; two neighbors."""
        grid = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
        # 1 at (2,2); neighbors: (1,2)=4, (2,1)=2 -> min = 2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_1_in_middle_of_grid(self):
        """Value 1 surrounded on all four sides."""
        grid = [[5, 4, 3], [6, 1, 2], [7, 8, 9]]
        # 1 at (1,1); neighbors: (0,1)=4, (2,1)=8, (1,0)=6, (1,2)=2 -> min = 2
        assert minPath(grid, 6) == [1, 2, 1, 2, 1, 2]

    def test_1_with_correct_min_neighbor(self):
        """Grid where we correctly compute the minimum neighbor."""
        grid = [[10, 1, 9], [8, 7, 6], [5, 4, 3]]
        # 1 at (0,1); neighbors: (0,0)=10, (0,2)=9, (1,1)=7 -> min = 7
        assert minPath(grid, 3) == [1, 7, 1]

    def test_even_k(self):
        """Even-length path ends with the neighbor value."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_odd_k(self):
        """Odd-length path ends with 1."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_larger_grid_4x4(self):
        """4x4 grid with 1 at a corner."""
        grid = [
            [1, 3, 5, 7],
            [2, 4, 6, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]
        # 1 at (0,0); neighbors: (0,1)=3, (1,0)=2 -> min = 2
        assert minPath(grid, 6) == [1, 2, 1, 2, 1, 2]

    def test_1_not_at_corner(self):
        """1 is somewhere in the interior of a 4x4 grid."""
        grid = [
            [16, 15, 14, 13],
            [11, 1, 12, 10],
            [6, 7, 8, 9],
            [5, 4, 3, 2],
        ]
        # 1 at (1,1); neighbors: (0,1)=15, (2,1)=7, (1,0)=11, (1,2)=12 -> min = 7
        assert minPath(grid, 5) == [1, 7, 1, 7, 1]


# ──────────────────────────────────────────────
# Boundary cases
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_minimum_k(self):
        """k = 1: only the value 1 is returned."""
        grid = [[2, 1], [3, 4]]
        assert minPath(grid, 1) == [1]

    def test_minimum_grid_size_N2(self):
        """Smallest valid grid: 2x2."""
        grid = [[2, 1], [3, 4]]
        # 1 at (0,1); neighbors: (0,0)=2, (1,1)=4 -> min = 2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_minimum_grid_N2_k1(self):
        """2x2 grid with k=1."""
        grid = [[4, 3], [1, 2]]
        # 1 at (1,0); neighbors: (0,0)=4, (1,1)=2 -> min = 2
        assert minPath(grid, 1) == [1]

    def test_minimum_grid_N2_k2(self):
        """2x2 grid with k=2."""
        grid = [[4, 3], [1, 2]]
        assert minPath(grid, 2) == [1, 2]

    def test_minimum_grid_N2_k3(self):
        """2x2 grid with k=3."""
        grid = [[4, 3], [1, 2]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_minimum_grid_N2_k4(self):
        """2x2 grid with k=4."""
        grid = [[4, 3], [1, 2]]
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_large_k(self):
        """Large k value with a 3x3 grid."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        expected = [1, 2] * 5 + [1]  # 11 elements
        assert minPath(grid, 11) == expected

    def test_k_equals_n_squared(self):
        """k equals N*N (total number of cells)."""
        grid = [[1, 2], [3, 4]]
        # N=2, N*N=4, k=4
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_1_adjacent_to_value_2_only(self):
        """When 1's only neighbors include 2, and 2 is the minimum."""
        grid = [[2, 1, 3], [4, 5, 6], [7, 8, 9]]
        # 1 at (0,1); neighbors: (0,0)=2, (0,2)=3, (1,1)=5 -> min = 2
        assert minPath(grid, 3) == [1, 2, 1]


# ──────────────────────────────────────────────
# Edge cases: zero, empty, unusual k
# ──────────────────────────────────────────────

class TestEdgeCasesZeroAndEmpty:
    """Tests with zero-size or zero-length inputs."""

    def test_k_zero(self):
        """k = 0: returns an empty list."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 0) == []

    def test_k_zero_on_larger_grid(self):
        """k = 0 on a 3x3 grid still returns []."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 0) == []

    def test_empty_grid(self):
        """Empty grid: N=0, mn=N*N=0, returns [1, 0, 1, 0, ...]."""
        result = minPath([], 5)
        assert result == [1, 0, 1, 0, 1]

    def test_single_row_grid(self):
        """Single row grid: N=1, no neighbors, mn=1, returns [1, 1, 1, ...]."""
        result = minPath([[1, 2, 3]], 4)
        assert result == [1, 1, 1, 1]


# ──────────────────────────────────────────────
# Invalid inputs
# ──────────────────────────────────────────────

class TestInvalidInputs:
    """Tests with inputs that violate documented constraints."""

    @pytest.mark.parametrize("k", [-1, -5, -100])
    def test_negative_k(self, k):
        """Negative k: range(k) is empty, returns []."""
        grid = [[1, 2], [3, 4]]
        result = minPath(grid, k)
        assert len(result) == 0

    def test_grid_without_value_1(self):
        """Grid missing value 1: defaults to (0,0), uses literal 1 in output."""
        grid = [[2, 3], [4, 5]]
        # 1 not found; defaults to (0,0) with value 2
        # Neighbors of (0,0): (0,1)=3, (1,0)=4 -> min = 3
        # Return: [1, 3, 1, 3, ...] (literal 1, not grid[0][0]=2)
        result = minPath(grid, 4)
        assert result == [1, 3, 1, 3]


# ──────────────────────────────────────────────
# Exception cases
# ──────────────────────────────────────────────

class TestExceptionCases:
    """Tests that exercise potential exceptions."""

    def test_grid_missing_value_1_no_exception(self):
        """If value 1 is absent, the function uses (0,0) silently."""
        grid = [[9, 8], [7, 6]]
        # 1 not found; defaults to (0,0) with value 9
        # N=2, N*N=4; neighbors: (0,1)=8, (1,0)=7
        # mn = min(4, 8, 7) = 4
        # Return: [1, 4, 1] (literal 1)
        assert minPath(grid, 3) == [1, 4, 1]

    def test_k_extremely_large(self):
        """Very large k: just returns a long alternating list."""
        grid = [[1, 2], [3, 4]]
        k = 10000
        result = minPath(grid, k)
        assert len(result) == k
        assert result[0] == 1
        assert result[1] == 2
        assert result[-1] == (2 if k % 2 == 0 else 1)


# ──────────────────────────────────────────────
# Additional thorough coverage
# ──────────────────────────────────────────────

class TestAdditionalCoverage:
    """Extra tests for thoroughness."""

    def test_1_at_top_right_corner(self):
        """Value 1 at top-right corner."""
        grid = [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
        # 1 at (0,2); neighbors: (0,1)=2, (1,2)=4 -> min = 2
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_1_at_bottom_left_corner(self):
        """Value 1 at bottom-left corner."""
        grid = [[7, 8, 9], [4, 5, 6], [1, 2, 3]]
        # 1 at (2,0); neighbors: (1,0)=4, (2,1)=2 -> min = 2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_alternation_pattern_correct(self):
        """Verify the exact alternation pattern for various lengths."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for k in range(1, 10):
            expected = [1 if i % 2 == 0 else 2 for i in range(k)]
            assert minPath(grid, k) == expected

    def test_different_min_neighbor(self):
        """Grid where the minimum neighbor of 1 is not 2."""
        grid = [[1, 5, 3], [2, 4, 6], [7, 8, 9]]
        # 1 at (0,0); neighbors: (0,1)=5, (1,0)=2 -> min = 2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_with_mn_bounded_by_n_squared(self):
        """Grid where N*N < neighbor values, so mn = N*N."""
        grid = [[1, 100, 99], [98, 97, 96], [95, 94, 93]]
        # 1 at (0,0); N=3, N*N=9
        # Neighbors: (0,1)=100, (1,0)=98
        # mn = min(9, 100, 98) = 9
        assert minPath(grid, 3) == [1, 9, 1]

    def test_2x2_all_permutations(self):
        """Test all 4 positions of value 1 in a 2x2 grid."""
        # 1 at (0,0)
        assert minPath([[1, 2], [3, 4]], 3) == [1, 2, 1]
        # 1 at (0,1)
        assert minPath([[2, 1], [3, 4]], 3) == [1, 2, 1]
        # 1 at (1,0)
        assert minPath([[3, 4], [1, 2]], 3) == [1, 2, 1]
        # 1 at (1,1)
        assert minPath([[4, 3], [2, 1]], 3) == [1, 2, 1]
