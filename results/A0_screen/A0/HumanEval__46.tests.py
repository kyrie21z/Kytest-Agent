import pytest
from solution import fib4


class TestFib4BaseCases:
    """Test the base cases of the fib4 sequence."""

    def test_fib4_zero(self):
        assert fib4(0) == 0

    def test_fib4_one(self):
        assert fib4(1) == 0

    def test_fib4_two(self):
        assert fib4(2) == 2

    def test_fib4_three(self):
        assert fib4(3) == 0


class TestFib4DocstringExamples:
    """Test the examples given in the docstring."""

    def test_fib4_five(self):
        assert fib4(5) == 4

    def test_fib4_six(self):
        assert fib4(6) == 8

    def test_fib4_seven(self):
        assert fib4(7) == 14


class TestFib4Recurrence:
    """Test that fib4 satisfies the recurrence relation for larger n."""

    def test_fib4_four(self):
        # fib4(4) = fib4(3) + fib4(2) + fib4(1) + fib4(0) = 0 + 2 + 0 + 0 = 2
        assert fib4(4) == 2

    def test_fib4_eight(self):
        # fib4(8) = fib4(7) + fib4(6) + fib4(5) + fib4(4) = 14 + 8 + 4 + 2 = 28
        assert fib4(8) == 28

    def test_fib4_nine(self):
        # fib4(9) = fib4(8) + fib4(7) + fib4(6) + fib4(5) = 28 + 14 + 8 + 4 = 54
        assert fib4(9) == 54

    def test_fib4_ten(self):
        # fib4(10) = fib4(9) + fib4(8) + fib4(7) + fib4(6) = 54 + 28 + 14 + 8 = 104
        assert fib4(10) == 104

    def test_fib4_twenty(self):
        assert fib4(20) == 73552

    def test_fib4_fifty(self):
        assert fib4(50) == 26112283777288

    def test_fib4_hundred(self):
        assert fib4(100) == 4647959998589498844128566416

    def test_fib4_large(self):
        assert fib4(200) == 147264284485249952746848558937024255947199569971119911200


class TestFib4PositiveValues:
    """Test that fib4 returns positive integers for n > 2 (except n=3)."""

    @pytest.mark.parametrize("n", range(4, 21))
    def test_positive_for_n_ge_4(self, n):
        result = fib4(n)
        assert isinstance(result, int), f"fib4({n}) should return an int"
        assert result > 0, f"fib4({n}) should be positive for n >= 4"


class TestFib4EdgeCases:
    """Test edge cases and boundary conditions."""

    def test_negative_input_returns_zero(self):
        """Negative inputs fall through the if/elif chain and return 0."""
        assert fib4(-1) == 0
        assert fib4(-5) == 0

    def test_return_type_is_int(self):
        for n in range(0, 20):
            assert isinstance(fib4(n), int), f"fib4({n}) should return an int"


class TestFib4Consistency:
    """Test consistency of the recurrence relation across all computed values."""

    def test_recurrence_holds(self):
        """Verify fib4(n) = fib4(n-1) + fib4(n-2) + fib4(n-3) + fib4(n-4) for n >= 4."""
        values = [fib4(i) for i in range(10)]
        for i in range(4, len(values)):
            expected = values[i - 1] + values[i - 2] + values[i - 3] + values[i - 4]
            assert values[i] == expected, f"Recurrence fails at n={i}"

    def test_monotonic_increase_after_n_3(self):
        """fib4 should be strictly increasing for n >= 4."""
        for n in range(4, 50):
            assert fib4(n) < fib4(n + 1), f"fib4({n}) should be less than fib4({n+1})"
