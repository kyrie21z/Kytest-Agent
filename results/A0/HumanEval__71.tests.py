import pytest
from solution import triangle_area


class TestTriangleAreaValidTriangles:
    """Tests for valid triangles."""

    def test_equilateral_triangle(self):
        """Equilateral triangle with sides 3, 3, 3."""
        assert triangle_area(3, 3, 3) == 3.9

    def test_right_triangle_3_4_5(self):
        """Classic 3-4-5 right triangle."""
        assert triangle_area(3, 4, 5) == 6.0

    def test_right_triangle_5_12_13(self):
        """Another Pythagorean triple."""
        assert triangle_area(5, 12, 13) == 30.0

    def test_isosceles_triangle(self):
        """Isosceles triangle with sides 5, 5, 8."""
        # Height = sqrt(5^2 - 4^2) = 3, area = 0.5 * 8 * 3 = 12
        assert triangle_area(5, 5, 8) == 12.0

    def test_isosceles_triangle_small(self):
        """Isosceles triangle with sides 2, 2, 3."""
        # Semi-perimeter p = 3.5, area = sqrt(3.5 * 1.5 * 1.5 * 0.5) ≈ 1.98
        assert triangle_area(2, 2, 3) == 1.98

    def test_scalene_triangle(self):
        """Scalene triangle with sides 7, 8, 9."""
        result = triangle_area(7, 8, 9)
        assert abs(result - 26.83) < 0.01

    def test_degenerate_almost_valid(self):
        """Triangle very close to degenerate but still valid."""
        result = triangle_area(1, 1, 1.99)
        assert result > 0

    def test_large_triangle(self):
        """Large triangle with bigger side lengths."""
        assert triangle_area(10, 10, 10) == 43.3

    def test_decimal_sides(self):
        """Triangle with decimal side lengths."""
        result = triangle_area(1.5, 2.0, 2.5)
        assert abs(result - 1.5) < 0.01

    def test_unit_triangle(self):
        """Unit equilateral triangle."""
        result = triangle_area(1, 1, 1)
        assert abs(result - 0.43) < 0.01


class TestTriangleAreaInvalidTriangles:
    """Tests for invalid triangles (should return -1)."""

    def test_zero_sides(self):
        """A side of length zero cannot form a triangle."""
        assert triangle_area(0, 0, 0) == -1

    def test_negative_sides(self):
        """Negative side lengths are invalid."""
        assert triangle_area(-1, -2, -3) == -1

    def test_two_sides_equal_third(self):
        """Degenerate triangle: sum of two sides equals third."""
        assert triangle_area(1, 2, 3) == -1

    def test_two_sides_sum_less_than_third(self):
        """Two sides too short to reach across the third."""
        assert triangle_area(1, 2, 10) == -1

    def test_one_side_zero(self):
        """One side is zero."""
        assert triangle_area(0, 5, 5) == -1

    def test_two_zeros(self):
        """Two sides are zero."""
        assert triangle_area(0, 0, 5) == -1

    def test_all_same_invalid(self):
        """All sides equal but not forming a valid triangle (impossible for positive equal sides, but testing edge case)."""
        # For equal positive sides, they always form a valid triangle, so this tests logic differently
        pass

    def test_vastly_different_sides(self):
        """Sides that differ enormously."""
        assert triangle_area(1, 1, 100) == -1

    def test_second_case_from_docstring(self):
        """Example from docstring: triangle_area(1, 2, 10) == -1."""
        assert triangle_area(1, 2, 10) == -1


class TestTriangleAreaEdgeCases:
    """Edge cases and boundary conditions."""

    def test_perfect_square_result(self):
        """Result that rounds cleanly."""
        assert triangle_area(3, 4, 5) == 6.0

    def test_rounding_behavior(self):
        """Ensure rounding to 2 decimal places works correctly."""
        # 5-5-6 triangle: height = sqrt(25-9) = 4, area = 12.0
        assert triangle_area(5, 5, 6) == 12.0

    def test_return_type_float(self):
        """Result should be a float."""
        result = triangle_area(3, 4, 5)
        assert isinstance(result, float)

    def test_return_type_int_for_invalid(self):
        """Invalid triangle returns -1 (int)."""
        result = triangle_area(1, 2, 10)
        assert isinstance(result, int)
        assert result == -1

    def test_order_of_sides_does_not_matter(self):
        """Permuting side order should give same result."""
        assert triangle_area(3, 4, 5) == triangle_area(5, 3, 4)
        assert triangle_area(3, 4, 5) == triangle_area(4, 5, 3)

    def test_all_positive_valid(self):
        """Smallest positive integer sides that form a valid triangle."""
        assert triangle_area(1, 1, 1) > 0

    def test_boundary_validity_a_plus_b_equals_c(self):
        """Exactly at the boundary: a + b == c, should be invalid."""
        assert triangle_area(2, 3, 5) == -1

    def test_boundary_validity_a_plus_b_greater_than_c(self):
        """Just barely valid: a + b > c."""
        assert triangle_area(2, 3, 4) > 0


class TestTriangleAreaDocstringExamples:
    """Verify examples from the docstring."""

    def test_example_1(self):
        """triangle_area(3, 4, 5) == 6.00"""
        assert triangle_area(3, 4, 5) == 6.0

    def test_example_2(self):
        """triangle_area(1, 2, 10) == -1"""
        assert triangle_area(1, 2, 10) == -1
