"""Unit tests for solution.is_palindrome."""

import pytest
from solution import is_palindrome


class TestIsPalindrome:
    """Tests for the is_palindrome function."""

    # --- Basic / Docstring examples ---

    def test_empty_string(self):
        """An empty string is considered a palindrome."""
        assert is_palindrome('') is True

    def test_single_character(self):
        """A single-character string is always a palindrome."""
        assert is_palindrome('a') is True

    def test_simple_odd_length_palindrome(self):
        """Classic odd-length palindrome."""
        assert is_palindrome('aba') is True

    def test_all_same_characters(self):
        """String of identical characters is a palindrome."""
        assert is_palindrome('aaaaa') is True

    def test_non_palindrome(self):
        """A string that reads differently backwards."""
        assert is_palindrome('zbcd') is False

    # --- Even-length palindromes ---

    def test_even_length_palindrome(self):
        """Even-length palindromes should return True."""
        assert is_palindrome('abba') is True

    def test_two_char_palindrome(self):
        """Two identical characters form a palindrome."""
        assert is_palindrome('aa') is True

    def test_two_char_non_palindrome(self):
        """Two different characters are not a palindrome."""
        assert is_palindrome('ab') is False

    # --- Case sensitivity ---

    def test_case_sensitive_mixed_case(self):
        """Mixed-case strings are NOT treated as palindromes."""
        assert is_palindrome('Abba') is False

    def test_case_sensitive_uppercase(self):
        """All-uppercase palindrome."""
        assert is_palindrome('ABA') is True

    def test_case_sensitive_lowercase(self):
        """All-lowercase palindrome."""
        assert is_palindrome('aba') is True

    # --- Palindromes with spaces and punctuation ---

    def test_with_spaces(self):
        """Spaces are included in the comparison."""
        assert is_palindrome('a b a') is True

    def test_sentence_not_palindrome(self):
        """A regular sentence is not a palindrome."""
        assert is_palindrome('hello world') is False

    def test_punctuation_included(self):
        """Punctuation characters are compared literally."""
        assert is_palindrome('a,a') is True
        assert is_palindrome('a,a!') is False

    # --- Longer strings ---

    def test_long_palindrome(self):
        """A longer palindrome string."""
        assert is_palindrome('racecar') is True

    def test_very_long_palindrome(self):
        """A very long palindrome made of repeated patterns."""
        s = 'abcde' * 100 + 'edcba' * 100
        assert is_palindrome(s) is True

    def test_long_non_palindrome(self):
        """A long string that is clearly not a palindrome."""
        assert is_palindrome('abcdefghij') is False

    # --- Numeric-like strings ---

    def test_numeric_string_palindrome(self):
        """Numeric digit strings can be palindromes."""
        assert is_palindrome('12321') is True

    def test_numeric_string_non_palindrome(self):
        """Numeric digit strings that are not palindromes."""
        assert is_palindrome('12345') is False

    # --- Special characters ---

    def test_special_chars_palindrome(self):
        """Strings with special characters can be palindromes."""
        assert is_palindrome('!!!') is True
        assert is_palindrome('a!a') is True

    def test_unicode_palindrome(self):
        """Unicode characters can form palindromes."""
        assert is_palindrome('été') is True

    def test_unicode_non_palindrome(self):
        """Unicode characters that are not palindromes."""
        assert is_palindrome('éà') is False

    # --- Type edge cases ---

    def test_whitespace_only(self):
        """Whitespace-only strings are palindromes."""
        assert is_palindrome('   ') is True

    def test_newline_and_tabs(self):
        """Newlines and tabs are compared literally."""
        assert is_palindrome('\n\n') is True
        assert is_palindrome('\t\t') is True
        assert is_palindrome('\n\t') is False
