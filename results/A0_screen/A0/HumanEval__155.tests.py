import pytest
from solution import even_odd_count


class TestEvenOddCount:
    """Tests for the even_odd_count function."""

    # --- Basic positive integers ---

    def test_positive_two_digits(self):
        assert even_odd_count(12) == (1, 1)

    def test_positive_three_digits(self):
        assert even_odd_count(123) == (1, 2)

    def test_all_even_digits(self):
        assert even_odd_count(2468) == (4, 0)

    def test_all_odd_digits(self):
        assert even_odd_count(13579) == (0, 5)

    # --- Negative integers ---

    def test_negative_two_digits(self):
        assert even_odd_count(-12) == (1, 1)

    def test_negative_three_digits(self):
        assert even_odd_count(-123) == (1, 2)

    def test_negative_all_even(self):
        assert even_odd_count(-2468) == (4, 0)

    def test_negative_all_odd(self):
        assert even_odd_count(-13579) == (0, 5)

    # --- Zero and single-digit numbers ---

    def test_zero(self):
        assert even_odd_count(0) == (1, 0)

    def test_single_even_digit(self):
        assert even_odd_count(4) == (1, 0)

    def test_single_odd_digit(self):
        assert even_odd_count(7) == (0, 1)

    # --- Larger numbers ---

    def test_large_number(self):
        assert even_odd_count(1234567890) == (5, 5)

    def test_repeated_digits(self):
        assert even_odd_count(1111) == (0, 4)

    def test_repeated_even_digits(self):
        assert even_odd_count(2222) == (4, 0)

    def test_mixed_large_number(self):
        assert even_odd_count(8888811111) == (5, 5)

    # --- Edge cases ---

    def test_one(self):
        assert even_odd_count(1) == (0, 1)

    def test_two(self):
        assert even_odd_count(2) == (1, 0)

    def test_ten(self):
        assert even_odd_count(10) == (1, 1)

    def test_hundred(self):
        assert even_odd_count(100) == (2, 1)

    def test_thousand(self):
        assert even_odd_count(1000) == (3, 1)

    # --- Return type checks ---

    def test_returns_tuple(self):
        result = even_odd_count(123)
        assert isinstance(result, tuple)

    def test_returns_two_elements(self):
        result = even_odd_count(123)
        assert len(result) == 2

    def test_returns_integers(self):
        result = even_odd_count(123)
        assert all(isinstance(x, int) for x in result)
