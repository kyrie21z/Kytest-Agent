import pytest
from solution import sum_to_n


class TestSumToN:
    """Tests for the sum_to_n function."""

    # --- Docstring examples ---

    def test_sum_to_n_30(self):
        assert sum_to_n(30) == 465

    def test_sum_to_n_100(self):
        assert sum_to_n(100) == 5050

    def test_sum_to_n_5(self):
        assert sum_to_n(5) == 15

    def test_sum_to_n_10(self):
        assert sum_to_n(10) == 55

    def test_sum_to_n_1(self):
        assert sum_to_n(1) == 1

    # --- Edge cases ---

    def test_sum_to_n_zero(self):
        """Sum from 1 to 0 should be 0."""
        assert sum_to_n(0) == 0

    def test_sum_to_n_negative(self):
        """Negative input produces a result via the formula (not necessarily meaningful)."""
        assert sum_to_n(-5) == 10

    def test_sum_to_n_two(self):
        assert sum_to_n(2) == 3

    # --- Larger values ---

    def test_sum_to_n_large(self):
        assert sum_to_n(1000) == 500500

    def test_sum_to_n_very_large(self):
        assert sum_to_n(10000) == 50005000

    # --- Return type ---

    def test_returns_int(self):
        assert isinstance(sum_to_n(10), int)

    # --- Known formula verification ---

    @pytest.mark.parametrize("n, expected", [
        (1, 1),
        (2, 3),
        (3, 6),
        (4, 10),
        (5, 15),
        (10, 55),
        (20, 210),
        (50, 1275),
        (100, 5050),
    ])
    def test_known_values(self, n, expected):
        assert sum_to_n(n) == expected
