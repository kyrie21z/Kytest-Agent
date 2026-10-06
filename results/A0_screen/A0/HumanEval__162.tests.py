import pytest
from solution import string_to_md5


class TestStringToMd5:
    """Tests for the string_to_md5 function."""

    def test_hello_world(self):
        """Test with the example from the docstring."""
        assert string_to_md5("Hello world") == "3e25960a79dbc69b674cd4ec67a72c62"

    def test_empty_string(self):
        """Empty string should return None."""
        assert string_to_md5("") is None

    def test_single_character(self):
        """Test with a single character string."""
        assert string_to_md5("a") == "0cc175b9c0f1b6a831c399e269772661"

    def test_known_hash(self):
        """Test with a well-known MD5 hash value."""
        assert string_to_md5("abc") == "900150983cd24fb0d6963f7d28e17f72"

    def test_known_hash_2(self):
        """Another well-known MD5 hash value."""
        assert string_to_md5("hello") == "5d41402abc4b2a76b9719d911017c592"

    def test_whitespace_only(self):
        """Test with whitespace-only string (not empty)."""
        assert string_to_md5("   ") == "628631f07321b22d8c176c200c855e1b"

    def test_special_characters(self):
        """Test with special characters."""
        assert string_to_md5("!@#$%^&*()") == "05b28d17a7b6e7024b6e5d8cc43a8bf7"

    def test_unicode_string(self):
        """Test with unicode characters."""
        result = string_to_md5("你好世界")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_long_string(self):
        """Test with a longer string."""
        long_text = "a" * 1000
        result = string_to_md5(long_text)
        assert isinstance(result, str)
        assert len(result) == 32

    def test_returns_string_type(self):
        """Ensure non-empty inputs return a string."""
        result = string_to_md5("test")
        assert isinstance(result, str)

    def test_returns_none_for_empty(self):
        """Ensure empty input returns None, not an empty string."""
        result = string_to_md5("")
        assert result is None

    def test_case_sensitivity(self):
        """MD5 should be case-sensitive."""
        upper = string_to_md5("ABC")
        lower = string_to_md5("abc")
        assert upper != lower

    def test_numbers_as_string(self):
        """Test with numeric string."""
        assert string_to_md5("123") == "202cb962ac59075b964b07152d234b70"

    def test_mixed_content(self):
        """Test with mixed alphanumeric content."""
        assert string_to_md5("Hello World!") == "ed076287532e86365e841e92bfc50d8c"
