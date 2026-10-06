"""Unit tests for solution.car_race_collision using pytest."""

import pytest
from solution import car_race_collision


class TestCarRaceCollision:
    """Tests for the car_race_collision function."""

    @pytest.mark.parametrize("n, expected", [
        (0, 0),
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
        (5, 25),
        (10, 100),
        (100, 10000),
    ])
    def test_formula_n_squared(self, n, expected):
        """Verify that the output equals n² for a range of inputs."""
        assert car_race_collision(n) == expected

    def test_zero_cars(self):
        """With zero cars in each direction, there are no collisions."""
        assert car_race_collision(0) == 0

    def test_one_car_each_direction(self):
        """With one car in each direction, exactly one collision occurs."""
        assert car_race_collision(1) == 1

    def test_large_input(self):
        """Test with a large value of n to ensure correctness."""
        n = 1000
        assert car_race_collision(n) == 1_000_000

    def test_return_type_is_int(self):
        """Ensure the return type is always an integer."""
        assert isinstance(car_race_collision(5), int)
