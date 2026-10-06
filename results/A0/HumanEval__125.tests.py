import pytest
from solution import split_words


class TestSplitWordsWhitespace:
    """Tests for splitting on whitespace."""

    def test_single_word_with_trailing_space(self):
        assert split_words("Hello ") == ["Hello"]

    def test_multiple_words_separated_by_spaces(self):
        assert split_words("Hello world!") == ["Hello", "world!"]

    def test_multiple_words(self):
        assert split_words("one two three") == ["one", "two", "three"]

    def test_leading_and_trailing_whitespace(self):
        assert split_words("  hello world  ") == ["hello", "world"]

    def test_tabs_as_whitespace(self):
        assert split_words("hello\tworld") == ["hello", "world"]

    def test_newlines_as_whitespace(self):
        assert split_words("hello\nworld") == ["hello", "world"]

    def test_carriage_return_as_whitespace(self):
        assert split_words("hello\rworld") == ["hello", "world"]

    def test_mixed_whitespace(self):
        result = split_words("hello \n world \r\t foo")
        assert result == ["hello", "world", "foo"]

    def test_single_character_word(self):
        assert split_words("a b c") == ["a", "b", "c"]

    def test_words_with_special_characters(self):
        assert split_words("!@# $%^ &*()") == ["!@#", "$%^", "&*()"]

    def test_numbers_in_words(self):
        assert split_words("abc 123 def") == ["abc", "123", "def"]


class TestSplitWordsComma:
    """Tests for splitting on commas when no whitespace is present."""

    def test_two_words_comma_separated(self):
        assert split_words("Hello,world!") == ["Hello", "world!"]

    def test_multiple_commas(self):
        assert split_words("a,b,c,d") == ["a", "b", "c", "d"]

    def test_empty_string_between_commas(self):
        assert split_words("a,,b") == ["a", "", "b"]

    def test_leading_comma(self):
        assert split_words(",hello,world") == ["", "hello", "world"]

    def test_trailing_comma(self):
        assert split_words("hello,world,") == ["hello", "world", ""]

    def test_only_comma(self):
        assert split_words(",") == ["", ""]

    def test_commas_with_special_chars(self):
        assert split_words("!@#,#$%,&*()") == ["!@#", "#$%", "&*()"]

    def test_commas_with_numbers(self):
        assert split_words("1,2,3,4") == ["1", "2", "3", "4"]

    def test_unicode_comma_split(self):
        assert split_words("café,espresso") == ["café", "espresso"]


class TestSplitWordsLetterCount:
    """Tests for counting lowercase letters with odd alphabetical order.
    
    Odd-order letters: b(1), d(3), f(5), h(7), j(9), l(11), n(13),
                       p(15), r(17), t(19), v(21), x(23), z(25)
    """

    def test_example_from_docstring(self):
        assert split_words("abcdef") == 3  # b, d, f

    def test_no_odd_letters(self):
        # a(0), c(2), e(4) are even order
        assert split_words("ace") == 0

    def test_all_odd_letters(self):
        # b(1), d(3), f(5) are odd order
        assert split_words("bdf") == 3

    def test_single_odd_letter(self):
        assert split_words("b") == 1

    def test_single_even_letter(self):
        assert split_words("a") == 0

    def test_mixed_case_letters(self):
        # Only lowercase counts; uppercase doesn't match islower()
        # b(odd), d(odd), f(odd) => 3
        assert split_words("AbCdEf") == 3

    def test_uppercase_only(self):
        assert split_words("ABCDEF") == 0

    def test_digits_and_special_chars(self):
        # No lowercase letters at all
        assert split_words("12345!@#") == 0

    def test_mixed_content(self):
        # b, d, f in "ab1cd2ef" => 3
        assert split_words("ab1cd2ef") == 3

    def test_all_lowercase_alphabet(self):
        # Count odd-order letters in full alphabet
        # Odd: b, d, f, h, j, l, n, p, r, t, v, x, z = 13
        assert split_words("abcdefghijklmnopqrstuvwxyz") == 13

    def test_repeated_odd_letters(self):
        # b appears twice, both count
        assert split_words("bb") == 2

    def test_empty_string(self):
        assert split_words("") == 0

    def test_whitespace_prevents_letter_count(self):
        # "a b" has whitespace, so it splits instead of counting
        assert split_words("a b") == ["a", "b"]

    def test_comma_prevents_letter_count(self):
        # "a,b" has comma, so it splits instead of counting
        assert split_words("a,b") == ["a", "b"]

    def test_long_string_of_odd_letters(self):
        # All odd letters repeated
        assert split_words("bdfhjlnprtvxz") == 13

    def test_alternating_even_odd(self):
        # a(even), b(odd), c(even), d(odd) => 2
        assert split_words("abcd") == 2


class TestEdgeCases:
    """Additional edge case tests."""

    def test_very_long_string(self):
        txt = "a" * 10000
        assert split_words(txt) == 0  # 'a' has even order

    def test_very_long_odd_letter_string(self):
        txt = "b" * 10000
        assert split_words(txt) == 10000

    def test_string_with_only_newline(self):
        assert split_words("\n") == []

    def test_string_with_only_tab(self):
        assert split_words("\t") == []

    def test_string_with_only_comma(self):
        assert split_words(",") == ["", ""]

    def test_string_with_only_space(self):
        assert split_words(" ") == []

    def test_boolean_like_strings(self):
        assert split_words("true,false") == ["true", "false"]

    def test_numeric_string_no_separator(self):
        assert split_words("123456") == 0  # no lowercase letters

    def test_string_with_both_comma_and_whitespace(self):
        # Whitespace takes priority
        assert split_words("hello, world") == ["hello,", "world"]

    def test_string_with_consecutive_whitespace(self):
        assert split_words("hello   world") == ["hello", "world"]

    def test_string_with_consecutive_commas(self):
        assert split_words("hello,,,world") == ["hello", "", "", "world"]
