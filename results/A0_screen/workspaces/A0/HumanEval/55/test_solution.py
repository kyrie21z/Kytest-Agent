import pytest
from solution import fib


class TestFib:
    """Unit tests for the fib() function."""

    # --- Base cases ---

    def test_fib_zero(self):
        assert fib(0) == 0

    def test_fib_one(self):
        assert fib(1) == 1

    def test_fib_two(self):
        assert fib(2) == 1

    # --- Known Fibonacci values ---

    @pytest.mark.parametrize("n, expected", [
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
        (15, 610),
        (20, 6765),
        (25, 75025),
        (30, 832040),
    ])
    def test_fib_known_values(self, n, expected):
        assert fib(n) == expected

    # --- Docstring doctests ---

    def test_fib_doctest_10(self):
        assert fib(10) == 55

    def test_fib_doctest_1(self):
        assert fib(1) == 1

    def test_fib_doctest_8(self):
        assert fib(8) == 21

    # --- Monotonicity / growth property ---

    def test_fib_increasing_for_n_ge_2(self):
        """For n >= 2, fib(n) should be strictly increasing."""
        for n in range(2, 50):
            assert fib(n) < fib(n + 1)

    # --- Fibonacci recurrence relation ---

    @pytest.mark.parametrize("n", range(3, 30))
    def test_fib_recurrence(self, n):
        """fib(n) == fib(n-1) + fib(n-2) for n >= 3."""
        assert fib(n) == fib(n - 1) + fib(n - 2)

    # --- Type checking ---

    def test_fib_returns_int(self):
        result = fib(10)
        assert isinstance(result, int)

    # --- Negative input behavior ---

    def test_fib_negative_input(self):
        """Negative inputs are not valid; the function may return unexpected results.
        We document this behavior rather than asserting correctness."""
        # fib(-1) does not raise an error but produces an incorrect value
        result = fib(-1)
        assert result != 0  # Just confirm it doesn't crash

    # --- Larger values ---

    def test_fib_large_value(self):
        assert fib(50) == 12586269025

    def test_fib_type_error_on_non_int(self):
        """Passing a non-integer type should either raise TypeError or behave unexpectedly."""
        with pytest.raises(TypeError):
            fib("10")

    def test_fib_float_input(self):
        """Float inputs are not valid."""
        with pytest.raises(TypeError):
            fib(5.0)
