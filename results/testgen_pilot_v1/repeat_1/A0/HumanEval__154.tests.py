import unittest
from solution import cycpattern_check


class TestCycpatternCheckBasic(unittest.TestCase):
    """Tests for basic functionality from the docstring examples."""

    def test_false_case_abd_not_in_abcd(self):
        self.assertFalse(cycpattern_check("abcd", "abd"))

    def test_true_case_ell_in_hello(self):
        self.assertTrue(cycpattern_check("hello", "ell"))

    def test_false_case_psus_not_in_whassup(self):
        self.assertFalse(cycpattern_check("whassup", "psus"))

    def test_true_case_baa_rotation_of_baab_in_abab(self):
        self.assertTrue(cycpattern_check("abab", "baa"))

    def test_false_case_eeff_not_in_efef(self):
        self.assertFalse(cycpattern_check("efef", "eeff"))

    def test_true_case_simen_in_himenss(self):
        self.assertTrue(cycpattern_check("himenss", "simen"))


class TestCycpatternCheckEmptyStrings(unittest.TestCase):
    """Tests for edge cases involving empty strings."""

    def test_empty_second_word_returns_true(self):
        self.assertTrue(cycpattern_check("abc", ""))

    def test_empty_first_word_with_nonempty_second_returns_false(self):
        self.assertFalse(cycpattern_check("", "a"))

    def test_both_empty_strings_return_true(self):
        self.assertTrue(cycpattern_check("", ""))


class TestCycpatternCheckEqualStrings(unittest.TestCase):
    """Tests when both words are equal."""

    def test_equal_single_char(self):
        self.assertTrue(cycpattern_check("a", "a"))

    def test_equal_multi_char(self):
        self.assertTrue(cycpattern_check("hello", "hello"))

    def test_equal_long_string(self):
        self.assertTrue(cycpattern_check("abcdefghij", "abcdefghij"))


class TestCycpatternCheckSingleCharacterSecondWord(unittest.TestCase):
    """Tests where the second word is a single character."""

    def test_single_char_present_in_first_word(self):
        self.assertTrue(cycpattern_check("abc", "a"))

    def test_single_char_not_present_in_first_word(self):
        self.assertFalse(cycpattern_check("abc", "d"))

    def test_single_char_at_end(self):
        self.assertTrue(cycpattern_check("abc", "c"))

    def test_single_char_in_middle(self):
        self.assertTrue(cycpattern_check("abc", "b"))


class TestCycpatternCheckRotations(unittest.TestCase):
    """Tests specifically for rotation-based substring matching."""

    def test_rotation_found_at_start(self):
        # "ab" rotated to "ba" should be found in "xaba"
        self.assertTrue(cycpattern_check("xaba", "ab"))

    def test_rotation_found_at_end(self):
        # "ab" rotated to "ba" should be found in "abax"
        self.assertTrue(cycpattern_check("abax", "ab"))

    def test_no_rotation_matches(self):
        # No rotation of "xyz" is a substring of "abc"
        self.assertFalse(cycpattern_check("abc", "xyz"))

    def test_full_rotation_equals_original(self):
        # Rotating "abc" by 3 positions gives "abc" again
        self.assertTrue(cycpattern_check("abcabc", "abc"))

    def test_two_char_word_rotated(self):
        # "ab" -> "ba", "ba" in "xbay"
        self.assertTrue(cycpattern_check("xbay", "ab"))

    def test_three_char_word_all_rotations(self):
        # "abc" rotations: "abc", "bca", "cab"
        # "bca" is in "xbcaz"
        self.assertTrue(cycpattern_check("xbcaz", "abc"))

    def test_four_char_word_rotation(self):
        # "abcd" rotations include "bcda", "cdab", "dabc"
        # "cdab" is in "xxcdabyy"
        self.assertTrue(cycpattern_check("xxcdabyy", "abcd"))


class TestCycpatternCheckSubstringWithoutRotation(unittest.TestCase):
    """Tests where the original (non-rotated) second word is a substring."""

    def test_direct_substring_match(self):
        self.assertTrue(cycpattern_check("abcdef", "cde"))

    def test_direct_substring_at_beginning(self):
        self.assertTrue(cycpattern_check("abcdef", "abc"))

    def test_direct_substring_at_end(self):
        self.assertTrue(cycpattern_check("abcdef", "def"))

    def test_direct_substring_not_found(self):
        self.assertFalse(cycpattern_check("abcdef", "xyz"))


class TestCycpatternCheckLongerWords(unittest.TestCase):
    """Tests with longer input strings."""

    def test_long_second_word_as_substring(self):
        self.assertTrue(
            cycpattern_check(
                "thisisalongstringwithsubstring", "substring"
            )
        )

    def test_long_second_word_not_substring(self):
        self.assertFalse(
            cycpattern_check("short", "longwordthatdoesnotfit")
        )

    def test_second_word_longer_than_first(self):
        self.assertFalse(cycpattern_check("ab", "abcdef"))

    def test_same_length_different_content(self):
        self.assertFalse(cycpattern_check("abc", "def"))

    def test_same_length_same_content(self):
        self.assertTrue(cycpattern_check("abc", "abc"))


class TestCycpatternCheckRepeatedPatterns(unittest.TestCase):
    """Tests with repeated patterns in the first word."""

    def test_repeated_pattern_contains_rotation(self):
        # "abab" contains "bab" which is a rotation of "aba"
        self.assertTrue(cycpattern_check("abab", "aba"))

    def test_repeated_pattern_no_match(self):
        self.assertFalse(cycpattern_check("aaaa", "bbb"))

    def test_alternating_pattern(self):
        # "abab" contains "bab" which is a rotation of "aba"
        self.assertTrue(cycpattern_check("abab", "bab"))


class TestCycpatternCheckSpecialCharacters(unittest.TestCase):
    """Tests with special characters and numbers."""

    def test_numbers_in_words(self):
        self.assertTrue(cycpattern_check("abc123def", "123"))

    def test_special_chars_in_words(self):
        self.assertTrue(cycpattern_check("hello!world", "!wor"))

    def test_mixed_alphanumeric(self):
        self.assertTrue(cycpattern_check("test12345", "2345"))


class TestCycpatternCheckCaseSensitivity(unittest.TestCase):
    """Tests confirming case-sensitive behavior."""

    def test_case_sensitive_no_match(self):
        self.assertFalse(cycpattern_check("ABC", "abc"))

    def test_case_sensitive_match(self):
        self.assertTrue(cycpattern_check("Hello", "ell"))

    def test_case_sensitive_rotation(self):
        self.assertFalse(cycpattern_check("AbCa", "bca"))

    def test_case_sensitive_rotation_upper(self):
        self.assertTrue(cycpattern_check("ABCA", "BCA"))


class TestCycpatternCheckEdgeCases(unittest.TestCase):
    """Additional edge case tests."""

    def test_whitespace_in_first_word(self):
        self.assertTrue(cycpattern_check("hello world", "world"))

    def test_whitespace_in_second_word(self):
        self.assertTrue(cycpattern_check("hello world", " wor"))

    def test_newline_character(self):
        self.assertTrue(cycpattern_check("hello\nworld", "\nwor"))

    def test_unicode_characters(self):
        self.assertTrue(cycpattern_check("héllo wörld", "wör"))

    def test_second_word_longer_but_rotation_shorter(self):
        # Even though b is longer than a, no rotation can fit
        self.assertFalse(cycpattern_check("ab", "abcde"))

    def test_single_letter_first_word(self):
        self.assertTrue(cycpattern_check("a", "a"))

    def test_single_letter_first_word_different(self):
        self.assertFalse(cycpattern_check("a", "b"))


if __name__ == "__main__":
    unittest.main()
