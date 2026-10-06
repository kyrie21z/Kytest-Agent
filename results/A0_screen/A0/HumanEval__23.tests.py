import pytest
from solution import strlen


class TestStrLen:
    """Unit tests for the strlen function."""

    def test_empty_string(self):
        """Test that an empty string returns length 0."""
        assert strlen("") == 0

    def test_single_character(self):
        """Test a string with one character."""
        assert strlen("a") == 1

    def test_multiple_characters(self):
        """Test a string with multiple characters."""
        assert strlen("abc") == 3

    def test_longer_string(self):
        """Test a longer string."""
        assert strlen("hello world") == 11

    def test_string_with_spaces(self):
        """Test a string containing spaces."""
        assert strlen("hello   world") == 13

    def test_string_with_numbers(self):
        """Test a string containing digits."""
        assert strlen("abc123") == 6

    def test_string_with_special_characters(self):
        """Test a string containing special characters."""
        assert strlen("!@#$%") == 5

    def test_string_with_unicode(self):
        """Test a string containing unicode characters."""
        assert strlen("你好世界") == 4

    def test_string_with_emoji(self):
        """Test a string containing emoji characters."""
        assert strlen("😀😁😂") == 3

    def test_whitespace_only(self):
        """Test a string consisting only of whitespace."""
        assert strlen("   ") == 3

    def test_newline_and_tabs(self):
        """Test a string with newline and tab characters."""
        assert strlen("\n\t\r") == 3

    def test_single_space(self):
        """Test a string with a single space."""
        assert strlen(" ") == 1

    def test_return_type(self):
        """Test that the return type is int."""
        assert isinstance(strlen("test"), int)

    def test_large_string(self):
        """Test a very large string."""
        s = "a" * 10000
        assert strlen(s) == 10000
