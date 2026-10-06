import pytest
from solution import anti_shuffle


class TestAntiShuffleBasic:
    """Tests for basic functionality of anti_shuffle."""

    def test_single_word_already_sorted(self):
        assert anti_shuffle("Hi") == "Hi"

    def test_single_word_unsorted(self):
        assert anti_shuffle("hello") == "ehllo"

    def test_single_word_with_uppercase_and_lowercase(self):
        # Uppercase letters have lower ASCII values than lowercase
        assert anti_shuffle("ba") == "ab"

    def test_single_word_all_same_chars(self):
        assert anti_shuffle("aaa") == "aaa"

    def test_single_word_one_char(self):
        assert anti_shuffle("a") == "a"


class TestAntiShuffleMultipleWords:
    """Tests for strings with multiple words."""

    def test_two_words(self):
        assert anti_shuffle("abc def") == "abc def"

    def test_two_words_unsorted(self):
        assert anti_shuffle("cba fed") == "abc def"

    def test_preserves_word_order(self):
        # Each single-letter word stays as-is after sorting
        assert anti_shuffle("b a") == "b a"

    def test_mixed_case_multiple_words(self):
        # 'H'=72, 'e'=101, 'l'=108, 'l'=108, 'o'=111 -> already sorted
        # 'W'=87, 'd'=100, 'l'=108, 'o'=111, 'r'=114 -> "Wdlor"
        result = anti_shuffle("Hello World")
        assert result == "Hello Wdlor"


class TestAntiShuffleSpecialCharacters:
    """Tests for strings containing special characters."""

    def test_exclamation_marks(self):
        # ! has ASCII 33, which is less than letters
        assert anti_shuffle("World!!!") == "!!!Wdlor"

    def test_mixed_special_and_letters(self):
        result = anti_shuffle("Hello World!!!")
        assert result == "Hello !!!Wdlor"

    def test_only_special_chars(self):
        # ! = 33, @ = 64, # = 35 -> sorted: !, #, @
        assert anti_shuffle("!@#") == "!#@"

    def test_numbers_and_letters(self):
        # Digits have lower ASCII than uppercase letters
        assert anti_shuffle("b1a") == "1ab"


class TestAntiShuffleWhitespace:
    """Tests for handling whitespace correctly."""

    def test_empty_string(self):
        assert anti_shuffle("") == ""

    def test_single_space(self):
        assert anti_shuffle(" ") == " "

    def test_multiple_spaces_between_words(self):
        # split(" ") preserves empty strings for consecutive spaces
        result = anti_shuffle("a  b")
        assert result == "a  b"

    def test_leading_and_trailing_spaces(self):
        result = anti_shuffle("  hello  ")
        assert result == "  ehllo  "

    def test_only_spaces(self):
        assert anti_shuffle("   ") == "   "


class TestAntiShuffleEdgeCases:
    """Tests for edge cases."""

    def test_long_word(self):
        s = "abcdefghijklmnopqrstuvwxyz"
        assert anti_shuffle(s) == s

    def test_reversed_alphabet(self):
        s = "zyxwvutsrqponmlkjihgfedcba"
        expected = "abcdefghijklmnopqrstuvwxyz"
        assert anti_shuffle(s) == expected

    def test_numeric_string(self):
        assert anti_shuffle("321") == "123"

    def test_mixed_numeric_and_alpha(self):
        # '0'=48, '9'=57, 'A'=65, 'a'=97
        assert anti_shuffle("9a0") == "09a"

    def test_unicode_characters(self):
        # Non-ASCII characters should still be sorted by ord()
        result = anti_shuffle("café")
        assert result == "acfé"

    def test_punctuation_only(self):
        assert anti_shuffle("...") == "..."

    def test_symbol_combination(self):
        assert anti_shuffle("!@#$%") == "!#$%@"


class TestAntiShuffleDocstringExamples:
    """Verify the examples from the docstring work correctly."""

    def test_docstring_example_1(self):
        assert anti_shuffle("Hi") == "Hi"

    def test_docstring_example_2(self):
        assert anti_shuffle("hello") == "ehllo"

    def test_docstring_example_3(self):
        assert anti_shuffle("Hello World!!!") == "Hello !!!Wdlor"
