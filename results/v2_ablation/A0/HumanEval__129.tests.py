import pytest
from solution import minPath


class TestMinPathBasic:
    """Test basic functionality of minPath."""

    def test_k_equals_1(self):
        """When k=1, the path should just be [1]."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]

    def test_k_equals_2(self):
        """When k=2, the path should be [1, min_neighbor_of_1]."""
        grid = [[1, 2], [3, 4]]
        # Cell with 1 is at (0,0), neighbors are 2 and 3, min is 2
        assert minPath(grid, 2) == [1, 2]

    def test_k_equals_3_example_from_docstring(self):
        """Example from docstring: grid=[[1,2,3],[4,5,6],[7,8,9]], k=3."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # Cell with 1 is at (0,0), neighbors are 2 and 4, min is 2
        # Pattern: [1, 2, 1]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_k_equals_4(self):
        """Pattern alternates: [1, mn, 1, mn]."""
        grid = [[1, 2], [3, 4]]
        # min neighbor of 1 is 2
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_k_equals_5(self):
        """Pattern alternates: [1, mn, 1, mn, 1]."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]


class TestMinPathGridPositions:
    """Test minPath when 1 is in different positions."""

    def test_1_in_center(self):
        """1 is in the center of a 3x3 grid."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        # Neighbors of 1 at (1,1): 9, 4, 8, 6 -> min is 4
        assert minPath(grid, 1) == [1]
        assert minPath(grid, 2) == [1, 4]
        assert minPath(grid, 3) == [1, 4, 1]

    def test_1_in_corner_top_right(self):
        """1 is at top-right corner."""
        grid = [[2, 3, 1], [5, 6, 4], [8, 7, 9]]
        # Neighbors of 1 at (0,2): 3 (left), 4 (down) -> min is 3
        assert minPath(grid, 2) == [1, 3]
        assert minPath(grid, 3) == [1, 3, 1]

    def test_1_in_corner_bottom_left(self):
        """1 is at bottom-left corner."""
        grid = [[9, 8, 7], [6, 5, 4], [1, 2, 3]]
        # Neighbors of 1 at (2,0): 4 (up), 2 (right) -> min is 2
        assert minPath(grid, 2) == [1, 2]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_in_corner_bottom_right(self):
        """1 is at bottom-right corner."""
        grid = [[4, 3, 2], [5, 6, 1], [8, 7, 9]]
        # Neighbors of 1 at (1,2): 2 (up), 6 (left), 9 (down) -> min is 2
        assert minPath(grid, 2) == [1, 2]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_on_edge_not_corner(self):
        """1 is on an edge but not a corner."""
        grid = [[5, 1, 3], [4, 6, 2], [7, 8, 9]]
        # Neighbors of 1 at (0,1): 5 (left), 3 (right), 6 (down) -> min is 3
        assert minPath(grid, 2) == [1, 3]
        assert minPath(grid, 3) == [1, 3, 1]


class TestMinPathEdgeCases:
    """Test edge cases."""

    def test_minimal_grid_2x2(self):
        """Smallest possible grid size."""
        grid = [[2, 1], [3, 4]]
        # 1 at (0,1), neighbors: 2, 4 -> min is 2
        assert minPath(grid, 1) == [1]
        assert minPath(grid, 2) == [1, 2]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_large_k(self):
        """Test with a large k value."""
        grid = [[1, 2], [3, 4]]
        expected = [1 if i % 2 == 0 else 2 for i in range(100)]
        assert minPath(grid, 100) == expected

    def test_alternating_pattern_correctness(self):
        """Verify the alternating pattern [1, mn, 1, mn, ...] for various k."""
        grid = [[1, 2], [3, 4]]
        # 1 at (0,0), neighbors: 2, 3 -> min is 2
        for k in range(1, 20):
            expected = [1 if i % 2 == 0 else 2 for i in range(k)]
            assert minPath(grid, k) == expected

    def test_1_at_max_value_position(self):
        """Test when 1's neighbors include the maximum value N*N."""
        # 3x3 grid, N*N=9, 1 at (0,0), neighbors 2 and 4
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 2) == [1, 2]

    def test_1_adjacent_to_nn(self):
        """Test when 1 is adjacent to cell with value N*N."""
        # 3x3 grid, 1 at (0,0), N*N=9 at (2,2) — not adjacent
        # Use 1 at (1,2), N*N=9 at (2,2) — adjacent
        grid = [[2, 3, 4], [5, 6, 1], [7, 8, 9]]
        # 1 at (1,2), neighbors: 4 (up), 6 (left), 9 (down) -> min is 4
        assert minPath(grid, 2) == [1, 4]


class TestMinPathLargerGrids:
    """Test with larger grids."""

    def test_4x4_grid(self):
        """Test with a 4x4 grid."""
        grid = [
            [10, 11, 12, 13],
            [9, 1, 14, 15],
            [8, 7, 6, 5],
            [4, 3, 2, 16]
        ]
        # 1 at (1,1), neighbors: 11, 9, 7, 14 -> min is 7
        assert minPath(grid, 1) == [1]
        assert minPath(grid, 2) == [1, 7]
        assert minPath(grid, 3) == [1, 7, 1]
        assert minPath(grid, 4) == [1, 7, 1, 7]

    def test_5x5_grid(self):
        """Test with a 5x5 grid."""
        grid = [
            [25, 24, 23, 22, 21],
            [10, 9, 8, 7, 6],
            [11, 2, 1, 3, 5],
            [12, 13, 14, 15, 4],
            [16, 17, 18, 19, 20]
        ]
        # 1 at (2,2), neighbors: 8, 14, 2, 3 -> min is 2
        assert minPath(grid, 1) == [1]
        assert minPath(grid, 2) == [1, 2]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_3x3_with_1_at_different_positions(self):
        """Test all possible positions of 1 in a 3x3 grid."""
        # 1 at (0,0): neighbors 2, 4 -> min 2
        grid1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid1, 2) == [1, 2]

        # 1 at (0,1): neighbors 2, 3, 5 -> min 2
        grid2 = [[2, 1, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid2, 2) == [1, 2]

        # 1 at (0,2): neighbors 3, 6 -> min 3
        grid3 = [[2, 3, 1], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid3, 2) == [1, 3]

        # 1 at (1,0): neighbors 2, 4, 7 -> min 2
        grid4 = [[2, 3, 4], [1, 5, 6], [7, 8, 9]]
        assert minPath(grid4, 2) == [1, 2]

        # 1 at (1,1): neighbors 3, 8, 5, 6 -> min 3
        grid5 = [[2, 3, 4], [5, 1, 6], [7, 8, 9]]
        assert minPath(grid5, 2) == [1, 3]

        # 1 at (1,2): neighbors 4, 6, 9 -> min 4
        grid6 = [[2, 3, 4], [5, 6, 1], [7, 8, 9]]
        assert minPath(grid6, 2) == [1, 4]

        # 1 at (2,0): neighbors 5 (up), 8 (right) -> min 5
        grid7 = [[2, 3, 4], [5, 6, 7], [1, 8, 9]]
        assert minPath(grid7, 2) == [1, 5]

        # 1 at (2,1): neighbors 6 (up), 8 (left), 9 (right) -> min 6
        grid8 = [[2, 3, 4], [5, 6, 7], [8, 1, 9]]
        assert minPath(grid8, 2) == [1, 6]

        # 1 at (2,2): neighbors 7 (up), 9 (left) -> min 7
        grid9 = [[2, 3, 4], [5, 6, 7], [8, 9, 1]]
        assert minPath(grid9, 2) == [1, 7]


class TestMinPathReturnTypes:
    """Test return types and data integrity."""

    def test_return_is_list(self):
        """Ensure the return value is a list."""
        grid = [[1, 2], [3, 4]]
        result = minPath(grid, 3)
        assert isinstance(result, list)

    def test_return_length_matches_k(self):
        """The returned list should have exactly k elements."""
        grid = [[1, 2], [3, 4]]
        for k in range(1, 10):
            result = minPath(grid, k)
            assert len(result) == k

    def test_first_element_always_1(self):
        """The first element of the path should always be 1."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        for k in range(1, 20):
            result = minPath(grid, k)
            assert result[0] == 1


class TestMinPathDocstringExamples:
    """Test the exact examples from the docstring."""

    def test_example_1(self):
        """grid = [[1,2,3],[4,5,6],[7,8,9]], k = 3 -> [1, 2, 1]"""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_example_2(self):
        """grid = [[5,9,3],[4,1,6],[7,8,2]], k = 1 -> [1]"""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]
