import pytest
from solution import prime_length


class TestPrimeLength:
    """Tests for the prime_length function."""

    # --- Examples from docstring ---
    def test_hello(self):
        assert prime_length('Hello') is True

    def test_abcdcba(self):
        assert prime_length('abcdcba') is True

    def test_kittens(self):
        assert prime_length('kittens') is True

    def test_orange(self):
        assert prime_length('orange') is False

    # --- Edge cases: empty and short strings ---
    def test_empty_string(self):
        """Empty string has length 0, which is not prime."""
        assert prime_length('') is False

    def test_single_char(self):
        """Length 1 is not prime."""
        assert prime_length('a') is False

    def test_two_chars_prime(self):
        """Length 2 is the smallest prime."""
        assert prime_length('ab') is True

    def test_three_chars_prime(self):
        """Length 3 is prime."""
        assert prime_length('abc') is True

    def test_four_chars_not_prime(self):
        """Length 4 is composite."""
        assert prime_length('abcd') is False

    # --- Various non-prime lengths ---
    def test_length_6_not_prime(self):
        assert prime_length('abcdef') is False

    def test_length_8_not_prime(self):
        assert prime_length('abcdefgh') is False

    def test_length_9_not_prime(self):
        assert prime_length('abcdefghi') is False

    def test_length_10_not_prime(self):
        assert prime_length('abcdefghij') is False

    def test_length_12_not_prime(self):
        assert prime_length('abcdefghijkl') is False

    def test_length_14_not_prime(self):
        assert prime_length('abcdefghijklmn') is False

    def test_length_15_not_prime(self):
        assert prime_length('abcdefghijklmno') is False

    def test_length_16_not_prime(self):
        assert prime_length('abcdefghijklmnop') is False

    # --- Various prime lengths ---
    def test_length_5_prime(self):
        assert prime_length('hello') is True

    def test_length_7_prime(self):
        assert prime_length('seven!!') is True

    def test_length_11_prime(self):
        assert prime_length('eleven chars!') is True

    def test_length_13_prime(self):
        assert prime_length('thirteen!!!') is True

    def test_length_17_prime(self):
        assert prime_length('this_is_seventeen') is True

    def test_length_19_prime(self):
        assert prime_length('a' * 19) is True

    def test_length_23_prime(self):
        s = 'a' * 23
        assert prime_length(s) is True

    def test_length_29_prime(self):
        s = 'b' * 29
        assert prime_length(s) is True

    # --- Strings with special characters ---
    def test_special_characters(self):
        """Special characters still count toward length."""
        assert prime_length('!@#$%') is True  # length 5

    def test_spaces(self):
        """Spaces count toward length."""
        assert prime_length('a b c') is True  # length 5

    def test_mixed_content(self):
        """Mixed alphanumeric content."""
        assert prime_length('Test123!') is False  # length 8

    # --- Boundary between primes ---
    def test_length_between_17_and_19(self):
        """Length 18 is not prime."""
        assert prime_length('a' * 18) is False

    def test_length_between_19_and_23(self):
        """Length 20, 21, 22 are not prime."""
        assert prime_length('a' * 20) is False
        assert prime_length('a' * 21) is False
        assert prime_length('a' * 22) is False

    def test_length_between_23_and_29(self):
        """Lengths 24-28 are not prime."""
        for length in range(24, 29):
            assert prime_length('a' * length) is False
