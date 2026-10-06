"""Unit tests for digitSum function in solution.py."""

import pytest
from solution import digitSum


class TestDigitSumEmptyAndBasic:
    """Tests for empty string and basic inputs."""

    def test_empty_string(self):
        """Empty string should return 0."""
        assert digitSum("") == 0

    def test_single_uppercase(self):
        """Single uppercase character returns its ASCII code."""
        assert digitSum("A") == 65
        assert digitSum("Z") == 90

    def test_single_lowercase(self):
        """Single lowercase character returns 0."""
        assert digitSum("a") == 0
        assert digitSum("z") == 0

    def test_no_uppercase_letters(self):
        """String with no uppercase letters returns 0."""
        assert digitSum("abc") == 0
        assert digitSum("hello world") == 0


class TestDigitSumMixedCase:
    """Tests for mixed case strings."""

    def test_example_abAB(self):
        """digitSum('abAB') => 131 (A=65 + B=66)."""
        assert digitSum("abAB") == 131

    def test_example_abcd(self):
        """digitSum('abcCd') => 67 (C=67)."""
        assert digitSum("abcCd") == 67

    def test_example_helloE(self):
        """digitSum('helloE') => 69 (E=69)."""
        assert digitSum("helloE") == 69

    def test_example_woArBld(self):
        """digitSum('woArBld') => 131 (A=65 + B=66)."""
        assert digitSum("woArBld") == 131

    def test_example_aAaaaXa(self):
        """digitSum('aAaaaXa') => 153 (A=65 + X=88)."""
        assert digitSum("aAaaaXa") == 153

    def test_all_uppercase(self):
        """All uppercase string sums all ASCII codes."""
        # A=65, B=66, C=67 => 198
        assert digitSum("ABC") == 198

    def test_alternating_case(self):
        """Alternating upper/lower case."""
        assert digitSum("AbCdEf") == 65 + 67 + 69  # = 201


class TestDigitSumSpecialCharacters:
    """Tests for strings containing special characters, digits, etc."""

    def test_digits_only(self):
        """Digits have no uppercase status; should return 0."""
        assert digitSum("12345") == 0

    def test_special_characters(self):
        """Special characters are not uppercase; should return 0."""
        assert digitSum("!@#$%") == 0

    def test_mixed_with_special_chars(self):
        """Mix of uppercase, digits, and special characters."""
        assert digitSum("A!1b") == 65  # Only 'A' is uppercase

    def test_spaces(self):
        """Spaces are not uppercase."""
        assert digitSum("A B") == 65 + 66  # A + B

    def test_newlines_and_tabs(self):
        """Whitespace characters are not uppercase."""
        assert digitSum("\n\tA") == 65


class TestDigitSumEdgeCases:
    """Edge case tests."""

    def test_repeated_uppercase(self):
        """Repeated uppercase characters are each counted."""
        assert digitSum("AAA") == 65 * 3  # = 195

    def test_long_string(self):
        """Long string with multiple uppercase letters."""
        s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        expected = sum(ord(ch) for ch in s if ch.isupper())
        assert digitSum(s) == expected

    def test_unicode_uppercase(self):
        """Unicode uppercase characters are handled by Python's isupper()."""
        # é is not considered uppercase by isupper() in most locales
        assert digitSum("é") == 0

    def test_whitespace_only(self):
        """Whitespace-only string returns 0."""
        assert digitSum("   ") == 0
        assert digitSum("\t\n\r") == 0


class TestDigitSumTypeHandling:
    """Tests for type-related edge cases."""

    def test_integer_input_raises_error(self):
        """Passing an integer should raise TypeError or AttributeError."""
        with pytest.raises((AttributeError, TypeError)):
            digitSum(123)

    def test_none_input_raises_error(self):
        """Passing None should raise TypeError or AttributeError."""
        with pytest.raises((AttributeError, TypeError)):
            digitSum(None)

    def test_float_input_raises_error(self):
        """Passing a float should raise TypeError or AttributeError."""
        with pytest.raises((AttributeError, TypeError)):
            digitSum(3.14)

    def test_list_of_ints_raises_error(self):
        """Passing a list of integers should raise TypeError or AttributeError."""
        with pytest.raises((AttributeError, TypeError)):
            digitSum([1, 2, 3])

    def test_tuple_of_ints_raises_error(self):
        """Passing a tuple of integers should raise TypeError or AttributeError."""
        with pytest.raises((AttributeError, TypeError)):
            digitSum((1, 2, 3))
