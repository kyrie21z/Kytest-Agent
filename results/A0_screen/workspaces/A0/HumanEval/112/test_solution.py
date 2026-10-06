import pytest
from solution import reverse_delete


class TestReverseDeleteBasic:
    """Test basic functionality as described in the docstring examples."""

    def test_example_1(self):
        """Example 1: s='abcde', c='ae' -> ('bcd', False)"""
        result = reverse_delete("abcde", "ae")
        assert result == ("bcd", False)

    def test_example_2(self):
        """Example 2: s='abcdef', c='b' -> ('acdef', False)"""
        result = reverse_delete("abcdef", "b")
        assert result == ("acdef", False)

    def test_example_3(self):
        """Example 3: s='abcdedcba', c='ab' -> ('cdedc', True)"""
        result = reverse_delete("abcdedcba", "ab")
        assert result == ("cdedc", True)


class TestReverseDeleteEmptyStrings:
    """Test edge cases with empty strings."""

    def test_empty_s(self):
        """When s is empty, result should be empty string and True (empty is palindrome)."""
        result = reverse_delete("", "abc")
        assert result == ("", True)

    def test_empty_c(self):
        """When c is empty, no characters are deleted; return original string and its palindrome status."""
        result = reverse_delete("abc", "")
        assert result == ("abc", False)

    def test_both_empty(self):
        """Both strings empty."""
        result = reverse_delete("", "")
        assert result == ("", True)


class TestReverseDeletePalindromeCases:
    """Test cases where the filtered result is a palindrome."""

    def test_already_palindrome_no_deletion(self):
        """A palindrome with no matching chars to delete."""
        result = reverse_delete("aba", "x")
        assert result == ("aba", True)

    def test_result_becomes_palindrome(self):
        """Deleting characters results in a palindrome."""
        result = reverse_delete("aabba", "a")
        assert result == ("bb", True)

    def test_single_char_result_is_palindrome(self):
        """Single character result is always a palindrome."""
        result = reverse_delete("abc", "ac")
        assert result == ("b", True)

    def test_all_chars_deleted(self):
        """All characters deleted yields empty string which is a palindrome."""
        result = reverse_delete("abc", "abc")
        assert result == ("", True)

    def test_even_length_palindrome(self):
        """Even-length palindrome after deletion."""
        result = reverse_delete("xyzyx", "x")
        assert result == ("yzy", True)

    def test_odd_length_palindrome(self):
        """Odd-length palindrome after deletion."""
        result = reverse_delete("racecar", "r")
        assert result == ("aceca", True)


class TestReverseDeleteNonPalindromeCases:
    """Test cases where the filtered result is NOT a palindrome."""

    def test_simple_non_palindrome(self):
        """Result is not a palindrome."""
        result = reverse_delete("hello", "h")
        assert result == ("ello", False)

    def test_no_matching_chars_not_palindrome(self):
        """No characters match c, original string is not a palindrome."""
        result = reverse_delete("hello", "xyz")
        assert result == ("hello", False)

    def test_mixed_case_result_not_palindrome(self):
        """Result has mixed characters that don't form a palindrome."""
        result = reverse_delete("abcdefg", "cf")
        assert result == ("abdeg", False)


class TestReverseDeleteMultipleCharsInC:
    """Test with multiple characters in c."""

    def test_multiple_chars_to_delete(self):
        """Delete several different characters."""
        result = reverse_delete("abcdefgh", "bdg")
        # Removing b, d, g from "abcdefgh" leaves "acefh"
        assert result == ("acefh", False)

    def test_duplicate_chars_in_c(self):
        """c contains duplicate characters; each char in c still only needs to match once."""
        result = reverse_delete("abc", "aa")
        assert result == ("bc", False)

    def test_chars_at_beginning_and_end(self):
        """Characters to delete appear at both ends of s."""
        result = reverse_delete("axbycz", "az")
        # Removing a and z from "axbycz" leaves "xbyc"
        assert result == ("xbyc", False)


class TestReverseDeleteSpecialCharacters:
    """Test with special characters and numbers."""

    def test_numbers_in_string(self):
        """String contains digits."""
        result = reverse_delete("12345", "24")
        assert result == ("135", False)

    def test_special_chars_in_string(self):
        """String contains special characters."""
        result = reverse_delete("!@#$%", "!%")
        assert result == ("@#$", False)

    def test_spaces_in_string(self):
        """String contains spaces."""
        result = reverse_delete("a b a", " ")
        assert result == ("aba", True)

    def test_spaces_in_c(self):
        """c contains space character."""
        result = reverse_delete("a b c", " ")
        assert result == ("abc", False)


class TestReverseDeleteReturnTypes:
    """Test that return types are correct."""

    def test_returns_tuple(self):
        """Should return a tuple."""
        result = reverse_delete("abc", "a")
        assert isinstance(result, tuple)

    def test_tuple_has_two_elements(self):
        """Tuple should have exactly two elements."""
        result = reverse_delete("abc", "a")
        assert len(result) == 2

    def test_first_element_is_string(self):
        """First element of tuple should be a string."""
        result = reverse_delete("abc", "a")
        assert isinstance(result[0], str)

    def test_second_element_is_bool(self):
        """Second element of tuple should be a boolean."""
        result = reverse_delete("abc", "a")
        assert isinstance(result[1], bool)


class TestReverseDeleteCaseSensitivity:
    """Test case sensitivity behavior."""

    def test_case_sensitive_matching(self):
        """Matching should be case-sensitive."""
        result = reverse_delete("AbCa", "a")
        # Only lowercase 'a' should be removed, uppercase 'A' remains
        assert result == ("AbC", False)

    def test_uppercase_only(self):
        """All uppercase string."""
        result = reverse_delete("ABCBA", "B")
        assert result == ("ACA", True)


class TestReverseDeleteLongStrings:
    """Test with longer strings."""

    def test_long_palindrome(self):
        """Long palindrome string."""
        long_palindrome = "a" * 100 + "b" + "a" * 100
        result = reverse_delete(long_palindrome, "a")
        assert result == ("b", True)

    def test_long_non_palindrome(self):
        """Long non-palindrome string."""
        long_str = "a" * 50 + "b" * 50
        result = reverse_delete(long_str, "a")
        assert result == ("b" * 50, True)  # All 'b's form a palindrome

    def test_long_with_partial_deletion(self):
        """Long string with partial character deletion."""
        long_str = "abcdefghij" * 10
        result = reverse_delete(long_str, "aei")
        assert isinstance(result, tuple)
        assert isinstance(result[0], str)
        assert isinstance(result[1], bool)
