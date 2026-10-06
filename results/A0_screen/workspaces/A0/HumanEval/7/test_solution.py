import pytest
from solution import filter_by_substring


class TestFilterBySubstring:
    """Tests for the filter_by_substring function."""

    def test_empty_list(self):
        """Empty input list should return empty list."""
        assert filter_by_substring([], 'a') == []

    def test_basic_match(self):
        """Test basic filtering with one matching substring."""
        result = filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
        assert result == ['abc', 'bacd', 'array']

    def test_no_matches(self):
        """When no strings contain the substring, return empty list."""
        result = filter_by_substring(['hello', 'world', 'foo'], 'xyz')
        assert result == []

    def test_all_match(self):
        """When all strings contain the substring, return all of them."""
        result = filter_by_substring(['apple', 'apply', 'application'], 'app')
        assert result == ['apple', 'apply', 'application']

    def test_single_element_matching(self):
        """Single element list where the element matches."""
        assert filter_by_substring(['hello'], 'ell') == ['hello']

    def test_single_element_not_matching(self):
        """Single element list where the element does not match."""
        assert filter_by_substring(['hello'], 'xyz') == []

    def test_empty_substring(self):
        """Empty substring should match every string (since '' is in every string)."""
        result = filter_by_substring(['abc', 'def', 'ghi'], '')
        assert result == ['abc', 'def', 'ghi']

    def test_substring_at_start(self):
        """Substring at the beginning of the string."""
        result = filter_by_substring(['start', 'end', 'starter'], 'sta')
        assert result == ['start', 'starter']

    def test_substring_at_end(self):
        """Substring at the end of the string."""
        result = filter_by_substring(['ending', 'middle', 'beginning'], 'ing')
        assert result == ['ending', 'beginning']

    def test_substring_in_middle(self):
        """Substring in the middle of the string."""
        result = filter_by_substring(['python', 'java', 'javascript'], 'ava')
        assert result == ['java', 'javascript']

    def test_multiple_occurrences(self):
        """String with multiple occurrences of the substring."""
        result = filter_by_substring(['aaa', 'aba'], 'a')
        assert result == ['aaa', 'aba']

    def test_case_sensitive(self):
        """Filtering should be case-sensitive."""
        result = filter_by_substring(['Hello', 'hello', 'HELLO'], 'h')
        assert result == ['hello']

    def test_case_insensitive_search_fails(self):
        """Uppercase substring should not match lowercase strings."""
        result = filter_by_substring(['hello', 'world'], 'H')
        assert result == []

    def test_special_characters(self):
        """Test with special characters in strings and substring."""
        result = filter_by_substring(['foo@bar', 'baz#qux', 'hello'], '@')
        assert result == ['foo@bar']

    def test_whitespace_substring(self):
        """Test with whitespace as substring."""
        result = filter_by_substring(['hello world', 'foo', 'bar baz'], ' ')
        assert result == ['hello world', 'bar baz']

    def test_full_string_match(self):
        """When the substring equals the full string."""
        result = filter_by_substring(['abc', 'def', 'abc'], 'abc')
        assert result == ['abc', 'abc']

    def test_duplicate_strings(self):
        """Duplicate strings in input should be preserved in output."""
        result = filter_by_substring(['test', 'test', 'other'], 'test')
        assert result == ['test', 'test']

    def test_numeric_strings(self):
        """Test with numeric strings."""
        result = filter_by_substring(['123', '456', '789', '1234'], '12')
        assert result == ['123', '1234']

    def test_long_substring(self):
        """Test with a long substring."""
        result = filter_by_substring(
            ['the quick brown fox', 'jumps over the lazy dog', 'hello'],
            'the quick'
        )
        assert result == ['the quick brown fox']

    def test_unicode_strings(self):
        """Test with unicode characters."""
        result = filter_by_substring(['café', 'naïve', 'hello'], 'é')
        assert result == ['café']

    def test_newline_character(self):
        """Test with newline character in strings."""
        result = filter_by_substring(['hello\nworld', 'foo', 'bar\nbaz'], '\n')
        assert result == ['hello\nworld', 'bar\nbaz']
