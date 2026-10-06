import pytest
from solution import sum_squares


class TestSumSquares:
    """Unit tests for the sum_squares function."""

    def test_basic_positive_integers(self):
        """Test with basic positive integers as in the docstring examples."""
        assert sum_squares([1, 2, 3]) == 14
        assert sum_squares([1, 4, 9]) == 98
        assert sum_squares([1, 3, 5, 7]) == 84

    def test_float_values(self):
        """Test that floats are ceiling'd before squaring."""
        # ceil(1.4)=2 -> 4, ceil(4.2)=5 -> 25, ceil(0)=0 -> 0 => 29
        assert sum_squares([1.4, 4.2, 0]) == 29

    def test_negative_numbers(self):
        """Test ceiling on negative numbers."""
        # ceil(-2.4)=-2 -> 4, ceil(1)=1 -> 1, ceil(1)=1 -> 1 => 6
        assert sum_squares([-2.4, 1, 1]) == 6

    def test_all_zeros(self):
        """Test with all zeros."""
        assert sum_squares([0, 0, 0]) == 0

    def test_single_element(self):
        """Test with a single-element list."""
        assert sum_squares([5]) == 25
        assert sum_squares([2.1]) == 9  # ceil(2.1)=3, 3^2=9

    def test_empty_list(self):
        """Test with an empty list should return 0."""
        assert sum_squares([]) == 0

    def test_exact_integers_no_ceiling_effect(self):
        """Test that exact integers behave normally."""
        assert sum_squares([2, 3, 4]) == 4 + 9 + 16  # = 29

    def test_negative_floats(self):
        """Test ceiling on various negative floats."""
        # ceil(-1.1) = -1 -> 1, ceil(-5.9) = -5 -> 25 => 26
        assert sum_squares([-1.1, -5.9]) == 26

    def test_large_values(self):
        """Test with larger numbers."""
        lst = [10, 20, 30]
        expected = 10**2 + 20**2 + 30**2  # 100 + 400 + 900 = 1400
        assert sum_squares(lst) == 1400

    def test_mixed_positive_and_negative(self):
        """Test with a mix of positive and negative numbers."""
        # ceil(-3.7)=-3 -> 9, ceil(2.1)=3 -> 9, ceil(0.5)=1 -> 1 => 19
        assert sum_squares([-3.7, 2.1, 0.5]) == 19

    def test_very_small_floats(self):
        """Test with very small positive floats (close to zero)."""
        # ceil(0.001)=1 -> 1, ceil(0.999)=1 -> 1 => 2
        assert sum_squares([0.001, 0.999]) == 2

    def test_identical_elements(self):
        """Test with identical elements in the list."""
        assert sum_squares([3, 3, 3]) == 27  # 3*3*3 = 27
        assert sum_squares([2.5, 2.5, 2.5]) == 27  # ceil(2.5)=3, 3^2*3=27
