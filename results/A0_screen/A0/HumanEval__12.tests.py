import pytest
from solution import longest


class TestLongest:
    """Tests for the longest() function."""

    def test_empty_list(self):
        """Empty list should return None."""
        assert longest([]) is None

    def test_single_element(self):
        """Single element list should return that element."""
        assert longest(["hello"]) == "hello"

    def test_all_same_length(self):
        """When all strings have the same length, return the first one."""
        assert longest(["abc", "def", "ghi"]) == "abc"

    def test_first_is_longest(self):
        """First string is the longest."""
        assert longest(["longest", "short", "medium"]) == "longest"

    def test_last_is_longest(self):
        """Last string is the longest."""
        assert longest(["a", "bb", "ccc"]) == "ccc"

    def test_middle_is_longest(self):
        """Middle string is the longest."""
        assert longest(["ab", "cccc", "de"]) == "cccc"

    def test_tie_returns_first(self):
        """In case of tie, return the first occurrence."""
        assert longest(["aaa", "bbb", "ccc"]) == "aaa"

    def test_tie_not_at_start(self):
        """In case of tie not at start, return the first among the tied."""
        assert longest(["a", "bb", "cc", "dd"]) == "bb"

    def test_contains_empty_string(self):
        """List with an empty string among others."""
        assert longest(["", "a", "bb"]) == "bb"

    def test_only_empty_strings(self):
        """List containing only empty strings."""
        assert longest(["", "", ""]) == ""

    def test_mixed_lengths(self):
        """Various lengths mixed together."""
        assert longest(["x", "xx", "xxx", "xxxx"]) == "xxxx"

    def test_negative_case_none(self):
        """Explicitly verify None for empty input."""
        result = longest([])
        assert result is None

    def test_unicode_strings(self):
        """Test with unicode characters."""
        assert longest(["α", "ββ", "γγγ"]) == "γγγ"

    def test_whitespace_strings(self):
        """Test with strings containing whitespace."""
        assert longest([" ", "  ", "   "]) == "   "

    def test_numbers_as_strings(self):
        """Test with numeric strings."""
        assert longest(["1", "12", "123"]) == "123"
