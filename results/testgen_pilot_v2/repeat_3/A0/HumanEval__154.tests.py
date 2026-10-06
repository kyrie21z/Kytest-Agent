import pytest
from solution import cycpattern_check


class TestCycpatternCheck:
    """Tests for the cycpattern_check function."""

    # ---- Docstring examples ----

    def test_docstring_false_1(self):
        assert cycpattern_check("abcd", "abd") is False

    def test_docstring_true_1(self):
        assert cycpattern_check("hello", "ell") is True

    def test_docstring_false_2(self):
        assert cycpattern_check("whassup", "psus") is False

    def test_docstring_true_2(self):
        assert cycpattern_check("abab", "baa") is True

    def test_docstring_false_3(self):
        assert cycpattern_check("efef", "eeff") is False

    def test_docstring_true_3(self):
        assert cycpattern_check("himenss", "simen") is True

    # ---- Exact match cases ----

    def test_exact_match(self):
        assert cycpattern_check("abc", "abc") is True

    def test_exact_match_longer(self):
        assert cycpattern_check("hello world", "hello world") is True

    # ---- Empty string cases ----

    def test_b_empty(self):
        assert cycpattern_check("anything", "") is True

    def test_a_empty_b_not_empty(self):
        assert cycpattern_check("", "a") is False

    def test_both_empty(self):
        assert cycpattern_check("", "") is True

    # ---- Rotation that is a substring ----

    def test_simple_rotation_substring(self):
        # "ab" rotated -> "ba"; "ba" is in "cba"
        assert cycpattern_check("cba", "ab") is True

    def test_rotation_at_start(self):
        # "def" rotated -> "fde"; "fde" is at start of "fdeghi"
        assert cycpattern_check("fdeghi", "def") is True

    def test_rotation_at_end(self):
        # "xyz" rotated -> "yzx"; "yzx" is at end of "abcyzx"
        assert cycpattern_check("abcyzx", "xyz") is True

    def test_full_string_rotation_match(self):
        # "abc" rotated -> "cab"; "cab" is in "xcaby"
        assert cycpattern_check("xcaby", "abc") is True

    # ---- No rotation is a substring ----

    def test_no_rotation_match(self):
        assert cycpattern_check("abcdef", "xyz") is False

    def test_different_length_too_short(self):
        assert cycpattern_check("ab", "abc") is False

    def test_different_length_too_long(self):
        assert cycpattern_check("abc", "abcdef") is False

    # ---- Single character cases ----

    def test_single_char_in_string(self):
        assert cycpattern_check("hello", "h") is True

    def test_single_char_not_in_string(self):
        assert cycpattern_check("hello", "z") is False

    def test_single_char_equal(self):
        assert cycpattern_check("a", "a") is True

    # ---- Repeated / palindrome-like patterns ----

    def test_repeated_pattern(self):
        # "ab" rotations: "ab", "ba"; "ba" is in "abab"
        assert cycpattern_check("abab", "ab") is True

    def test_palindrome_like(self):
        # "aba" rotations: "aba", "baa", "aab"; "baa" is in "xabaa"
        assert cycpattern_check("xabaa", "aba") is True

    # ---- Case sensitivity ----

    def test_case_sensitive_uppercase(self):
        assert cycpattern_check("HELLO", "ell") is False

    def test_case_sensitive_mixed(self):
        # "Hello" contains "lle" (rotation of "ell"), so result is True
        assert cycpattern_check("Hello", "ell") is True

    # ---- Longer rotation strings ----

    def test_longer_rotation_match(self):
        # "abcd" rotations include "bcda", "cdab", "dabc"
        assert cycpattern_check("xyzcdabwv", "abcd") is True

    def test_longer_rotation_no_match(self):
        assert cycpattern_check("xyzabcdwv", "zzzz") is False

    # ---- Whitespace handling ----

    def test_with_spaces_rotation_match(self):
        # "lo wo" rotations: "lo wo", "o wol", "wol o", "ol ow", "low o"
        # "low o" is in "hello world"
        assert cycpattern_check("hello world", "lo wo") is True

    def test_with_spaces_no_match(self):
        # "rld he" rotations don't appear in "hello world"
        assert cycpattern_check("hello world", "rld he") is False

    # ---- Boundary: rotation equals original ----

    def test_all_same_chars(self):
        # "aaa" rotations are all "aaa"
        assert cycpattern_check("aaaaa", "aaa") is True

    def test_all_same_chars_no_match(self):
        assert cycpattern_check("bbb", "aaa") is False
