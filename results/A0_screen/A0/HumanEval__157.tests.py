import pytest
from solution import right_angle_triangle


class TestRightAngleTriangle:
    """Tests for the right_angle_triangle function."""

    # --- Classic right-angled triangles (should return True) ---

    def test_3_4_5(self):
        """Classic 3-4-5 right triangle."""
        assert right_angle_triangle(3, 4, 5) is True

    def test_5_4_3(self):
        """Same triangle with different ordering."""
        assert right_angle_triangle(5, 4, 3) is True

    def test_4_3_5(self):
        """Another permutation of 3-4-5."""
        assert right_angle_triangle(4, 3, 5) is True

    def test_5_12_13(self):
        """Classic 5-12-13 right triangle."""
        assert right_angle_triangle(5, 12, 13) is True

    def test_8_15_17(self):
        """Classic 8-15-17 right triangle."""
        assert right_angle_triangle(8, 15, 17) is True

    def test_7_24_25(self):
        """Classic 7-24-25 right triangle."""
        assert right_angle_triangle(7, 24, 25) is True

    def test_9_40_41(self):
        """Classic 9-40-41 right triangle."""
        assert right_angle_triangle(9, 40, 41) is True

    def test_6_8_10(self):
        """Scaled 3-4-5 triangle (6-8-10)."""
        assert right_angle_triangle(6, 8, 10) is True

    def test_10_24_26(self):
        """Scaled 5-12-13 triangle (10-24-26)."""
        assert right_angle_triangle(10, 24, 26) is True

    # --- Non-right-angled triangles (should return False) ---

    def test_1_2_3_not_a_triangle(self):
        """Degenerate triangle that can't even form a triangle."""
        assert right_angle_triangle(1, 2, 3) is False

    def test_equilateral_triangle(self):
        """Equilateral triangle is not right-angled."""
        assert right_angle_triangle(1, 1, 1) is False

    def test_obtuse_triangle(self):
        """Obtuse triangle (e.g., 2, 3, 4 where 2²+3² < 4²)."""
        assert right_angle_triangle(2, 3, 4) is False

    def test_acute_triangle(self):
        """Acute triangle (e.g., 4, 5, 6 where all angles < 90°)."""
        assert right_angle_triangle(4, 5, 6) is False

    def test_non_integer_sides(self):
        """Non-integer sides that don't form a right triangle."""
        assert right_angle_triangle(1.5, 2.0, 3.0) is False

    # --- Edge cases ---

    def test_all_zeros(self):
        """All sides zero: 0²+0²==0² evaluates to True due to squaring."""
        assert right_angle_triangle(0, 0, 0) is True

    def test_one_zero_side(self):
        """One side is zero but others aren't: 0²+3²≠4²."""
        assert right_angle_triangle(0, 3, 4) is False

    def test_negative_sides(self):
        """Negative sides: (-3)²+(-4)²==(-5)² evaluates to True due to squaring."""
        assert right_angle_triangle(-3, -4, -5) is True

    def test_mixed_positive_negative(self):
        """Mix of positive and negative: (-3)²+4²==5² evaluates to True."""
        assert right_angle_triangle(-3, 4, 5) is True

    def test_large_values(self):
        """Large integer sides forming a right triangle."""
        assert right_angle_triangle(200, 210, 290) is True

    def test_all_same_nonzero(self):
        """All sides equal and nonzero — equilateral, not right."""
        assert right_angle_triangle(5, 5, 5) is False

    def test_two_equal_sides_not_right(self):
        """Two equal sides but not a right triangle."""
        assert right_angle_triangle(5, 5, 8) is False

    def test_float_right_triangle(self):
        """Float sides that form a right triangle."""
        assert right_angle_triangle(1.5, 2.0, 2.5) is True

    def test_float_right_triangle_permuted(self):
        """Float right triangle with permuted arguments."""
        assert right_angle_triangle(2.5, 1.5, 2.0) is True
