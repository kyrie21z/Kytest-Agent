import pytest
from solution import is_simple_power


class TestIsSimplePowerBasicCases:
    """Test basic positive-power-of-n scenarios."""

    def test_x_equals_one(self):
        # Any number raised to the power 0 is 1
        assert is_simple_power(1, 4) is True
        assert is_simple_power(1, 2) is True
        assert is_simple_power(1, 10) is True
        assert is_simple_power(1, -3) is True

    def test_n_squared(self):
        assert is_simple_power(4, 2) is True   # 2^2 = 4
        assert is_simple_power(9, 3) is True   # 3^2 = 9
        assert is_simple_power(16, 4) is True  # 4^2 = 16
        assert is_simple_power(25, 5) is True  # 5^2 = 25

    def test_n_cubed(self):
        assert is_simple_power(8, 2) is True   # 2^3 = 8
        assert is_simple_power(27, 3) is True  # 3^3 = 27
        assert is_simple_power(64, 4) is True  # 4^3 = 64

    def test_not_a_power(self):
        assert is_simple_power(3, 2) is False
        assert is_simple_power(5, 3) is False
        assert is_simple_power(10, 2) is False
        assert is_simple_power(7, 3) is False
        assert is_simple_power(12, 4) is False


class TestIsSimplePowerEdgeCases:
    """Test edge cases with special values of n."""

    def test_n_is_zero(self):
        # Note: x==1 always returns True (checked first in implementation)
        assert is_simple_power(0, 0) is True
        assert is_simple_power(0, 5) is False  # 5^k never equals 0
        assert is_simple_power(1, 0) is True   # x==1 check short-circuits
        assert is_simple_power(2, 0) is False
        assert is_simple_power(-1, 0) is False

    def test_n_is_one(self):
        # 1^k = 1 for all k, so only x==1 should return True
        assert is_simple_power(1, 1) is True
        assert is_simple_power(0, 1) is False
        assert is_simple_power(2, 1) is False
        assert is_simple_power(-1, 1) is False

    def test_n_is_negative_one(self):
        # (-1)^k alternates between -1 and 1
        assert is_simple_power(1, -1) is True
        assert is_simple_power(-1, -1) is True
        assert is_simple_power(0, -1) is False
        assert is_simple_power(2, -1) is False
        assert is_simple_power(-2, -1) is False


class TestIsSimplePowerNegativeX:
    """Test scenarios where x is negative."""

    def test_negative_x_positive_n(self):
        # A positive base cannot produce a negative result
        assert is_simple_power(-1, 2) is False
        assert is_simple_power(-4, 2) is False
        assert is_simple_power(-8, 2) is False

    def test_negative_x_negative_n(self):
        # Negative base can produce negative results for odd powers
        assert is_simple_power(-8, -2) is True   # (-2)^3 = -8
        assert is_simple_power(-27, -3) is True  # (-3)^3 = -27
        assert is_simple_power(-8, 2) is False   # 2^k is always positive
        assert is_simple_power(-27, 3) is False  # 3^k is always positive


class TestIsSimplePowerLargeValues:
    """Test with larger numbers to ensure correctness."""

    def test_large_powers(self):
        assert is_simple_power(1024, 2) is True   # 2^10 = 1024
        assert is_simple_power(65536, 2) is True  # 2^16 = 65536
        assert is_simple_power(81, 3) is True     # 3^4 = 81
        assert is_simple_power(625, 5) is True    # 5^4 = 625
        assert is_simple_power(1000, 10) is True  # 10^3 = 1000

    def test_large_not_a_power(self):
        assert is_simple_power(1025, 2) is False
        assert is_simple_power(1000, 2) is False
        assert is_simple_power(100, 3) is False


class TestIsSimplePowerTypeAndBoundary:
    """Test boundary conditions and type behavior."""

    def test_x_equals_n(self):
        # n^1 = n
        assert is_simple_power(2, 2) is True
        assert is_simple_power(5, 5) is True
        assert is_simple_power(10, 10) is True

    def test_x_greater_than_any_power(self):
        assert is_simple_power(100, 2) is False
        assert is_simple_power(1000, 2) is False  # 2^9=512, 2^10=1024

    def test_x_less_than_n(self):
        assert is_simple_power(1, 2) is True   # 2^0 = 1
        assert is_simple_power(2, 4) is False  # 4^0=1, 4^1=4, no match
        assert is_simple_power(3, 5) is False
