import pytest
from solution import words_string


class TestWordsString:
    """Tests for the words_string function."""

    # --- Comma-separated words ---

    def test_comma_separated_two_words(self):
        assert words_string("Hi, my") == ["Hi", "my"]

    def test_comma_separated_multiple_words(self):
        assert words_string("One, two, three, four, five, six") == [
            "One",
            "two",
            "three",
            "four",
            "five",
            "six",
        ]

    def test_comma_separated_single_word(self):
        assert words_string("Hello") == ["Hello"]

    # --- Space-separated words ---

    def test_space_separated_words(self):
        assert words_string("Hi, my name is John") == ["Hi", "my", "name", "is", "John"]

    def test_space_separated_only(self):
        assert words_string("one two three") == ["one", "two", "three"]

    # --- Mixed commas and spaces ---

    def test_mixed_separators(self):
        assert words_string("apple, banana orange, grape") == [
            "apple",
            "banana",
            "orange",
            "grape",
        ]

    def test_mixed_with_extra_spaces(self):
        assert words_string("a,  b   c,d") == ["a", "b", "c", "d"]

    # --- Consecutive separators ---

    def test_consecutive_commas(self):
        assert words_string("a,,b") == ["a", "b"]

    def test_consecutive_spaces(self):
        assert words_string("a   b") == ["a", "b"]

    def test_consecutive_mixed_separators(self):
        assert words_string("a, , b") == ["a", "b"]

    # --- Leading / trailing whitespace ---

    def test_leading_trailing_spaces(self):
        assert words_string("  hello world  ") == ["hello", "world"]

    def test_leading_trailing_commas(self):
        assert words_string(",hello,world,") == ["hello", "world"]

    def test_leading_and_trailing_mixed(self):
        assert words_string(" , hello , world , ") == ["hello", "world"]

    # --- Empty input ---

    def test_empty_string(self):
        assert words_string("") == []

    def test_only_spaces(self):
        assert words_string("   ") == []

    def test_only_commas(self):
        assert words_string(",,,") == []

    def test_only_whitespace_and_commas(self):
        assert words_string(" , , ") == []

    # --- Single word edge cases ---

    def test_single_word_no_separator(self):
        assert words_string("Hello") == ["Hello"]

    def test_single_word_with_trailing_comma(self):
        assert words_string("Hello,") == ["Hello"]

    def test_single_word_with_leading_comma(self):
        assert words_string(",Hello") == ["Hello"]

    # --- Special characters in words ---

    def test_words_with_numbers(self):
        assert words_string("abc123, def456") == ["abc123", "def456"]

    def test_words_with_special_chars(self):
        assert words_string("hello-world, foo_bar!") == ["hello-world", "foo_bar!"]

    def test_words_with_punctuation(self):
        assert words_string("Hello!, how are you?") == ["Hello!", "how", "are", "you?"]

    # --- Case sensitivity ---

    def test_mixed_case(self):
        assert words_string("Hello, WORLD, TeSt") == ["Hello", "WORLD", "TeSt"]

    # --- Return type ---

    def test_returns_list(self):
        result = words_string("a, b")
        assert isinstance(result, list)

    def test_returns_list_of_strings(self):
        result = words_string("a, b")
        assert all(isinstance(w, str) for w in result)
