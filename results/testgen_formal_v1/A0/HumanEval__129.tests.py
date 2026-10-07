import pytest
from solution import minPath


class TestMinPathBasicExamples:
    """Tests based on the docstring examples."""

    def test_example_1(self):
        """grid = [[1,2,3],[4,5,6],[7,8,9]], k = 3 -> [1, 2, 1]"""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert minPath(grid, 3) == [1, 2, 1]

    def test_example_2(self):
        """grid = [[5,9,3],[4,1,6],[7,8,2]], k = 1 -> [1]"""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        assert minPath(grid, 1) == [1]


class TestMinPathKValues:
    """Tests with various k values."""

    def test_k_equals_1(self):
        """When k=1, the result should be [1]."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 1) == [1]

    def test_k_equals_2(self):
        """When k=2, the result should be [1, min_neighbor_of_1]."""
        grid = [[1, 2], [3, 4]]
        # Cell with 1 is at (0,0), neighbors are 2 and 3, min is 2
        assert minPath(grid, 2) == [1, 2]

    def test_k_equals_4(self):
        """When k=4, the result should alternate: [1, mn, 1, mn]."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_k_equals_5(self):
        """When k=5, the result should be [1, mn, 1, mn, 1]."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_large_k(self):
        """Test with a large k value."""
        grid = [[1, 2], [3, 4]]
        expected = [1 if i % 2 == 0 else 2 for i in range(20)]
        assert minPath(grid, 20) == expected


class TestMinPathGridSize2x2:
    """Tests with 2x2 grids."""

    def test_1_at_top_left(self):
        """1 at top-left corner."""
        grid = [[1, 2], [3, 4]]
        # Neighbors of 1: 2 (right), 3 (down). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_at_top_right(self):
        """1 at top-right corner."""
        grid = [[2, 1], [3, 4]]
        # Neighbors of 1: 2 (left), 4 (down). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_at_bottom_left(self):
        """1 at bottom-left corner."""
        grid = [[3, 4], [1, 2]]
        # Neighbors of 1: 4 (up), 2 (right). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_at_bottom_right(self):
        """1 at bottom-right corner."""
        grid = [[3, 4], [2, 1]]
        # Neighbors of 1: 4 (up), 2 (left). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_with_larger_neighbor_min(self):
        """1 surrounded by larger values."""
        grid = [[4, 3], [2, 1]]
        # Neighbors of 1: 3 (up), 2 (left). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]


class TestMinPathGridSize3x3:
    """Tests with 3x3 grids."""

    def test_1_in_center(self):
        """1 in the center of a 3x3 grid."""
        grid = [[2, 3, 4], [5, 1, 6], [7, 8, 9]]
        # Neighbors of 1: 3 (up), 6 (right), 8 (down), 5 (left). Min = 3.
        assert minPath(grid, 3) == [1, 3, 1]

    def test_1_on_edge(self):
        """1 on the top edge of a 3x3 grid."""
        grid = [[1, 5, 3], [4, 2, 6], [7, 8, 9]]
        # Neighbors of 1: 5 (right), 4 (down). Min = 4.
        assert minPath(grid, 3) == [1, 4, 1]

    def test_1_on_corner(self):
        """1 on a corner of a 3x3 grid."""
        grid = [[1, 5, 3], [4, 2, 6], [7, 8, 9]]
        # Neighbors of 1: 5 (right), 4 (down). Min = 4.
        assert minPath(grid, 3) == [1, 4, 1]

    def test_1_with_small_neighbor(self):
        """1 has a very small neighbor."""
        grid = [[1, 10, 9], [2, 8, 7], [6, 5, 4]]
        # Neighbors of 1: 10 (right), 2 (down). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]


class TestMinPathGridSize4x4:
    """Tests with 4x4 grids."""

    def test_basic_4x4(self):
        """Basic 4x4 grid test."""
        grid = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]
        # Neighbors of 1: 2 (right), 5 (down). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_not_at_origin(self):
        """1 is not at position (0,0)."""
        grid = [
            [16, 15, 14, 13],
            [12, 11, 10, 9],
            [8, 7, 6, 5],
            [4, 3, 2, 1],
        ]
        # Neighbors of 1: 3 (left), 2 (up). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]


class TestMinPathEdgeCases:
    """Edge case tests."""

    def test_k_is_odd(self):
        """Test with odd k - last element should be 1."""
        grid = [[1, 2], [3, 4]]
        result = minPath(grid, 7)
        assert result[-1] == 1
        assert result[0] == 1

    def test_k_is_even(self):
        """Test with even k - last element should be min_neighbor."""
        grid = [[1, 2], [3, 4]]
        result = minPath(grid, 6)
        assert result[-1] == 2
        assert result[0] == 1

    def test_alternating_pattern(self):
        """Verify the alternating pattern [1, mn, 1, mn, ...]."""
        grid = [[1, 2], [3, 4]]
        result = minPath(grid, 10)
        for i in range(10):
            if i % 2 == 0:
                assert result[i] == 1
            else:
                assert result[i] == 2

    def test_result_length_equals_k(self):
        """Result list length must equal k."""
        grid = [[1, 2], [3, 4]]
        for k in range(1, 11):
            result = minPath(grid, k)
            assert len(result) == k

    def test_all_elements_are_1_or_mn(self):
        """All elements in result should be either 1 or the min neighbor."""
        grid = [[1, 2], [3, 4]]
        result = minPath(grid, 15)
        for val in result:
            assert val in (1, 2)


class TestMinPathReturnTypes:
    """Tests for return type correctness."""

    def test_returns_list(self):
        """Result should be a list."""
        grid = [[1, 2], [3, 4]]
        assert isinstance(minPath(grid, 1), list)

    def test_elements_are_integers(self):
        """All elements should be integers."""
        grid = [[1, 2], [3, 4]]
        result = minPath(grid, 5)
        for val in result:
            assert isinstance(val, int)


class TestMinPathUniqueness:
    """Tests verifying unique answer guarantee."""

    def test_deterministic_output(self):
        """Same input should always produce same output."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result1 = minPath(grid, 5)
        result2 = minPath(grid, 5)
        assert result1 == result2


class TestMinPathLargerGrids:
    """Tests with larger grids."""

    def test_5x5_grid(self):
        """Test with a 5x5 grid."""
        grid = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25],
        ]
        # Neighbors of 1: 2 (right), 6 (down). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]

    def test_5x5_grid_1_in_middle(self):
        """Test with 1 in the middle of a 5x5 grid."""
        grid = [
            [25, 24, 23, 22, 21],
            [20, 19, 18, 17, 16],
            [15, 14, 13, 12, 11],
            [10, 9, 8, 7, 6],
            [5, 4, 3, 2, 1],
        ]
        # Neighbors of 1: 2 (left), 6 (up). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]

    def test_10x10_grid(self):
        """Test with a 10x10 grid."""
        grid = [[i * 10 + j + 1 for j in range(10)] for i in range(10)]
        # Neighbors of 1: 2 (right), 11 (down). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]


class TestMinPathSpecialConfigurations:
    """Tests with special grid configurations."""

    def test_1_has_wide_range_neighbors(self):
        """1 has neighbors spanning a wide range of values (valid grid)."""
        # Use a 4x4 grid where 1's neighbors are 4 and 3 (min=3)
        grid = [
            [1, 4, 3, 2],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]
        # Neighbors of 1: 4 (right), 5 (down). Min = 4.
        assert minPath(grid, 3) == [1, 4, 1]

    def test_1_adjacent_to_larger_values_only(self):
        """1 only has relatively large-valued neighbors."""
        # Use a 4x4 grid where 1's neighbors are 10 and 11 (min=10)
        grid = [
            [1, 10, 3, 4],
            [11, 6, 7, 8],
            [9, 5, 2, 12],
            [13, 14, 15, 16],
        ]
        # Neighbors of 1: 10 (right), 11 (down). Min = 10.
        assert minPath(grid, 3) == [1, 10, 1]

    def test_1_adjacent_to_very_small_non_1_values(self):
        """1's neighbors are just above 1."""
        grid = [[1, 2], [3, 4]]
        # Neighbors of 1: 2 (right), 3 (down). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]
