import pytest
from solution import filter_by_prefix


class TestFilterByPrefix:
    """Tests for the filter_by_prefix function."""

    def test_empty_list(self):
        """Empty input list should return an empty list."""
        assert filter_by_prefix([], 'a') == []

    def test_no_matches(self):
        """No strings matching the prefix should return an empty list."""
        assert filter_by_prefix(['abc', 'bcd', 'cde'], 'z') == []

    def test_all_match(self):
        """All strings matching the prefix should return the full list."""
        result = filter_by_prefix(['apple', 'apply', 'application'], 'app')
        assert result == ['apple', 'apply', 'application']

    def test_partial_match(self):
        """Only strings starting with the prefix should be returned."""
        result = filter_by_prefix(['abc', 'bcd', 'cde', 'array'], 'a')
        assert result == ['abc', 'array']

    def test_single_element_match(self):
        """Single element that matches should be returned."""
        assert filter_by_prefix(['hello'], 'hel') == ['hello']

    def test_single_element_no_match(self):
        """Single element that doesn't match should return empty list."""
        assert filter_by_prefix(['hello'], 'world') == []

    def test_empty_prefix(self):
        """Empty prefix should match all strings (every string starts with '')."""
        result = filter_by_prefix(['foo', 'bar', 'baz'], '')
        assert result == ['foo', 'bar', 'baz']

    def test_string_equals_prefix(self):
        """Strings exactly equal to the prefix should be included."""
        result = filter_by_prefix(['cat', 'dog', 'bird'], 'cat')
        assert result == ['cat']

    def test_case_sensitivity(self):
        """Matching should be case-sensitive."""
        result = filter_by_prefix(['Apple', 'apple', 'APPLE'], 'A')
        assert result == ['Apple', 'APPLE']

    def test_lowercase_prefix_not_matched_uppercase(self):
        """Lowercase prefix should not match uppercase strings."""
        result = filter_by_prefix(['Apple', 'banana'], 'b')
        assert result == ['banana']

    def test_longer_prefix_than_string(self):
        """Prefix longer than a string should never match that string."""
        result = filter_by_prefix(['hi', 'hello', 'hey'], 'helloo')
        assert result == []

    def test_special_characters_in_prefix(self):
        """Prefix containing special characters should work correctly."""
        result = filter_by_prefix(['@user1', '@user2', '#hashtag'], '@')
        assert result == ['@user1', '@user2']

    def test_numbers_as_strings(self):
        """Strings representing numbers should be filtered correctly."""
        result = filter_by_prefix(['123', '456', '12ab'], '12')
        assert result == ['123', '12ab']

    def test_whitespace_prefix(self):
        """Prefix consisting of whitespace should work."""
        result = filter_by_prefix([' hello', 'world', ' hi there'], ' ')
        assert result == [' hello', ' hi there']

    def test_returns_new_list(self):
        """The function should return a new list, not modify the original."""
        original = ['apple', 'banana', 'apricot']
        result = filter_by_prefix(original, 'a')
        assert result == ['apple', 'apricot']
        assert original == ['apple', 'banana', 'apricot']  # unchanged

    def test_duplicate_strings(self):
        """Duplicate strings in input should appear multiple times in output."""
        result = filter_by_prefix(['test', 'test', 'other'], 'test')
        assert result == ['test', 'test']

    def test_unicode_strings(self):
        """Unicode strings should be handled correctly."""
        result = filter_by_prefix(['日本語', 'français', 'español'], 'fr')
        assert result == ['français']

    def test_mixed_length_strings(self):
        """Mixed length strings should be filtered correctly."""
        result = filter_by_prefix(['a', 'ab', 'abc', 'b', 'bc'], 'a')
        assert result == ['a', 'ab', 'abc']
