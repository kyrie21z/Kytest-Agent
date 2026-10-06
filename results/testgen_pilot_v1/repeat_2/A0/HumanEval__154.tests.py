import pytest
from solution import cycpattern_check


class TestCycpatternCheck:
    """Tests for the cycpattern_check function."""

    # ---- Provided examples from docstring ----

    def test_example_1(self):
        """abcd does not contain abd or any rotation of abd as substring."""
        assert cycpattern_check("abcd", "abd") is False

    def test_example_2(self):
        """hello contains ell as substring."""
        assert cycpattern_check("hello", "ell") is True

    def test_example_3(self):
        """whassup does not contain psus or any rotation of psus as substring."""
        assert cycpattern_check("whassup", "psus") is False

    def test_example_4(self):
        """abab contains baa (rotation of ab) ... actually baa is rotation of ab? No.
        baa is NOT a rotation of ab. But wait - let me re-check.
        Rotations of 'baa': baa, aab, aba. 'aba' IS in 'abab'. So True."""
        assert cycpattern_check("abab", "baa") is True

    def test_example_5(self):
        """efef does not contain eeff or any rotation of eeff."""
        assert cycpattern_check("efef", "eeff") is False

    def test_example_6(self):
        """himenss contains simen (rotation of himenss? no, rotation of simen).
        Rotations of 'simen': simen, imens, mensi, ensim, nsime.
        'imens' is in 'himenss'? h-i-m-e-n-s-s -> 'imens' at index 2. Yes!"""
        assert cycpattern_check("himenss", "simen") is True

    # ---- Edge cases ----

    def test_empty_b(self):
        """Empty second word should return True."""
        assert cycpattern_check("hello", "") is True

    def test_both_empty(self):
        """Both words empty should return True."""
        assert cycpattern_check("", "") is True

    def test_single_char_match(self):
        """Single character that matches."""
        assert cycpattern_check("abc", "a") is True

    def test_single_char_no_match(self):
        """Single character that doesn't match."""
        assert cycpattern_check("abc", "d") is False

    def test_a_equals_b(self):
        """When both words are identical, return True."""
        assert cycpattern_check("hello", "hello") is True

    def test_a_equals_b_single_char(self):
        """Single char identical strings."""
        assert cycpattern_check("x", "x") is True

    def test_b_longer_than_a(self):
        """If b is longer than a, it can never be a substring."""
        assert cycpattern_check("ab", "abcdef") is False

    def test_b_longer_than_a_with_rotation(self):
        """Even with rotation, b longer than a means no match."""
        assert cycpattern_check("abc", "abcdef") is False

    # ---- Rotation-specific tests ----

    def test_first_rotation_matches(self):
        """First rotation (no shift) matches directly."""
        assert cycpattern_check("xyzabc", "abc") is True

    def test_second_rotation_matches(self):
        """Second rotation ('bca') is in 'xbcaz'."""
        assert cycpattern_check("xbcaz", "abc") is True

    def test_third_rotation_matches(self):
        """Third rotation ('cab') is in 'xcaby'."""
        assert cycpattern_check("xcaby", "abc") is True

    def test_all_rotations_checked(self):
        """Verify all rotations are checked by testing a case where only one works."""
        # Rotations of 'def': def, efd, fde
        # 'fde' is in 'xfdez' but 'def' and 'efd' are not
        assert cycpattern_check("xfdez", "def") is True

    def test_no_rotation_matches(self):
        """No rotation of b is a substring of a."""
        assert cycpattern_check("abc", "xyz") is False

    # ---- Two-character patterns ----

    def test_two_char_exact_match(self):
        """Two-char exact match."""
        assert cycpattern_check("ab", "ab") is True

    def test_two_char_rotation_match(self):
        """Rotation of two-char string: 'ba' rotated is 'ab', which is in 'xab'."""
        assert cycpattern_check("xab", "ba") is True

    def test_two_char_no_match(self):
        """Two-char string with no matching rotation."""
        assert cycpattern_check("cd", "ab") is False

    # ---- Longer patterns ----

    def test_long_pattern_full_match(self):
        """Long pattern fully contained."""
        assert cycpattern_check("abcdefghij", "cdefgh") is True

    def test_long_pattern_rotation_match(self):
        """Long pattern where a rotation is found."""
        # Rotations of 'fghij': fghij, ghijf, hijfg, ijfgh, jfghi
        # 'hijfg' is in 'ahijfgk'
        assert cycpattern_check("ahijfgk", "fghij") is True

    def test_long_pattern_no_match(self):
        """Long pattern with no matching rotation."""
        assert cycpattern_check("abcdefghij", "klmnop") is False

    # ---- Repeated characters ----

    def test_repeated_chars_in_b(self):
        """Pattern with repeated characters."""
        # Rotations of 'aa': aa, aa (same). 'aa' is in 'baac'.
        assert cycpattern_check("baac", "aa") is True

    def test_all_same_chars_in_b(self):
        """All same characters in b."""
        assert cycpattern_check("aaaa", "aaa") is True

    def test_all_same_chars_no_match(self):
        """All same chars in b but not present in a."""
        assert cycpattern_check("abc", "ddd") is False

    # ---- Boundary conditions ----

    def test_b_length_one_in_multi_char_a(self):
        """Single char b in multi-char a."""
        assert cycpattern_check("python", "t") is True

    def test_b_length_one_not_in_a(self):
        """Single char b not in a."""
        assert cycpattern_check("python", "z") is False

    def test_a_is_single_char_matching(self):
        """a is single char and matches b."""
        assert cycpattern_check("a", "a") is True

    def test_a_is_single_char_not_matching(self):
        """a is single char and doesn't match b."""
        assert cycpattern_check("a", "b") is False

    # ---- Special characters / whitespace ----

    def test_whitespace_in_strings(self):
        """Strings containing whitespace."""
        assert cycpattern_check("hello world", "world") is True

    def test_whitespace_in_b(self):
        """Whitespace in b that forms part of rotation."""
        assert cycpattern_check("o w", "wo ") is True  # rotation of "wo " includes " o"

    # ---- Case sensitivity ----

    def test_case_sensitive(self):
        """Function is case-sensitive."""
        assert cycpattern_check("Hello", "hello") is False

    def test_case_sensitive_uppercase(self):
        """Uppercase match."""
        assert cycpattern_check("HELLO", "ELL") is True
