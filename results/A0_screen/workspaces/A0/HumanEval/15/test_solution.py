"""Unit tests for solution.string_sequence."""

import pytest
from solution import string_sequence


class TestStringSequence:
    """Tests for the string_sequence function."""

    def test_zero(self):
        """Test with n = 0, should return '0'."""
        assert string_sequence(0) == "0"

    def test_one(self):
        """Test with n = 1, should return '0 1'."""
        assert string_sequence(1) == "0 1"

    def test_two(self):
        """Test with n = 2, should return '0 1 2'."""
        assert string_sequence(2) == "0 1 2"

    def test_five(self):
        """Test with n = 5, should return '0 1 2 3 4 5'."""
        assert string_sequence(5) == "0 1 2 3 4 5"

    def test_ten(self):
        """Test with n = 10, should return '0 1 2 ... 10'."""
        assert string_sequence(10) == "0 1 2 3 4 5 6 7 8 9 10"

    def test_large_n(self):
        """Test with a larger value of n."""
        assert string_sequence(100) == " ".join(map(str, range(101)))

    def test_returns_string(self):
        """Ensure the return type is str."""
        result = string_sequence(3)
        assert isinstance(result, str)

    def test_no_trailing_or_leading_spaces(self):
        """Ensure no extra spaces at start or end."""
        result = string_sequence(5)
        assert result == result.strip()

    def test_space_delimited(self):
        """Ensure elements are separated by exactly one space."""
        result = string_sequence(5)
        parts = result.split(" ")
        assert len(parts) == 6
        assert all(p.isdigit() for p in parts)

    @pytest.mark.parametrize("n, expected", [
        (0, "0"),
        (1, "0 1"),
        (2, "0 1 2"),
        (5, "0 1 2 3 4 5"),
        (10, "0 1 2 3 4 5 6 7 8 9 10"),
    ])
    def test_parametrized(self, n, expected):
        """Parametrized tests for various inputs."""
        assert string_sequence(n) == expected
