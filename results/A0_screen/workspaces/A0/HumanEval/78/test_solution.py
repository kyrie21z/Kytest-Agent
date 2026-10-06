import pytest
from solution import hex_key


class TestHexKey:
    """Tests for the hex_key function."""

    def test_example_ab(self):
        """Example: AB -> 1 (B is prime)"""
        assert hex_key("AB") == 1

    def test_example_1077e(self):
        """Example: 1077E -> 2 (two 7s are prime)"""
        assert hex_key("1077E") == 2

    def test_example_abed1a33(self):
        """Example: ABED1A33 -> 4 (B, D, 3, 3 are prime)"""
        assert hex_key("ABED1A33") == 4

    def test_example_long(self):
        """Example: 123456789ABCDEF0 -> 6 (2, 3, 5, 7, B, D)"""
        assert hex_key("123456789ABCDEF0") == 6

    def test_example_2020(self):
        """Example: 2020 -> 2 (two 2s are prime)"""
        assert hex_key("2020") == 2

    def test_empty_string(self):
        """Empty string should return 0."""
        assert hex_key("") == 0

    def test_no_prime_digits(self):
        """String with no prime hex digits."""
        assert hex_key("014689ACF") == 0

    def test_all_prime_digits(self):
        """String with all prime hex digits."""
        assert hex_key("2357BD") == 6

    def test_single_prime_digit(self):
        """Single prime digit."""
        assert hex_key("2") == 1
        assert hex_key("3") == 1
        assert hex_key("5") == 1
        assert hex_key("7") == 1
        assert hex_key("B") == 1
        assert hex_key("D") == 1

    def test_single_non_prime_digit(self):
        """Single non-prime digit."""
        assert hex_key("0") == 0
        assert hex_key("1") == 0
        assert hex_key("4") == 0
        assert hex_key("6") == 0
        assert hex_key("8") == 0
        assert hex_key("9") == 0
        assert hex_key("A") == 0
        assert hex_key("C") == 0
        assert hex_key("E") == 0
        assert hex_key("F") == 0

    def test_mixed_case_input(self):
        """Test with lowercase letters (should still work since they're not in '2357BD')."""
        # Lowercase letters won't match uppercase primes, so result is 0
        assert hex_key("ab") == 0
        assert hex_key("abcdef") == 0

    def test_repeated_primes(self):
        """Multiple occurrences of the same prime digit."""
        assert hex_key("BBBBBB") == 6
        assert hex_key("DDDDDD") == 6
        assert hex_key("222222") == 6

    def test_alternating_primes_and_non_primes(self):
        """Alternating pattern."""
        assert hex_key("2A3B5C7D") == 6

    def test_leading_zeros(self):
        """Leading zeros should not affect count."""
        assert hex_key("0002") == 1
        assert hex_key("0000") == 0

    def test_trailing_zeros(self):
        """Trailing zeros should not affect count."""
        assert hex_key("2000") == 1
        assert hex_key("B000") == 1

    def test_large_input(self):
        """Large input with many digits."""
        long_hex = "2357BD" * 100  # 600 characters, 600 prime digits
        assert hex_key(long_hex) == 600
