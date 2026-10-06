import pytest
from solution import max_fill


class TestMaxFillExamples:
    """Tests based on the docstring examples."""

    def test_example_1(self):
        """Example 1: capacity 1, three wells with varying water units."""
        grid = [[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]]
        capacity = 1
        assert max_fill(grid, capacity) == 6

    def test_example_2(self):
        """Example 2: capacity 2, four wells with varying water units."""
        grid = [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]]
        capacity = 2
        assert max_fill(grid, capacity) == 5

    def test_example_3(self):
        """Example 3: no water in any well."""
        grid = [[0, 0, 0], [0, 0, 0]]
        capacity = 5
        assert max_fill(grid, capacity) == 0


class TestMaxFillEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_single_well_single_water_unit(self):
        """One well with exactly one unit of water."""
        grid = [[1]]
        capacity = 1
        assert max_fill(grid, capacity) == 1

    def test_single_well_multiple_water_units(self):
        """One well with multiple units of water."""
        grid = [[1, 1, 1, 1, 1]]
        capacity = 2
        # ceil(5/2) = 3
        assert max_fill(grid, capacity) == 3

    def test_all_zeros_grid(self):
        """Grid with no water at all."""
        grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        capacity = 1
        assert max_fill(grid, capacity) == 0

    def test_capacity_larger_than_any_well(self):
        """Bucket capacity larger than total water in any single well."""
        grid = [[1, 1], [1, 1, 1, 1]]
        capacity = 10
        # ceil(2/10) + ceil(4/10) = 1 + 1 = 2
        assert max_fill(grid, capacity) == 2

    def test_capacity_equals_total_water_in_one_well(self):
        """Capacity exactly equals the water in a well."""
        grid = [[1, 1, 1]]
        capacity = 3
        # ceil(3/3) = 1
        assert max_fill(grid, capacity) == 1

    def test_min_capacity(self):
        """Minimum allowed capacity of 1."""
        grid = [[1, 1, 1], [1, 1]]
        capacity = 1
        # ceil(3/1) + ceil(2/1) = 3 + 2 = 5
        assert max_fill(grid, capacity) == 5

    def test_max_capacity(self):
        """Maximum allowed capacity of 10."""
        grid = [[1] * 10]
        capacity = 10
        # ceil(10/10) = 1
        assert max_fill(grid, capacity) == 1

    def test_single_row_grid(self):
        """Grid with only one row."""
        grid = [[1, 0, 1, 0, 1]]
        capacity = 2
        # ceil(3/2) = 2
        assert max_fill(grid, capacity) == 2

    def test_single_column_grid(self):
        """Grid with only one column per well."""
        grid = [[1], [1], [1], [1]]
        capacity = 1
        # ceil(1/1) * 4 = 4
        assert max_fill(grid, capacity) == 4

    def test_mixed_empty_and_full_wells(self):
        """Mix of empty wells and fully filled wells."""
        grid = [[0, 0, 0], [1, 1, 1], [0, 0], [1, 1, 1, 1, 1]]
        capacity = 2
        # ceil(0/2) + ceil(3/2) + ceil(0/2) + ceil(5/2) = 0 + 2 + 0 + 3 = 5
        assert max_fill(grid, capacity) == 5

    def test_large_grid(self):
        """Larger grid with many wells."""
        grid = [[1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1]]
        capacity = 3
        # ceil(5/3) + ceil(0/3) + ceil(3/3) + ceil(4/3) = 2 + 0 + 1 + 2 = 5
        assert max_fill(grid, capacity) == 5

    def test_exact_division(self):
        """Water amount divides evenly by capacity."""
        grid = [[1, 1, 1, 1, 1, 1]]
        capacity = 3
        # ceil(6/3) = 2
        assert max_fill(grid, capacity) == 2

    def test_remainder_requires_extra_drop(self):
        """Water amount does not divide evenly; extra drop needed."""
        grid = [[1, 1, 1, 1, 1]]
        capacity = 3
        # ceil(5/3) = 2
        assert max_fill(grid, capacity) == 2

    def test_many_empty_rows_with_one_filled(self):
        """Many empty rows with just one non-empty row."""
        grid = [[0, 0], [0, 0], [0, 0], [1, 1, 1], [0, 0]]
        capacity = 1
        # 0 + 0 + 0 + 3 + 0 = 3
        assert max_fill(grid, capacity) == 3

    def test_alternating_pattern(self):
        """Grid with alternating 0s and 1s."""
        grid = [[1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0]]
        capacity = 2
        # ceil(4/2) + ceil(3/2) = 2 + 2 = 4
        assert max_fill(grid, capacity) == 4

    def test_widest_grid(self):
        """Wide grid with many columns."""
        grid = [[1] * 100]
        capacity = 10
        # ceil(100/10) = 10
        assert max_fill(grid, capacity) == 10

    def test_tallest_grid(self):
        """Tall grid with many rows."""
        grid = [[1]] * 100
        capacity = 1
        # ceil(1/1) * 100 = 100
        assert max_fill(grid, capacity) == 100

    def test_both_dimensions_maxed(self):
        """Grid with both dimensions at maximum size."""
        grid = [[1] * 100 for _ in range(100)]
        capacity = 1
        # ceil(100/1) * 100 = 10000
        assert max_fill(grid, capacity) == 10000

    def test_capacity_one_with_no_water(self):
        """Capacity 1 but no water anywhere."""
        grid = [[0] * 50]
        capacity = 1
        assert max_fill(grid, capacity) == 0

    def test_partial_well_with_large_capacity(self):
        """A partially filled well with large capacity."""
        grid = [[1, 1, 1]]
        capacity = 10
        # ceil(3/10) = 1
        assert max_fill(grid, capacity) == 1
