import pytest
from solution import iscube


class TestIscube:
    """Tests for the iscube function."""

    # --- Examples from the docstring ---

    def test_cube_of_1(self):
        assert iscube(1) is True

    def test_not_a_cube_2(self):
        assert iscube(2) is False

    def test_negative_one(self):
        assert iscube(-1) is True

    def test_cube_of_4(self):
        assert iscube(64) is True

    def test_zero(self):
        assert iscube(0) is True

    def test_not_a_cube_180(self):
        assert iscube(180) is False

    # --- Positive perfect cubes ---

    def test_positive_cubes(self):
        """Test various positive perfect cubes."""
        cubes = [
            (1, 1),
            (8, 2),
            (27, 3),
            (64, 4),
            (125, 5),
            (216, 6),
            (343, 7),
            (512, 8),
            (729, 9),
            (1000, 10),
        ]
        for value, base in cubes:
            assert iscube(value) is True, f"{value} ({base}^3) should be a cube"

    def test_larger_positive_cube(self):
        """Test a larger perfect cube."""
        assert iscube(1_000_000) is True  # 100^3
        assert iscube(1_728_000) is True  # 120^3
        assert iscube(92_713_643_576) is True  # 4526^3

    # --- Negative perfect cubes ---

    def test_negative_cubes(self):
        """Test various negative perfect cubes."""
        cubes = [
            (-1, -1),
            (-8, -2),
            (-27, -3),
            (-64, -4),
            (-125, -5),
            (-216, -6),
            (-343, -7),
            (-512, -8),
            (-729, -9),
            (-1000, -10),
        ]
        for value, base in cubes:
            assert iscube(value) is True, f"{value} ({base}^3) should be a cube"

    def test_larger_negative_cube(self):
        """Test a larger negative perfect cube."""
        assert iscube(-1_000_000) is True  # (-100)^3
        assert iscube(-1_728_000) is True  # (-120)^3

    # --- Non-cubes ---

    def test_non_cubes(self):
        """Test integers that are not perfect cubes."""
        non_cubes = [2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        for value in non_cubes:
            assert iscube(value) is False, f"{value} should not be a cube"

    def test_non_cubes_near_perfect_cubes(self):
        """Test values just above/below perfect cubes."""
        # Near 1^3 = 1
        assert iscube(0) is True   # edge case: 0 is a cube
        assert iscube(2) is False
        # Near 2^3 = 8
        assert iscube(7) is False
        assert iscube(9) is False
        # Near 3^3 = 27
        assert iscube(26) is False
        assert iscube(28) is False
        # Near 10^3 = 1000
        assert iscube(999) is False
        assert iscube(1001) is False

    def test_random_non_cubes(self):
        """Test some random-looking numbers that aren't cubes."""
        assert iscube(180) is False
        assert iscube(500) is False
        assert iscube(9999) is False
        assert iscube(12345) is False

    # --- Edge cases ---

    def test_zero_is_cube(self):
        """Zero is 0^3, so it should return True."""
        assert iscube(0) is True

    def test_input_1(self):
        """1 is 1^3, so it should return True."""
        assert iscube(1) is True

    def test_input_minus_1(self):
        """-1 is (-1)^3, so it should return True."""
        assert iscube(-1) is True

    # --- Boundary between cubes and non-cubes ---

    def test_boundary_values(self):
        """Check values right at the boundary of being a cube."""
        # 2^3 = 8
        assert iscube(8) is True
        assert iscube(7) is False
        assert iscube(9) is False

        # 5^3 = 125
        assert iscube(125) is True
        assert iscube(124) is False
        assert iscube(126) is False

        # 10^3 = 1000
        assert iscube(1000) is True
        assert iscube(999) is False
        assert iscube(1001) is False
