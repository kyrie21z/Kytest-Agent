import pytest
from solution import multiply_int


class TestMultiplyInt:
    """Unit tests for multiply_int function."""

    # --- Basic positive multiplications ---
    def test_positive_positive(self):
        assert multiply_int(2, 3) == 6
        assert multiply_int(3, 4) == 12
        assert multiply_int(5, 5) == 25
        assert multiply_int(10, 10) == 100
        assert multiply_int(7, 8) == 56

    # --- Multiplication by zero ---
    def test_zero_y(self):
        assert multiply_int(5, 0) == 0
        assert multiply_int(-5, 0) == 0
        assert multiply_int(0, 0) == 0

    def test_zero_x(self):
        assert multiply_int(0, 5) == 0
        assert multiply_int(0, -5) == 0
        assert multiply_int(0, 100) == 0

    # --- Negative y values ---
    def test_negative_y(self):
        assert multiply_int(2, -3) == -6
        assert multiply_int(5, -4) == -20
        assert multiply_int(10, -1) == -10

    # --- Both negative ---
    def test_both_negative(self):
        assert multiply_int(-2, -3) == 6
        assert multiply_int(-5, -4) == 20
        assert multiply_int(-1, -1) == 1

    # --- Negative x, positive y ---
    def test_negative_x_positive_y(self):
        assert multiply_int(-2, 3) == -6
        assert multiply_int(-5, 4) == -20
        assert multiply_int(-7, 1) == -7

    # --- Identity cases ---
    def test_multiply_by_one(self):
        assert multiply_int(5, 1) == 5
        assert multiply_int(-5, 1) == -5
        assert multiply_int(1, 5) == 5

    # --- Larger numbers ---
    def test_larger_numbers(self):
        assert multiply_int(100, 100) == 10000
        assert multiply_int(99, 99) == 9801
        assert multiply_int(123, 456) == 56088

    # --- Edge case: single digit ---
    def test_single_digits(self):
        assert multiply_int(1, 1) == 1
        assert multiply_int(9, 9) == 81
        assert multiply_int(1, 9) == 9
        assert multiply_int(9, 1) == 9

    # --- Symmetry / commutativity check ---
    def test_commutativity(self):
        pairs = [
            (2, 3), (5, 7), (-3, 4), (-3, -4), (0, 5), (10, 10)
        ]
        for a, b in pairs:
            assert multiply_int(a, b) == multiply_int(b, a), \
                f"Commutativity failed for {a} * {b}"

    # --- Type consistency ---
    def test_returns_integer(self):
        result = multiply_int(3, 4)
        assert isinstance(result, int)

    # --- Known tricky cases ---
    def test_tricky_cases(self):
        assert multiply_int(-1, 5) == -5
        assert multiply_int(1, -5) == -5
        assert multiply_int(-1, -5) == 5
        assert multiply_int(-1, 1) == -1
        assert multiply_int(1, 1) == 1
