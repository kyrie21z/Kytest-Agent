import pytest
from solution import is_palindrome, make_palindrome


# ---------------------------------------------------------------------------
# is_palindrome tests
# ---------------------------------------------------------------------------

class TestIsPalindrome:
    """Tests for the is_palindrome function."""

    def test_empty_string(self):
        assert is_palindrome("") is True

    def test_single_character(self):
        assert is_palindrome("a") is True

    def test_two_same_characters(self):
        assert is_palindrome("aa") is True

    def test_two_different_characters(self):
        assert is_palindrome("ab") is False

    def test_odd_length_palindrome(self):
        assert is_palindrome("aba") is True

    def test_even_length_palindrome(self):
        assert is_palindrome("abba") is True

    def test_longer_palindrome(self):
        assert is_palindrome("racecar") is True

    def test_non_palindrome(self):
        assert is_palindrome("hello") is False

    def test_non_palindrome_simple(self):
        assert is_palindrome("abc") is False

    def test_case_sensitive(self):
        assert is_palindrome("Abba") is False

    def test_mixed_case_not_palindrome(self):
        assert is_palindrome("Racecar") is False

    def test_all_same_characters(self):
        assert is_palindrome("aaaa") is True

    def test_single_word(self):
        assert is_palindrome("level") is True

    def test_with_spaces(self):
        # Spaces are part of the string, so "a b" != "b a"
        assert is_palindrome("a b") is False

    def test_space_only(self):
        assert is_palindrome(" ") is True

    def test_special_characters(self):
        assert is_palindrome("!") is True

    def test_special_characters_palindrome(self):
        assert is_palindrome("!!") is True

    def test_numeric_string(self):
        assert is_palindrome("12321") is True

    def test_numeric_string_not_palindrome(self):
        assert is_palindrome("12345") is False


# ---------------------------------------------------------------------------
# make_palindrome tests
# ---------------------------------------------------------------------------

class TestMakePalindrome:
    """Tests for the make_palindrome function."""

    def test_empty_string(self):
        assert make_palindrome("") == ""

    def test_single_character(self):
        assert make_palindrome("a") == "a"

    def test_already_palindrome(self):
        assert make_palindrome("aba") == "aba"

    def test_even_length_palindrome(self):
        assert make_palindrome("abba") == "abba"

    def test_no_palindromic_suffix_longer_than_1(self):
        """'cat' has no palindromic suffix longer than 't', so append reverse of 'ca'."""
        assert make_palindrome("cat") == "catac"

    def test_partial_palindromic_suffix(self):
        """'cata' — longest palindromic suffix is 'a', prepend reverse of 'cat'."""
        assert make_palindrome("cata") == "catac"

    def test_two_char_non_palindrome(self):
        assert make_palindrome("ab") == "aba"

    def test_three_char_non_palindrome(self):
        assert make_palindrome("abc") == "abcba"

    def test_race_example(self):
        assert make_palindrome("race") == "racecar"

    def test_all_same_characters(self):
        assert make_palindrome("aaa") == "aaa"

    def test_two_same_characters(self):
        assert make_palindrome("aa") == "aa"

    def test_aab(self):
        """Longest palindromic suffix of 'aab' is 'b'."""
        assert make_palindrome("aab") == "aabaa"

    def test_level(self):
        assert make_palindrome("level") == "level"

    def test_madam(self):
        assert make_palindrome("madam") == "madam"

    def test_hello(self):
        assert make_palindrome("hello") == "hellolleh"

    def test_world(self):
        assert make_palindrome("world") == "worldlrow"

    def test_prefix_is_palindrome_but_not_full(self):
        """'abac' — longest palindromic suffix is 'c'."""
        assert make_palindrome("abac") == "abacaba"

    def test_reverse_of_input(self):
        """When input is already a palindrome, output equals input."""
        for word in ["deed", "pop", "noon", "refer"]:
            assert make_palindrome(word) == word

    def test_result_is_always_palindrome(self):
        """The output of make_palindrome should always be a palindrome."""
        test_strings = [
            "", "a", "ab", "abc", "cat", "cata", "race", "hello",
            "world", "aab", "abac", "python", "test", "example",
        ]
        for s in test_strings:
            result = make_palindrome(s)
            assert is_palindrome(result), f"{result} should be a palindrome"

    def test_result_starts_with_original(self):
        """The output must begin with the original string."""
        test_strings = [
            "", "a", "ab", "abc", "cat", "cata", "race", "hello",
            "world", "aab", "abac", "python", "test", "example",
        ]
        for s in test_strings:
            result = make_palindrome(s)
            assert result.startswith(s), f"{result} should start with '{s}'"

    def test_shortest_possible(self):
        """Verify that the result length equals len(s) + len(prefix_before_suffix)."""
        # For 'cat': longest palindromic suffix is 't' (len 1), prefix before is 'ca' (len 2)
        # Result should be len('cat') + 2 = 5
        assert len(make_palindrome("cat")) == 5

        # For 'race': longest palindromic suffix is 'e' (len 1), prefix before is 'rac' (len 3)
        # Result should be len('race') + 3 = 7
        assert len(make_palindrome("race")) == 7

        # For 'abba': already palindrome, result is 'abba' (len 4)
        assert len(make_palindrome("abba")) == 4
