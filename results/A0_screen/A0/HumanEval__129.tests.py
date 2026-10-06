"""Unit tests for solution.minPath using pytest."""

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
    """Tests varying k values."""

    def test_k_equals_1(self):
        """When k=1, result should always be [1]."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 1) == [1]

    def test_k_equals_2(self):
        """When k=2, result should be [1, min_neighbor_of_1]."""
        grid = [[1, 2], [3, 4]]
        # 1 is at (0,0), neighbors are 2 and 3, min is 2
        assert minPath(grid, 2) == [1, 2]

    def test_k_equals_4(self):
        """When k=4, result should be [1, mn, 1, mn]."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_k_equals_5(self):
        """When k=5, result should be [1, mn, 1, mn, 1]."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_large_k(self):
        """Test with a large k value."""
        grid = [[1, 2], [3, 4]]
        expected = [1, 2] * 50 + [1]  # 101 elements
        assert minPath(grid, 101) == expected


class TestMinPathGridSize2x2:
    """Tests on 2x2 grids."""

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

    def test_1_with_larger_neighbors(self):
        """1 surrounded by larger values."""
        grid = [[4, 3], [2, 1]]
        # Neighbors of 1: 3 (up), 2 (left). Min = 2.
        assert minPath(grid, 2) == [1, 2]


class TestMinPathGridSize3x3:
    """Tests on 3x3 grids."""

    def test_1_at_corner_with_small_neighbor(self):
        """1 at corner, smallest neighbor is 2."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # Neighbors of 1: 2 (right), 4 (down). Min = 2.
        assert minPath(grid, 1) == [1]
        assert minPath(grid, 2) == [1, 2]
        assert minPath(grid, 3) == [1, 2, 1]
        assert minPath(grid, 4) == [1, 2, 1, 2]

    def test_1_in_center(self):
        """1 in the center of the grid."""
        grid = [[5, 4, 3], [6, 1, 2], [7, 8, 9]]
        # Neighbors of 1: 4 (up), 2 (right), 8 (down), 6 (left). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_on_edge(self):
        """1 on an edge (not corner)."""
        grid = [[3, 1, 2], [6, 5, 4], [7, 8, 9]]
        # Neighbors of 1: 3 (left), 2 (right), 5 (down). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]

    def test_1_with_larger_neighbors(self):
        """1 surrounded by relatively large values."""
        grid = [[5, 6, 7], [4, 1, 8], [3, 2, 9]]
        # Neighbors of 1: 6 (up), 8 (right), 2 (down), 4 (left). Min = 2.
        assert minPath(grid, 3) == [1, 2, 1]


class TestMinPathGridSize4x4:
    """Tests on larger grids."""

    def test_1_with_min_neighbor_is_2(self):
        """Smallest possible neighbor value is 2."""
        grid = [
            [1, 2, 3, 4],
            [8, 7, 6, 5],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]
        # Neighbors of 1: 2 (right), 8 (down). Min = 2.
        assert minPath(grid, 5) == [1, 2, 1, 2, 1]

    def test_1_not_adjacent_to_2(self):
        """1 is not next to 2; must find nearest smaller neighbor."""
        grid = [
            [1, 5, 6, 7],
            [4, 3, 2, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]
        # Neighbors of 1: 5 (right), 4 (down). Min = 4.
        assert minPath(grid, 3) == [1, 4, 1]


class TestMinPathReturnTypesAndLengths:
    """Tests for return type and length correctness."""

    def test_return_type_is_list(self):
        """Result should be a Python list."""
        grid = [[1, 2], [3, 4]]
        result = minPath(grid, 3)
        assert isinstance(result, list)

    def test_return_length_equals_k(self):
        """Returned list length should equal k."""
        grid = [[1, 2], [3, 4]]
        for k in range(1, 20):
            result = minPath(grid, k)
            assert len(result) == k

    def test_all_elements_are_integers(self):
        """All elements in the result should be integers."""
        grid = [[1, 2], [3, 4]]
        result = minPath(grid, 10)
        assert all(isinstance(x, int) for x in result)

    def test_elements_are_valid_grid_values(self):
        """All returned values should exist in the grid."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = minPath(grid, 7)
        flat = [cell for row in grid for cell in row]
        assert all(x in flat for x in result)


class TestMinPathEdgeCases:
    """Edge case tests."""

    def test_minimum_grid_size(self):
        """Minimum grid size is 2x2."""
        grid = [[1, 2], [3, 4]]
        assert minPath(grid, 1) == [1]

    def test_k_equals_n_squared(self):
        """k equals total number of cells."""
        grid = [[1, 2], [3, 4]]
        n_sq = 4
        expected = [1, 2] * (n_sq // 2)
        assert minPath(grid, n_sq) == expected

    def test_alternating_pattern(self):
        """Verify the alternating [1, mn, 1, mn, ...] pattern."""
        grid = [[1, 3], [2, 4]]
        # Neighbors of 1: 3 (right), 2 (down). Min = 2.
        result = minPath(grid, 10)
        for i in range(10):
            if i % 2 == 0:
                assert result[i] == 1
            else:
                assert result[i] == 2

    def test_result_starts_with_1(self):
        """Every result should start with 1."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for k in range(1, 10):
            assert minPath(grid, k)[0] == 1

    def test_odd_k_ends_with_1(self):
        """When k is odd, last element should be 1."""
        grid = [[1, 2], [3, 4]]
        for k in range(1, 20, 2):
            assert minPath(grid, k)[-1] == 1

    def test_even_k_ends_with_mn(self):
        """When k is even, last element should be the min neighbor."""
        grid = [[1, 2], [3, 4]]
        for k in range(2, 20, 2):
            assert minPath(grid, k)[-1] == 2


class TestMinPathLexicographicCorrectness:
    """Tests verifying lexicographic minimality conceptually."""

    def test_path_begins_with_smallest_value(self):
        """The first element must be 1 (the globally smallest value)."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        result = minPath(grid, 3)
        assert result[0] == 1

    def test_second_element_is_smallest_neighbor_of_1(self):
        """The second element must be the smallest neighbor of 1."""
        grid = [[5, 9, 3], [4, 1, 6], [7, 8, 2]]
        # Neighbors of 1 at (1,1): 9 (up), 6 (right), 8 (down), 4 (left). Min = 4.
        result = minPath(grid, 2)
        assert result[1] == 4

    def test_deterministic_answer(self):
        """For a given grid and k, the answer is deterministic."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        r1 = minPath(grid, 5)
        r2 = minPath(grid, 5)
        assert r1 == r2


class TestMinPathValueRange:
    """Tests ensuring returned values are within valid range."""

    def test_values_within_range(self):
        """All returned values should be in [1, N*N]."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = minPath(grid, 10)
        for val in result:
            assert 1 <= val <= 9

    def test_only_two_values_in_result(self):
        """Result should only contain 1 and the min neighbor of 1."""
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = minPath(grid, 10)
        unique_vals = set(result)
        assert len(unique_vals) == 2
        assert 1 in unique_vals
