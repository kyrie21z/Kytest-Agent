import pytest
from solution import solve


class TestSolve:
    """Tests for the solve() function which returns the sum of digits of N in binary."""

    # --- Examples from docstring ---

    def test_example_1000(self):
        assert solve(1000) == "1"

    def test_example_150(self):
        assert solve(150) == "110"

    def test_example_147(self):
        assert solve(147) == "1100"

    # --- Edge cases ---

    def test_zero(self):
        """N = 0 should return '0'."""
        assert solve(0) == "0"

    def test_single_digit_one(self):
        """N = 1 should return '1'."""
        assert solve(1) == "1"

    def test_single_digit_nine(self):
        """N = 9 should return '1001' (sum = 9)."""
        assert solve(9) == "1001"

    def test_two_digit_number(self):
        """N = 23 → sum = 5 → '101'."""
        assert solve(23) == "101"

    def test_all_nines_three_digits(self):
        """N = 999 → sum = 27 → '11011'."""
        assert solve(999) == "11011"

    def test_max_constraint(self):
        """N = 10000 → sum = 1 → '1'."""
        assert solve(10000) == "1"

    def test_large_sum(self):
        """N = 9999 → sum = 36 → '100100'."""
        assert solve(9999) == "100100"

    # --- Additional numeric checks ---

    def test_palindrome(self):
        """N = 121 → sum = 4 → '100'."""
        assert solve(121) == "100"

    def test_repeated_digits(self):
        """N = 555 → sum = 15 → '1111'."""
        assert solve(555) == "1111"

    def test_leading_zeros_not_applicable(self):
        """Integers don't have leading zeros; N = 10 → sum = 1 → '1'."""
        assert solve(10) == "1"

    def test_returns_string(self):
        """Result must be a string, not an int or other type."""
        assert isinstance(solve(10), str)

    def test_no_leading_zeros_in_output(self):
        """Binary output should not have unnecessary leading zeros."""
        result = solve(150)
        assert result == result.lstrip("0") or result == "0"

    def test_various_mid_range_values(self):
        """Check several mid-range values."""
        assert solve(50) == "101"     # sum = 5
        assert solve(80) == "1000"    # sum = 8
        assert solve(99) == "10010"   # sum = 18
