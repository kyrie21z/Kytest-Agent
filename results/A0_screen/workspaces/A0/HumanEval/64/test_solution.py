"""Unit tests for solution.vowels_count using pytest."""

import pytest
from solution import vowels_count


class TestVowelsCount:
    """Tests for the vowels_count function."""

    # --- Basic vowel counting ---

    def test_empty_string(self):
        assert vowels_count("") == 0

    def test_single_vowel_lowercase(self):
        assert vowels_count("a") == 1

    def test_single_vowel_uppercase(self):
        assert vowels_count("A") == 1

    def test_single_consonant(self):
        assert vowels_count("b") == 0

    def test_no_vowels(self):
        assert vowels_count("xyz") == 0

    def test_all_vowels_lowercase(self):
        assert vowels_count("aeiou") == 5

    def test_all_vowels_uppercase(self):
        assert vowels_count("AEIOU") == 5

    def test_mixed_case_vowels(self):
        assert vowels_count("AeIoU") == 5

    # --- Standard examples from docstring ---

    def test_example_abcde(self):
        assert vowels_count("abcde") == 2

    def test_example_acedy(self):
        assert vowels_count("ACEDY") == 3

    # --- 'y' as a vowel only at the end ---

    def test_y_at_end_lowercase(self):
        """'y' at the end should be counted as a vowel."""
        assert vowels_count("fly") == 1  # only 'y' at end; 'f','l' are consonants

    def test_y_at_end_uppercase(self):
        """'Y' at the end should be counted as a vowel."""
        assert vowels_count("Fly") == 1  # only 'y' at end

    def test_y_not_at_end(self):
        """'y' in the middle should NOT be counted as a vowel."""
        assert vowels_count("yellow") == 2  # 'e' and 'o'; 'y' is not at end (ends with 'w')

    def test_y_in_middle_uppercase(self):
        assert vowels_count("Yellow") == 2  # 'e' and 'o'

    def test_word_ending_with_y_only(self):
        assert vowels_count("by") == 1

    def test_word_ending_with_Y_only(self):
        assert vowels_count("By") == 1

    def test_word_with_multiple_y(self):
        """Only the last 'y' (if at end) counts; internal 'y's don't."""
        assert vowels_count("syzygy") == 1  # only trailing 'y'

    def test_word_with_y_and_regular_vowels(self):
        assert vowels_count("happy") == 2  # 'a' + trailing 'y'

    def test_word_with_Y_and_regular_vowels(self):
        assert vowels_count("Happy") == 2  # 'a' + trailing 'Y'

    # --- Longer words ---

    def test_longer_word(self):
        assert vowels_count("beautiful") == 5  # e, a, u, i, u

    def test_sentence_like_string(self):
        assert vowels_count("hello world") == 3  # e, o, o

    def test_repeated_vowels(self):
        assert vowels_count("eeeee") == 5

    def test_alternating_vowels_and_consonants(self):
        assert vowels_count("ababab") == 3

    def test_consonants_only_long(self):
        assert vowels_count("bcdfghjklmnpqrstvwxyz") == 0  # ends with 'z', no vowels

    def test_uppercase_consonants_only(self):
        assert vowels_count("BCDFGHJKLMNPQRSTVWXZ") == 0

    # --- Edge cases with special characters ---

    def test_with_numbers(self):
        assert vowels_count("a1e2i3o4u5") == 5

    def test_with_special_chars(self):
        assert vowels_count("!@#aeiou$%^") == 5

    def test_whitespace_only(self):
        assert vowels_count("   ") == 0

    def test_newline_in_string(self):
        assert vowels_count("a\ne\ni") == 3

    # --- Case sensitivity ---

    def test_mixed_case_word(self):
        assert vowels_count("HeLLo") == 2  # E, O

    def test_all_uppercase_with_trailing_y(self):
        """STRY: S,T,R are consonants; Y at end counts as vowel."""
        assert vowels_count("STRY") == 1

    def test_complex_mixed(self):
        """CoMpLeX WoRdS: o, e, o => 3 vowels, no trailing y."""
        assert vowels_count("CoMpLeX WoRdS") == 3

    # --- Boundary: single character words ---

    def test_single_y(self):
        assert vowels_count("y") == 1

    def test_single_Y(self):
        assert vowels_count("Y") == 1

    def test_single_a(self):
        assert vowels_count("a") == 1

    def test_single_b(self):
        assert vowels_count("b") == 0

    # --- Idempotency / consistency ---

    def test_consistency_lowercase_vs_uppercase(self):
        """Lowercasing shouldn't change the count (except y handling)."""
        assert vowels_count("abcde") == vowels_count("ABCDE")

    def test_consistency_y_position(self):
        """Moving y away from end should reduce count by 1."""
        assert vowels_count("day") == 2  # a + y(at end)
        assert vowels_count("ady") == 2  # a + y(at end) — same
        assert vowels_count("day") == vowels_count("ady")
