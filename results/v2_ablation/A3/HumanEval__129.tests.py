import pytest
from solution import minPath


# ──────────────────────────────────────────────
# Normal / typical cases
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with typical valid inputs matching the documented examples."""

    def test_example_1(self):
        """grid = [[1,2,3],[4,5,6],[7,8,9]], k = 3 → [1, 2, 1]"""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_example_2(self):
        """grid = [[5,9,3],[4,1,6],[7,8,2]], k = 1 → [1]"""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]

    def test_k_even(self):
        """Even-length path alternates correctly."""
        # 1 is at (0,0), neighbors are 2 and 4 → min = 2
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_k_five(self):
        """Odd-length path of 5."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_1_in_corner_bottom_right(self):
        """Cell with 1 is at bottom-right corner."""
        grid = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
        # 1 at (2,2), neighbors: (1,2)=4, (2,1)=2 → min = 2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_on_edge(self):
        """Cell with 1 is on an edge (not a corner)."""
        grid = [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
        # 1 at (0,2), neighbors: (0,1)=2, (1,2)=4 → min = 2
        assert minPath(grid, 2) == [1, 2]

    def test_1_in_center(self):
        """Cell with 1 is in the center of a larger grid."""
        grid = [
            [16, 15, 14, 13],
            [11, 10, 9, 12],
            [8, 7, 1, 6],
            [3, 4, 5, 2],
        ]
        # 1 at (2,2), neighbors: (1,2)=9, (3,2)=5, (2,1)=7, (2,3)=6 → min = 5
        assert minPath(grid, 4) == [1, 5, 1, 5]

    def test_larger_grid(self):
        """4x4 grid with 1 near top-left."""
        grid = [
            [1, 10, 11, 12],
            [9, 8, 7, 13],
            [2, 3, 4, 14],
            [5, 6, 15, 16],
        ]
        # 1 at (0,0), neighbors: (0,1)=10, (1,0)=9 → min = 9
        assert minPath(grid, 6) == [1, 9, 1, 9, 1, 9]


# ──────────────────────────────────────────────
# Boundary cases
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_smallest_grid_2x2(self):
        """Minimum allowed grid size: 2x2."""
        grid = [[1, 2], [3, 4]]
        # 1 at (0,0), neighbors: (0,1)=2, (1,0)=3 → min = 2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_2x2_with_1_at_other_positions(self):
        """2x2 grid with 1 at each possible position."""
        # 1 at (0,1)
        grid = [[2, 1], [3, 4]]
        # neighbors: (0,0)=2, (1,1)=4 → min = 2
        assert minPath(grid, 2) == [1, 2]

        # 1 at (1,0)
        grid = [[3, 4], [1, 2]]
        # neighbors: (0,0)=3, (1,1)=2 → min = 2
        assert minPath(grid, 2) == [1, 2]

        # 1 at (1,1)
        grid = [[3, 4], [2, 1]]
        # neighbors: (0,1)=4, (1,0)=2 → min = 2
        assert minPath(grid, 2) == [1, 2]

    def test_large_k(self):
        """Very large k value."""
        grid = [[1, 2], [3, 4]]
        expected = [1, 2] * 500  # k = 1000
        assert minPath(grid, 1000) == expected

    def test_min_neighbor_is_2(self):
        """When 1's minimum neighbor is 2 (the smallest possible > 1)."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_min_neighbor_is_large(self):
        """When all neighbors are larger than N*N, mn defaults to N*N."""
        # Grid is 3x3, N=3, so mn starts at N*N=9.
        # All neighbors (99, 96, 97, 94) > 9, so mn stays at 9.
        grid = [
            [100, 99, 98],
            [97, 1, 96],
            [95, 94, 93],
        ]
        assert minPath(grid, 4) == [1, 9, 1, 9]

    def test_neighbors_all_equal_to_n_sq(self):
        """When neighbors equal N*N exactly, mn = N*N."""
        # 3x3 grid, N=3, N*N=9. Neighbors are all 9.
        grid = [
            [9, 9, 9],
            [9, 1, 9],
            [9, 9, 9],
        ]
        assert minPath(grid, 3) == [1, 9, 1]


# ──────────────────────────────────────────────
# Edge cases: zero-size / empty / null-like inputs
# ──────────────────────────────────────────────

class TestEdgeCasesZeroSize:
    """Tests for zero-size, empty, or unusual inputs."""

    def test_k_equals_zero(self):
        """k = 0 should return an empty list."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 0) == []

    def test_k_equals_one(self):
        """k = 1 always returns [1]."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]

    def test_single_cell_path(self):
        """Verify that only the first element is 1 when k=1."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = minPath(grid, 1)
        assert len(result) == 1
        assert result[0] == 1


# ──────────────────────────────────────────────
# Invalid inputs (function does not validate; we document behaviour)
# ──────────────────────────────────────────────

class TestInvalidInputs:
    """Tests with inputs outside documented constraints.
    
    The function does NOT validate inputs, so these test whatever
    implicit behaviour occurs.
    """

    def test_negative_k(self):
        """Negative k: range(negative) is empty → returns []."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, -1) == []

    def test_empty_grid(self):
        """Empty grid: N=0, no loops run, x=y=0, mn=0, no neighbor checks.
        Returns [1]*k since mn=0 and 0%2==0 → 1, 0%2!=0 → 0... 
        Actually: [1 if i%2==0 else 0 for i in range(k)]
        For k=3: [1, 0, 1]
        """
        grid = []
        assert minPath(grid, 3) == [1, 0, 1]

    def test_non_square_grid(self):
        """Non-square grid: function uses len(grid) as N but accesses
        grid[i][j] — may work or fail depending on shape."""
        # This is outside documented constraints; testing anyway.
        grid = [[1, 2, 3], [4, 5, 6]]  # 2x3
        # N = 2, looks for 1 at (0,0), neighbors within 2x2 bounds:
        # (0,1)=2, (1,0)=5 → min=2
        assert minPath(grid, 3) == [1, 2, 1]


# ──────────────────────────────────────────────
# Exception / error-raising cases
# ──────────────────────────────────────────────

class TestExceptionCases:
    """Tests where the function can raise exceptions."""

    def test_missing_value_1(self):
        """Grid without value 1: x,y stay at (0,0), mn=N*N.
        This is technically invalid per spec but won't crash."""
        grid = [[2, 3], [4, 5]]
        # 1 not found, x=0,y=0, grid[0][0]=2
        # neighbors: (0,1)=3, (1,0)=4 → min=3
        assert minPath(grid, 3) == [1, 3, 1]

    def test_single_row_grid(self):
        """Single-row grid: fewer neighbors available."""
        grid = [[1, 2, 3]]
        # N=1, 1 at (0,0), only right neighbor exists: (0,1)=2
        # But wait: N=len(grid)=1, so x<N-1 means 0<0=False, no down neighbor
        # y<N-1 means 0<2=True, so (0,1)=2 is checked
        # Actually N=1, so x<N-1 → 0<0 → False. Only horizontal neighbors.
        # Wait, N = len(grid) = 1. So x=0, y=0.
        # x>0: False. x<N-1: 0<0: False. y>0: False. y<N-1: 0<0: False.
        # mn stays at N*N = 1.
        # Result: [1, 1, 1, ...]
        assert minPath(grid, 3) == [1, 1, 1]

    def test_grid_with_duplicate_values(self):
        """Grid with duplicate values: only first occurrence of 1 is used."""
        grid = [[1, 1], [2, 3]]
        # First 1 found at (0,0), neighbors: (0,1)=1, (1,0)=2 → min=1
        assert minPath(grid, 3) == [1, 1, 1]


# ──────────────────────────────────────────────
# Pattern verification
# ──────────────────────────────────────────────

class TestPatternVerification:
    """Tests that verify the alternating pattern structure."""

    def test_all_odd_indices_are_1(self):
        """Every element at an odd index (0-based) equals the min neighbor."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = minPath(grid, 7)
        for i in range(0, len(result), 2):
            assert result[i] == 1
        for i in range(1, len(result), 2):
            assert result[i] == 2

    def test_result_length_equals_k(self):
        """Result length always equals k."""
        grid = [[1, 2], [3, 4]]
        for k in range(0, 20):
            assert len(minPath(grid, k)) == k

    def test_alternating_pattern_consistent(self):
        """Increasing k by 1 appends one more element to the pattern."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        r1 = minPath(grid, 5)
        r2 = minPath(grid, 6)
        assert r2[:5] == r1
        assert r2[5] == 2  # next in alternating pattern
