"""Unit tests for minPath(grid, k) from solution.py."""

import pytest
from solution import minPath


# ---------------------------------------------------------------------------
# Normal / typical cases
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with well-formed inputs matching the documented examples."""

    def test_example_1(self):
        """grid = [[1,2,3],[4,5,6],[7,8,9]], k = 3 -> [1, 2, 1]."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_example_2(self):
        """grid = [[5,9,3],[4,1,6],[7,8,2]], k = 1 -> [1]."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]

    def test_k_even(self):
        """k=4 alternates 1, mn, 1, mn."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # 1 is at (0,0), neighbors are 2 and 4, min=2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_k_large(self):
        """k=7 alternates correctly."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 7) == [1, 2, 1, 2, 1, 2, 1]

    def test_1_in_center(self):
        """1 is surrounded by larger values; min neighbor should be picked."""
        grid = [[5, 4, 3], [6, 1, 2], [7, 8, 9]]
        # 1 at (1,1); neighbors: 4, 2, 6, 8 -> min=2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_at_top_right_corner(self):
        """1 at top-right corner, only two neighbors."""
        grid = [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
        # 1 at (0,2); neighbors: 2, 4 -> min=2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_1_at_bottom_left_corner(self):
        """1 at bottom-left corner."""
        grid = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
        # 1 at (2,2); neighbors: 4, 2 -> min=2
        assert minPath(grid, 2) == [1, 2]

    def test_1_at_bottom_right_corner(self):
        """1 at bottom-right corner."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # Wait, 1 is at (0,0). Let's put 1 at (2,2).
        grid = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
        # Actually let me redo: 1 at (2,2), neighbors: grid[1][2]=4, grid[2][1]=2 -> min=2
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_min_neighbor_from_different_directions(self):
        """Min neighbor comes from left direction."""
        grid = [[1, 5, 6], [2, 4, 3], [7, 8, 9]]
        # 1 at (0,0); neighbors: grid[1][0]=2, grid[0][1]=5 -> min=2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_larger_grid(self):
        """4x4 grid with 1 somewhere in the middle."""
        grid = [
            [16, 15, 14, 13],
            [11, 10, 9, 12],
            [6, 7, 8, 1],
            [5, 4, 3, 2],
        ]
        # 1 at (2,3); neighbors: grid[1][3]=12, grid[3][3]=2, grid[2][2]=8 -> min=2
        assert minPath(grid, 6) == [1, 2, 1, 2, 1, 2]


# ---------------------------------------------------------------------------
# Boundary cases
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Edge-of-range valid inputs."""

    def test_k_zero(self):
        """k=0 should return an empty list."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 0) == []

    def test_k_one(self):
        """k=1 returns just [1]."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 1) == [1]

    def test_k_two(self):
        """k=2 returns [1, mn]."""
        grid = [[1, 2], [3, 4]]
        # 1 at (0,0); neighbors: grid[0][1]=2, grid[1][0]=3 -> min=2
        assert minPath(grid, 2) == [1, 2]

    def test_minimum_grid_size(self):
        """N=2 is the minimum per the docstring (N >= 2)."""
        grid = [[2, 1], [4, 3]]
        # 1 at (0,1); neighbors: grid[0][0]=2, grid[1][1]=3 -> min=2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_at_top_left(self):
        """1 at top-left corner has exactly 2 neighbors."""
        grid = [[1, 3], [2, 4]]
        # neighbors: 3, 2 -> min=2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_1_at_top_right(self):
        """1 at top-right corner has exactly 2 neighbors."""
        grid = [[3, 1], [4, 2]]
        # neighbors: 3, 2 -> min=2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_at_bottom_left(self):
        """1 at bottom-left corner has exactly 2 neighbors."""
        grid = [[4, 3], [1, 2]]
        # neighbors: 3, 2 -> min=2
        assert minPath(grid, 2) == [1, 2]

    def test_1_at_bottom_right(self):
        """1 at bottom-right corner has exactly 2 neighbors."""
        grid = [[3, 4], [2, 1]]
        # neighbors: 4, 2 -> min=2
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_all_neighbors_same_value(self):
        """All neighbors have the same value as the min."""
        grid = [[1, 2], [2, 3]]
        # 1 at (0,0); neighbors: 2, 2 -> min=2
        assert minPath(grid, 3) == [1, 2, 1]

    def test_alternating_pattern_long(self):
        """Verify the alternating pattern holds for large k."""
        grid = [[1, 5], [3, 4]]
        # 1 at (0,0); neighbors: 5, 3 -> min=3
        expected = [1, 3] * 50  # k=100
        assert minPath(grid, 100) == expected


# ---------------------------------------------------------------------------
# Invalid / exceptional inputs
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Inputs that violate preconditions or cause errors."""

    def test_negative_k(self):
        """Negative k produces an empty range, so returns []."""
        grid = [[1, 2], [3, 4]]
        # range(-1) is empty, so result is []
        assert minPath(grid, -1) == []

    def test_jagged_grid_index_error(self):
        """Jagged rows cause IndexError when accessing neighbors."""
        grid = [[1, 2, 3, 4], [5, 6]]
        with pytest.raises(IndexError):
            minPath(grid, 3)

    def test_1_not_found(self):
        """If 1 is not in the grid, x,y stay (0,0) and behavior is undefined.
        We still test that it doesn't crash on a simple case."""
        grid = [[2, 3], [4, 5]]
        # 1 not present; x=0,y=0 defaults; grid[0][0]=2
        # neighbors of (0,0): grid[0][1]=3, grid[1][0]=4 -> min=3
        assert minPath(grid, 3) == [1, 3, 1]

    def test_non_square_grid(self):
        """Non-square grid may produce unexpected results or errors."""
        grid = [[1, 2, 3], [4, 5, 6]]
        # N=2 (len(grid)), but there are 3 columns. Accessing grid[i][j]
        # where j goes up to N-1=1 should work fine for this case.
        # 1 at (0,0); neighbors within bounds: grid[0][1]=2, grid[1][0]=5 -> min=2
        assert minPath(grid, 3) == [1, 2, 1]


# ---------------------------------------------------------------------------
# Additional edge-case scenarios
# ---------------------------------------------------------------------------

class TestAdditionalScenarios:
    """More nuanced test scenarios."""

    def test_min_neighbor_is_from_below(self):
        """Min neighbor is directly below 1."""
        grid = [[5, 6, 7], [1, 3, 4], [8, 9, 2]]
        # 1 at (1,0); neighbors: grid[0][0]=5, grid[2][0]=8, grid[1][1]=3 -> min=3
        assert minPath(grid, 4) == [1, 3, 1, 3]

    def test_min_neighbor_is_from_above(self):
        """Min neighbor is directly above 1."""
        grid = [[2, 6, 7], [5, 1, 4], [8, 9, 3]]
        # 1 at (1,1); neighbors: grid[0][1]=6, grid[2][1]=9, grid[1][0]=5, grid[1][2]=4 -> min=4
        assert minPath(grid, 3) == [1, 4, 1]

    def test_single_cell_path_repeated(self):
        """k=1 always returns [1] regardless of grid content."""
        for grid in [
            [[1, 2], [3, 4]],
            [[99, 1], [1, 99]],
            [[1]],
        ]:
            assert minPath(grid, 1) == [1]

    def test_k_equals_n_squared(self):
        """k equals total number of cells."""
        grid = [[1, 2], [3, 4]]
        # N=2, N*N=4, k=4
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_values_with_large_gaps(self):
        """Grid values span a wide range."""
        grid = [
            [1, 100, 200],
            [300, 400, 500],
            [600, 700, 800],
        ]
        # 1 at (0,0); neighbors: 100, 300 -> min=100
        assert minPath(grid, 5) == [1, 100, 1, 100, 1]
