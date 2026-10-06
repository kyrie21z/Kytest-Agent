import pytest
from solution import is_equal_to_sum_even


class TestIsEqualToSumEven:
    """Tests for is_equal_to_sum_even function."""

    # --- Edge cases around the boundary (n < 8) ---

    @pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5, 6, 7])
    def test_below_minimum(self, n):
        """Numbers below 8 cannot be the sum of 4 positive even numbers."""
        assert is_equal_to_sum_even(n) is False

    @pytest.mark.parametrize("n", [8, 10, 12, 14, 16])
    def test_at_and_above_minimum_even(self, n):
        """Even numbers >= 8 can be expressed as the sum of 4 positive even numbers."""
        assert is_equal_to_sum_even(n) is True

    # --- Odd numbers (never possible) ---

    @pytest.mark.parametrize("n", [1, 3, 5, 7, 9, 11, 13, 15, 17, 19])
    def test_odd_numbers(self, n):
        """Odd numbers can never be the sum of even numbers."""
        assert is_equal_to_sum_even(n) is False

    # --- Larger even numbers ---

    @pytest.mark.parametrize("n", [20, 50, 100, 200, 1000])
    def test_larger_even_numbers(self, n):
        """Larger even numbers should all return True."""
        assert is_equal_to_sum_even(n) is True

    # --- Negative numbers ---

    @pytest.mark.parametrize("n", [-2, -4, -8, -100])
    def test_negative_numbers(self, n):
        """Negative numbers cannot be the sum of positive even numbers."""
        assert is_equal_to_sum_even(n) is False

    # --- Boundary exact values from docstring ---

    def test_docstring_example_4(self):
        assert is_equal_to_sum_even(4) is False

    def test_docstring_example_6(self):
        assert is_equal_to_sum_even(6) is False

    def test_docstring_example_8(self):
        assert is_equal_to_sum_even(8) is True

    # --- Type checking ---

    @pytest.mark.parametrize("n", [2.5, 3.0])
    def test_float_input(self, n):
        """Float inputs may behave differently; just ensure no crash."""
        result = is_equal_to_sum_even(n)
        assert isinstance(result, bool)

    @pytest.mark.parametrize("n", ["8", None])
    def test_invalid_type_input(self, n):
        """Non-numeric inputs (str, None) should raise TypeError."""
        with pytest.raises(TypeError):
            is_equal_to_sum_even(n)

    # --- Property-based style: parity check ---

    @pytest.mark.parametrize("n", range(-10, 21))
    def test_parity_consistency(self, n):
        """Only even numbers >= 8 should return True."""
        result = is_equal_to_sum_even(n)
        if n % 2 != 0:
            assert result is False
        elif n < 8:
            assert result is False
        else:
            assert result is True
