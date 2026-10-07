import pytest
from solution import sum_div


class TestSumDiv:
    """Tests for the sum_div function."""

    # --- Basic / Positive Cases ---

    def test_prime_number(self):
        """Prime numbers have only 1 as a proper divisor."""
        assert sum_div(2) == 1
        assert sum_div(3) == 1
        assert sum_div(5) == 1
        assert sum_div(7) == 1
        assert sum_div(11) == 1
        assert sum_div(13) == 1

    def test_perfect_number(self):
        """A perfect number equals the sum of its proper divisors."""
        assert sum_div(6) == 6   # 1 + 2 + 3
        assert sum_div(28) == 28  # 1 + 2 + 4 + 7 + 14

    def test_abundant_number(self):
        """An abundant number has a divisor sum greater than itself."""
        assert sum_div(12) == 16  # 1 + 2 + 3 + 4 + 6
        assert sum_div(18) == 21  # 1 + 2 + 3 + 6 + 9

    def test_deficient_number(self):
        """A deficient number has a divisor sum less than itself."""
        assert sum_div(4) == 3    # 1 + 2
        assert sum_div(8) == 7    # 1 + 2 + 4
        assert sum_div(9) == 4    # 1 + 3
        assert sum_div(10) == 8   # 1 + 2 + 5

    def test_larger_numbers(self):
        """Test with larger composite numbers."""
        assert sum_div(100) == 117  # 1 + 2 + 4 + 5 + 10 + 20 + 25 + 50
        assert sum_div(49) == 8     # 1 + 7
        assert sum_div(50) == 43    # 1 + 2 + 5 + 10 + 25

    # --- Edge Cases ---

    def test_zero(self):
        """Zero should return 1 (implementation detail: divisors=[1], loop is empty)."""
        assert sum_div(0) == 1

    def test_one(self):
        """One returns 1 (implementation includes 1 in divisors list)."""
        assert sum_div(1) == 1

    # --- Negative Numbers ---

    def test_negative_numbers(self):
        """Negative numbers: loop range is empty, returns 1."""
        assert sum_div(-1) == 1
        assert sum_div(-5) == 1
        assert sum_div(-10) == 1

    # --- Type / Input Validation ---

    def test_non_integer_input_raises_error(self):
        """Non-integer inputs should raise TypeError."""
        with pytest.raises(TypeError):
            sum_div(3.14)
        with pytest.raises(TypeError):
            sum_div("5")
        with pytest.raises(TypeError):
            sum_div(None)

    def test_large_input(self):
        """Test with a large number to ensure performance is acceptable."""
        assert sum_div(10000) == 14211  # 1 + 2 + 4 + 5 + 8 + 10 + ...

    # --- Return Value Properties ---

    def test_return_type_is_int(self):
        """Return value should always be an integer."""
        assert isinstance(sum_div(6), int)
        assert isinstance(sum_div(1), int)
        assert isinstance(sum_div(100), int)

    def test_sum_is_always_positive_for_nonzero(self):
        """For any non-negative input, the result is at least 1."""
        assert sum_div(0) >= 1
        assert sum_div(1) >= 1
        assert sum_div(2) >= 1
        assert sum_div(100) >= 1
