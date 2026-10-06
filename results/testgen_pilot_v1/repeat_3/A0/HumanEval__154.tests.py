import pytest
from solution import cycpattern_check


class TestCycPatternCheckBasic:
    """Tests for basic functionality of cycpattern_check."""

    def test_exact_match(self):
        """When both words are identical, should return True."""
        assert cycpattern_check("hello", "hello") is True

    def test_rotation_in_string(self):
        """When a rotation of b is a substring of a, should return True."""
        # Rotations of "abc": "abc", "bca", "cab"
        assert cycpattern_check("abcde", "cab") is True  # "cab" is rotation of "abc"
        assert cycpattern_check("abcde", "bca") is True  # "bca" is rotation of "abc"
        assert cycpattern_check("abcde", "abc") is True  # "abc" itself is in "abcde"

    def test_substring_not_rotation(self):
        """When b is a substring but not a rotation, should return False."""
        assert cycpattern_check("abcd", "abd") is False
        assert cycpattern_check("efef", "eeff") is False

    def test_no_match(self):
        """When no rotation of b is in a, should return False."""
        assert cycpattern_check("whassup", "psus") is False
        assert cycpattern_check("hello", "xyz") is False


class TestCycPatternCheckFromDocstring:
    """Tests directly from the docstring examples."""

    def test_docstring_example_1(self):
        assert cycpattern_check("abcd", "abd") is False

    def test_docstring_example_2(self):
        assert cycpattern_check("hello", "ell") is True

    def test_docstring_example_3(self):
        assert cycpattern_check("whassup", "psus") is False

    def test_docstring_example_4(self):
        assert cycpattern_check("abab", "baa") is True

    def test_docstring_example_5(self):
        assert cycpattern_check("efef", "eeff") is False

    def test_docstring_example_6(self):
        assert cycpattern_check("himenss", "simen") is True


class TestCycPatternCheckEdgeCases:
    """Tests for edge cases."""

    def test_empty_b(self):
        """Empty b should always return True (empty string is substring of anything)."""
        assert cycpattern_check("hello", "") is True
        assert cycpattern_check("", "") is True

    def test_empty_a_with_nonempty_b(self):
        """Empty a with non-empty b should return False."""
        assert cycpattern_check("", "a") is False
        assert cycpattern_check("", "abc") is False

    def test_single_char_b(self):
        """Single character b should work correctly."""
        assert cycpattern_check("hello", "h") is True
        assert cycpattern_check("hello", "e") is True
        assert cycpattern_check("hello", "z") is False

    def test_single_char_a_and_b_same(self):
        assert cycpattern_check("a", "a") is True

    def test_single_char_a_and_b_different(self):
        assert cycpattern_check("a", "b") is False

    def test_equal_strings(self):
        """When a and b are equal, return True."""
        assert cycpattern_check("abc", "abc") is True
        assert cycpattern_check("aaaa", "aaaa") is True
        assert cycpattern_check("xyz", "xyz") is True


class TestCycPatternCheckRotations:
    """Tests specifically targeting rotation behavior."""

    def test_all_rotations_of_two_char(self):
        """For a 2-char string, all rotations are tested."""
        # Rotations of "ab": "ab", "ba"
        assert cycpattern_check("cba", "ab") is True   # "ab" in "cba"
        assert cycpattern_check("cba", "ba") is True   # "ba" in "cba"
        assert cycpattern_check("xyz", "ab") is False  # neither "ab" nor "ba" in "xyz"

    def test_all_rotations_of_three_char(self):
        """For a 3-char string, all 3 rotations are tested."""
        # Rotations of "abc": "abc", "bca", "cab"
        assert cycpattern_check("xabcx", "abc") is True
        assert cycpattern_check("xbca", "abc") is True
        assert cycpattern_check("xcab", "abc") is True
        assert cycpattern_check("xyz", "abc") is False

    def test_longer_word_b(self):
        """Test with longer b strings."""
        # Rotations of "defga": "defga", "efgad", "fgade", "gade f", "adegf"
        # None of these are substrings of "abcdefg"
        assert cycpattern_check("abcdefg", "defga") is False
        assert cycpattern_check("abcdefg", "efgad") is False
        assert cycpattern_check("abcdefg", "fghij") is False

    def test_repeated_pattern(self):
        """Test with repeated patterns."""
        assert cycpattern_check("abab", "baa") is True  # "aab" is rotation of "baa"
        assert cycpattern_check("aaaa", "aa") is True
        assert cycpattern_check("abcabc", "bcab") is True  # rotation of "abc"

    def test_b_longer_than_a(self):
        """When b is longer than a, no rotation can be a substring."""
        assert cycpattern_check("ab", "abc") is False
        assert cycpattern_check("a", "abc") is False

    def test_b_length_equals_a_length(self):
        """When b has same length as a, only exact match works."""
        assert cycpattern_check("abc", "abc") is True
        # Rotations of "bca": "bca", "cab", "abc" -> "abc" IS in "abc"
        assert cycpattern_check("abc", "bca") is True
        # Rotations of "cab": "cab", "abc", "bca" -> "abc" IS in "abc"
        assert cycpattern_check("abc", "cab") is True
        # Rotations of "acb": "acb", "cba", "bac" -> none in "abc"
        assert cycpattern_check("abc", "acb") is False

    def test_b_longer_than_a_but_equal(self):
        """When b is longer than a, even equal check fails."""
        assert cycpattern_check("a", "aa") is False


class TestCycPatternCheckSpecialCharacters:
    """Tests with special characters and numbers."""

    def test_numbers_in_string(self):
        # Rotations of "453": "453", "534", "345" -> "345" IS in "12345"
        assert cycpattern_check("12345", "345") is True
        assert cycpattern_check("12345", "453") is True
        assert cycpattern_check("12345", "534") is False

    def test_mixed_case(self):
        # Case-sensitive: "world" != "World"
        assert cycpattern_check("HelloWorld", "world") is False
        assert cycpattern_check("HelloWorld", "World") is True
        # Rotations of "rldHe": "rldHe", "ldHer", "dHerl", "Herld", "erldH"
        # None of these are in "HelloWorld"
        assert cycpattern_check("HelloWorld", "rldHe") is False

    def test_uppercase_only(self):
        # Rotations of "CDEFA": "CDEFA", "DEFAC", "EFACD", "FACDE", "ACDEF"
        # None of these are in "ABCDEF"
        assert cycpattern_check("ABCDEF", "CDEFA") is False
        assert cycpattern_check("ABCDEF", "XYZ") is False
