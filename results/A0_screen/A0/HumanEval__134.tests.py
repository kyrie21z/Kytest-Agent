import pytest
from solution import check_if_last_char_is_a_letter


class TestCheckIfLastCharIsAWordAlone:
    """Tests for check_if_last_char_is_a_letter."""

    # --- Docstring example cases ---

    def test_example_apple_pie(self):
        """'apple pie' ➞ False — last char 'e' is part of word 'pie'."""
        assert check_if_last_char_is_a_letter("apple pie") is False

    def test_example_apple_pi_e(self):
        """'apple pi e' ➞ True — last char 'e' is its own word."""
        assert check_if_last_char_is_a_letter("apple pi e") is True

    def test_example_trailing_space(self):
        """'apple pi e ' ➞ False — ends with space, not a letter."""
        assert check_if_last_char_is_a_letter("apple pi e ") is False

    def test_example_empty_string(self):
        """'' ➞ False — empty string."""
        assert check_if_last_char_is_a_letter("") is False

    # --- Empty / trivial inputs ---

    def test_single_alpha_char(self):
        """Single alphabetical character ➞ True."""
        assert check_if_last_char_is_a_letter("a") is True

    def test_single_uppercase_char(self):
        """Single uppercase alphabetical character ➞ True."""
        assert check_if_last_char_is_a_letter("Z") is True

    def test_single_digit(self):
        """Single digit ➞ False."""
        assert check_if_last_char_is_a_letter("5") is False

    def test_single_punctuation(self):
        """Single punctuation ➞ False."""
        assert check_if_last_char_is_a_letter("!") is False

    def test_single_space(self):
        """Single space ➞ False."""
        assert check_if_last_char_is_a_letter(" ") is False

    # --- Strings ending with a standalone letter (preceded by space) ---

    def test_two_words_last_is_letter(self):
        """'hello a' ➞ True — 'a' is its own word."""
        assert check_if_last_char_is_a_letter("hello a") is True

    def test_two_words_last_is_uppercase(self):
        """'hello A' ➞ True — 'A' is its own word."""
        assert check_if_last_char_is_a_letter("hello A") is True

    def test_many_words_last_is_letter(self):
        """'foo bar baz q' ➞ True — 'q' is its own word."""
        assert check_if_last_char_is_a_letter("foo bar baz q") is True

    def test_double_space_before_letter(self):
        """'hello  x' ➞ True — last char 'x' preceded by space."""
        assert check_if_last_char_is_a_letter("hello  x") is True

    # --- Strings where last char is NOT standalone ---

    def test_word_ends_with_letter_no_space(self):
        """'hello world' ➞ False — 'd' is part of 'world'."""
        assert check_if_last_char_is_a_letter("hello world") is False

    def test_single_word(self):
        """'python' ➞ False — last char is part of the word."""
        assert check_if_last_char_is_a_letter("python") is False

    def test_word_ending_with_vowel(self):
        """'banana' ➞ False — 'a' is part of 'banana'."""
        assert check_if_last_char_is_a_letter("banana") is False

    # --- Strings ending with non-alphabetic characters ---

    def test_ends_with_digit(self):
        """'abc 3' ➞ False — last char is a digit."""
        assert check_if_last_char_is_a_letter("abc 3") is False

    def test_ends_with_multiple_digits(self):
        """'abc 42' ➞ False — last char is a digit."""
        assert check_if_last_char_is_a_letter("abc 42") is False

    def test_ends_with_period(self):
        """'hello.' ➞ False — last char is punctuation."""
        assert check_if_last_char_is_a_letter("hello.") is False

    def test_ends_with_period_after_space(self):
        """'hello . ' ➞ False — last char is space."""
        assert check_if_last_char_is_a_letter("hello . ") is False

    def test_ends_with_comma(self):
        """'say hi,' ➞ False — last char is comma."""
        assert check_if_last_char_is_a_letter("say hi,") is False

    def test_ends_with_question_mark(self):
        """'what?' ➞ False — last char is '?'. """
        assert check_if_last_char_is_a_letter("what?") is False

    def test_ends_with_exclamation(self):
        """'wow!' ➞ False — last char is '!'. """
        assert check_if_last_char_is_a_letter("wow!") is False

    def test_ends_with_hash(self):
        """'tag #' ➞ False — last char is '#'. """
        assert check_if_last_char_is_a_letter("tag #") is False

    def test_ends_with_at_sign(self):
        """'user @' ➞ False — last char is '@'. """
        assert check_if_last_char_is_a_letter("user @") is False

    def test_ends_with_slash(self):
        """'path /' ➞ False — last char is '/'. """
        assert check_if_last_char_is_a_letter("path /") is False

    def test_ends_with_equals(self):
        """'x =' ➞ False — last char is '='. """
        assert check_if_last_char_is_a_letter("x =") is False

    def test_ends_with_underscore(self):
        """'name _' ➞ False — last char is '_'. """
        assert check_if_last_char_is_a_letter("name _") is False

    # --- Trailing whitespace ---

    def test_trailing_spaces(self):
        """'hello   ' ➞ False — ends with spaces."""
        assert check_if_last_char_is_a_letter("hello   ") is False

    def test_only_spaces(self):
        """'   ' ➞ False — only spaces."""
        assert check_if_last_char_is_a_letter("   ") is False

    def test_single_trailing_space(self):
        """'a ' ➞ False — ends with space."""
        assert check_if_last_char_is_a_letter("a ") is False

    # --- Edge cases with special characters in middle ---

    def test_special_char_then_letter(self):
        """'hi! z' ➞ True — 'z' is standalone after space."""
        assert check_if_last_char_is_a_letter("hi! z") is True

    def test_numbers_then_letter(self):
        """'123 7' ➞ True — '7' is a digit, so False."""
        assert check_if_last_char_is_a_letter("123 7") is False

    def test_mixed_middle_then_standalone_letter(self):
        """'ab cd ef g' ➞ True — 'g' is standalone."""
        assert check_if_last_char_is_a_letter("ab cd ef g") is True

    # --- Unicode / accented letters ---

    def test_accented_lowercase(self):
        """'café é' ➞ True — 'é' is alphabetic and standalone."""
        assert check_if_last_char_is_a_letter("café é") is True

    def test_accented_uppercase(self):
        """'café É' ➞ True — 'É' is alphabetic and standalone."""
        assert check_if_last_char_is_a_letter("café É") is True

    # --- Boundary: two-character strings ---

    def test_two_chars_space_and_letter(self):
        """' a' ➞ True — 'a' is standalone."""
        assert check_if_last_char_is_a_letter(" a") is True

    def test_two_chars_letter_and_space(self):
        """'a ' ➞ False — ends with space."""
        assert check_if_last_char_is_a_letter("a ") is False

    def test_two_chars_both_letters(self):
        """'ab' ➞ False — 'b' is part of word 'ab'."""
        assert check_if_last_char_is_a_letter("ab") is False

    def test_two_chars_space_and_digit(self):
        """' 5' ➞ False — '5' is a digit."""
        assert check_if_last_char_is_a_letter(" 5") is False

    def test_two_chars_space_and_punct(self):
        """' !' ➞ False — '!' is punctuation."""
        assert check_if_last_char_is_a_letter(" !") is False

    # --- Longer realistic sentences ---

    def test_sentence_with_final_standalone_letter(self):
        """'The quick brown fox jumps over the lazy dog j' ➞ True."""
        assert check_if_last_char_is_a_letter(
            "The quick brown fox jumps over the lazy dog j"
        ) is True

    def test_sentence_without_standalone_letter(self):
        """'The quick brown fox jumps over the lazy dog' ➞ False."""
        assert check_if_last_char_is_a_letter(
            "The quick brown fox jumps over the lazy dog"
        ) is False

    def test_long_string_all_spaces_except_last(self):
        """'             z' ➞ True — many spaces then standalone 'z'."""
        assert check_if_last_char_is_a_letter("             z") is True

    def test_tabs_in_middle(self):
        """'hello\tworld m' ➞ True — 'm' is standalone after space."""
        assert check_if_last_char_is_a_letter("hello\tworld m") is True
