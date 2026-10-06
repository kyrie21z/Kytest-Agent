import pytest
from solution import remove_vowels


class TestRemoveVowels:
    """Tests for the remove_vowels function."""

    # --- Basic functionality ---

    def test_empty_string(self):
        assert remove_vowels("") == ""

    def test_no_vowels(self):
        assert remove_vowels("zbcd") == "zbcd"

    def test_all_vowels_lowercase(self):
        assert remove_vowels("aaaaa") == ""

    def test_all_vowels_uppercase(self):
        assert remove_vowels("AAAAA") == ""

    def test_mixed_case_vowels(self):
        assert remove_vowels("aaBAA") == "B"

    def test_simple_consonant_vowel_mix(self):
        assert remove_vowels("abcdef") == "bcdf"

    def test_multiline_string(self):
        assert remove_vowels("abcdef\nghijklm") == "bcdf\nghjklm"

    # --- Edge cases ---

    def test_single_consonant(self):
        assert remove_vowels("z") == "z"

    def test_single_vowel_lowercase(self):
        assert remove_vowels("a") == ""

    def test_single_vowel_uppercase(self):
        assert remove_vowels("A") == ""

    def test_single_y(self):
        # 'y' is not considered a vowel in this implementation
        assert remove_vowels("y") == "y"

    # --- Vowels only ---

    def test_only_lowercase_vowels(self):
        assert remove_vowels("aeiou") == ""

    def test_only_uppercase_vowels(self):
        assert remove_vowels("AEIOU") == ""

    def test_mixed_vowels(self):
        assert remove_vowels("aEiOu") == ""

    # --- Consonants only ---

    def test_all_consonants(self):
        assert remove_vowels("bcdfghjklmnpqrstvwxyz") == "bcdfghjklmnpqrstvwxyz"

    # --- Mixed content ---

    def test_words_with_spaces(self):
        assert remove_vowels("hello world") == "hll wrld"

    def test_numbers_unchanged(self):
        assert remove_vowels("abc123def") == "bc123df"

    def test_special_characters_unchanged(self):
        assert remove_vowels("!@#$%") == "!@#$%"

    def test_mixed_alphanumeric_and_special(self):
        assert remove_vowels("a1!e@i#o$u%") == "1!@#$%"

    def test_tabs_and_newlines(self):
        result = remove_vowels("a\tb\nc")
        assert result == "\tb\nc"

    def test_preserves_order(self):
        assert remove_vowels("programming") == "prgrmmng"

    def test_repeated_consonants(self):
        assert remove_vowels("bookkeeper") == "bkkpr"

    def test_long_string(self):
        text = "abcdefghijklmnopqrstuvwxyz" * 10
        expected = "bcdfghjklmnpqrstvwxyz" * 10
        assert remove_vowels(text) == expected

    # --- Doctest examples from docstring ---

    def test_doctest_examples(self):
        assert remove_vowels("") == ""
        assert remove_vowels("abcdef\nghijklm") == "bcdf\nghjklm"
        assert remove_vowels("abcdef") == "bcdf"
        assert remove_vowels("aaaaa") == ""
        assert remove_vowels("aaBAA") == "B"
        assert remove_vowels("zbcd") == "zbcd"
