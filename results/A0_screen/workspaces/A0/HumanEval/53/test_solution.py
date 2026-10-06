import pytest
from solution import add


class TestAdd:
    """Unit tests for the add function."""

    def test_add_positive_numbers(self):
        assert add(2, 3) == 5
        assert add(1, 1) == 2
        assert add(10, 20) == 30

    def test_add_negative_numbers(self):
        assert add(-2, -3) == -5
        assert add(-1, -1) == -2
        assert add(-10, -20) == -30

    def test_add_mixed_signs(self):
        assert add(-2, 3) == 1
        assert add(2, -3) == -1
        assert add(-5, 5) == 0

    def test_add_with_zero(self):
        assert add(0, 0) == 0
        assert add(5, 0) == 5
        assert add(0, 5) == 5
        assert add(-5, 0) == -5
        assert add(0, -5) == -5

    def test_add_large_numbers(self):
        assert add(1_000_000, 2_000_000) == 3_000_000
        assert add(-1_000_000, 1_000_000) == 0

    def test_add_single_digit(self):
        assert add(0, 0) == 0
        assert add(9, 9) == 18

    def test_add_returns_correct_type(self):
        result = add(1, 2)
        assert isinstance(result, int)
