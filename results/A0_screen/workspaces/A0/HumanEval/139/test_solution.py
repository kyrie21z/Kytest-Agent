import pytest
from solution import special_factorial


class TestSpecialFactorial:
    """Unit tests for the special_factorial function."""

    # --- Basic correctness tests ---

    def test_special_factorial_one(self):
        """special_factorial(1) = 1! = 1"""
        assert special_factorial(1) == 1

    def test_special_factorial_two(self):
        """special_factorial(2) = 2! * 1! = 2"""
        assert special_factorial(2) == 2

    def test_special_factorial_three(self):
        """special_factorial(3) = 3! * 2! * 1! = 12"""
        assert special_factorial(3) == 12

    def test_special_factorial_four(self):
        """special_factorial(4) = 4! * 3! * 2! * 1! = 288"""
        assert special_factorial(4) == 288

    def test_special_factorial_five(self):
        """special_factorial(5) = 5! * 4! * 3! * 2! * 1! = 34560"""
        assert special_factorial(5) == 34560

    def test_special_factorial_six(self):
        """special_factorial(6) = 6! * 5! * 4! * 3! * 2! * 1! = 24883200"""
        assert special_factorial(6) == 24883200

    # --- Larger input tests ---

    def test_special_factorial_ten(self):
        """Test with a larger input value."""
        result = special_factorial(10)
        assert isinstance(result, int)
        assert result > 0

    def test_special_factorial_twenty(self):
        """Test with an even larger input value."""
        result = special_factorial(20)
        assert isinstance(result, int)
        assert result > 0

    # --- Return type checks ---

    def test_returns_integer(self):
        """The function should return an integer."""
        assert isinstance(special_factorial(4), int)

    def test_returns_positive_for_valid_input(self):
        """For n > 0, the result should always be positive."""
        for n in range(1, 11):
            assert special_factorial(n) > 0

    # --- Invalid / edge-case input tests ---

    def test_zero_returns_one(self):
        """special_factorial(0) returns 1 since the loop does not execute."""
        assert special_factorial(0) == 1

    def test_negative_returns_one(self):
        """special_factorial(-1) returns 1 since the loop does not execute."""
        assert special_factorial(-1) == 1

    def test_non_integer_raises_error(self):
        """Passing a float should raise an error."""
        with pytest.raises(Exception):
            special_factorial(4.5)

    def test_string_raises_error(self):
        """Passing a string should raise an error."""
        with pytest.raises(Exception):
            special_factorial("4")

    def test_none_raises_error(self):
        """Passing None should raise an error."""
        with pytest.raises(Exception):
            special_factorial(None)
