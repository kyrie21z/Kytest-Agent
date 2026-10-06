import pytest
from solution import select_words


class TestSelectWords:
    """Tests for the select_words function."""

    # --- Examples from the docstring ---

    def test_example_1(self):
        assert select_words("Mary had a little lamb", 4) == ["little"]

    def test_example_2(self):
        assert select_words("Mary had a little lamb", 3) == ["Mary", "lamb"]

    def test_example_3(self):
        assert select_words("simple white space", 2) == []

    def test_example_4(self):
        assert select_words("Hello world", 4) == ["world"]

    def test_example_5(self):
        assert select_words("Uncle sam", 3) == ["Uncle"]

    # --- Empty / trivial inputs ---

    def test_empty_string(self):
        assert select_words("", 1) == []

    def test_empty_string_n_zero(self):
        assert select_words("", 0) == []

    def test_single_space(self):
        assert select_words(" ", 1) == []

    def test_multiple_spaces(self):
        assert select_words("   ", 1) == []

    # --- n = 0 (words with no consonants — all vowels) ---

    def test_all_vowel_word(self):
        assert select_words("aeiou", 0) == ["aeiou"]

    def test_mixed_vowels_and_consonants_n_zero(self):
        assert select_words("hello aeiou", 0) == ["aeiou"]

    def test_no_all_vowel_words(self):
        assert select_words("hello world", 0) == []

    # --- Single word tests ---

    def test_single_word_matches(self):
        assert select_words("bcdfg", 5) == ["bcdfg"]

    def test_single_word_no_match(self):
        assert select_words("abcde", 5) == []

    def test_single_letter_word(self):
        assert select_words("b", 1) == ["b"]

    def test_single_vowel_word(self):
        assert select_words("a", 0) == ["a"]

    def test_single_vowel_word_wrong_n(self):
        assert select_words("a", 1) == []

    # --- Multiple words, some match ---

    def test_first_word_matches(self):
        assert select_words("bcdfg hello", 5) == ["bcdfg"]

    def test_last_word_matches(self):
        assert select_words("hello bcdfg", 5) == ["bcdfg"]

    def test_middle_word_matches(self):
        assert select_words("hello bcdfg world", 5) == ["bcdfg"]

    def test_all_words_match(self):
        assert select_words("bcdfg ghjkl", 5) == ["bcdfg", "ghjkl"]

    def test_none_match(self):
        assert select_words("hello world", 5) == []

    # --- Case sensitivity ---

    def test_uppercase_consonants_counted(self):
        assert select_words("BCDFG", 5) == ["BCDFG"]

    def test_mixed_case_consonants_counted(self):
        assert select_words("BcDfG", 5) == ["BcDfG"]

    def test_mixed_case_vowels_not_counted(self):
        assert select_words("AeIoU", 0) == ["AeIoU"]

    def test_mixed_case_partial(self):
        result = select_words("Mary had a little lamb", 3)
        assert "Mary" in result
        assert "lamb" in result

    # --- Duplicate words ---

    def test_duplicate_matching_words(self):
        assert select_words("bcdfg bcdfg", 5) == ["bcdfg", "bcdfg"]

    def test_duplicate_non_matching_words(self):
        assert select_words("hello hello", 5) == []

    # --- Edge cases with n ---

    def test_large_n(self):
        assert select_words("hello", 100) == []

    def test_n_equals_word_length_all_consonants(self):
        assert select_words("rst", 3) == ["rst"]

    def test_n_equals_word_length_all_vowels(self):
        assert select_words("aei", 0) == ["aei"]

    # --- Whitespace edge cases ---

    def test_leading_trailing_spaces(self):
        assert select_words("  hello world  ", 4) == ["world"]

    def test_consecutive_spaces(self):
        assert select_words("hello   world", 4) == ["world"]

    def test_spaces_between_matching_words(self):
        assert select_words("bcdfg   ghjkl", 5) == ["bcdfg", "ghjkl"]

    # --- Longer strings ---

    def test_long_sentence_n4(self):
        s = "The quick brown fox jumps over the lazy dog"
        result = select_words(s, 4)
        assert "brown" in result
        assert "jumps" in result

    def test_long_sentence_n3(self):
        s = "The quick brown fox jumps over the lazy dog"
        result = select_words(s, 3)
        assert "quick" in result
        assert "lazy" in result

    def test_order_preserved(self):
        result = select_words("bcdfg abcde ghjkl", 5)
        assert result == ["bcdfg", "ghjkl"]

    # --- Return type check ---

    def test_returns_list(self):
        assert isinstance(select_words("hello", 4), list)

    def test_returns_empty_list_for_no_match(self):
        assert select_words("hello", 4) == []
