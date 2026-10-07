import pytest
from solution import multiply_int


class TestMultiplyInt:
    """Tests for the multiply_int function."""

    # --- Basic positive multiplications ---
    def test_multiply_positive_by_positive(self):
        assert multiply_int(3, 4) == 12

    def test_multiply_positive_by_one(self):
        assert multiply_int(7, 1) == 7

    def test_multiply_one_by_positive(self):
        assert multiply_int(1, 5) == 5

    def test_multiply_by_zero_y(self):
        assert multiply_int(9, 0) == 0

    def test_multiply_zero_x(self):
        assert multiply_int(0, 8) == 0

    def test_multiply_both_zero(self):
        assert multiply_int(0, 0) == 0

    # --- Negative y values ---
    def test_multiply_negative_y(self):
        assert multiply_int(3, -4) == -12

    def test_multiply_both_negative(self):
        assert multiply_int(-3, -4) == 12

    def test_multiply_negative_x_positive_y(self):
        assert multiply_int(-3, 4) == -12

    def test_multiply_negative_x_negative_y(self):
        assert multiply_int(-5, -6) == 30

    def test_multiply_negative_y_equals_one(self):
        assert multiply_int(7, -1) == -7

    def test_multiply_negative_y_equals_zero(self):
        assert multiply_int(7, 0) == 0

    # --- Edge cases ---
    def test_multiply_large_numbers(self):
        assert multiply_int(100, 100) == 10000

    def test_multiply_small_negative(self):
        assert multiply_int(-1, -1) == 1

    def test_multiply_negative_one_by_positive(self):
        assert multiply_int(-1, 5) == -5

    def test_multiply_positive_by_negative_one(self):
        assert multiply_int(5, -1) == -5

    # --- Idempotency / commutativity checks (within recursion limits) ---
    def test_commutative_3_times_5(self):
        assert multiply_int(3, 5) == multiply_int(5, 3)

    def test_commutative_negative_values(self):
        assert multiply_int(-3, 4) == multiply_int(4, -3)

    def test_commutative_both_negative(self):
        assert multiply_int(-3, -4) == multiply_int(-4, -3)
