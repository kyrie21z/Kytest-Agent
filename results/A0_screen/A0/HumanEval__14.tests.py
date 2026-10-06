import pytest
from solution import all_prefixes


class TestAllPrefixes:
    """Tests for the all_prefixes function."""

    def test_basic_example(self):
        """Test the example from the docstring."""
        assert all_prefixes('abc') == ['a', 'ab', 'abc']

    def test_empty_string(self):
        """An empty string should return an empty list."""
        assert all_prefixes('') == []

    def test_single_character(self):
        """A single-character string should return a list with one element."""
        assert all_prefixes('x') == ['x']

    def test_two_characters(self):
        """A two-character string should return two prefixes."""
        assert all_prefixes('ab') == ['a', 'ab']

    def test_longer_string(self):
        """Test with a longer string."""
        result = all_prefixes('hello')
        assert result == ['h', 'he', 'hel', 'hell', 'hello']

    def test_returns_list(self):
        """Verify the return type is a list."""
        assert isinstance(all_prefixes('test'), list)

    def test_order_shortest_to_longest(self):
        """Prefixes should be ordered from shortest to longest."""
        result = all_prefixes('python')
        for i in range(len(result) - 1):
            assert len(result[i]) < len(result[i + 1])

    def test_full_string_included(self):
        """The last element should be the full input string."""
        assert all_prefixes('world')[-1] == 'world'

    def test_first_element_is_first_char(self):
        """The first element should be the first character of the string."""
        assert all_prefixes('abcdef')[0] == 'a'

    def test_special_characters(self):
        """Test with special characters in the string."""
        assert all_prefixes('!@#') == ['!', '!@', '!@#']

    def test_spaces(self):
        """Test with spaces in the string."""
        assert all_prefixes('a b') == ['a', 'a ', 'a b']

    def test_numbers_as_string(self):
        """Test with numeric characters."""
        assert all_prefixes('1234') == ['1', '12', '123', '1234']

    def test_uppercase_and_lowercase(self):
        """Test with mixed case."""
        assert all_prefixes('AbC') == ['A', 'Ab', 'AbC']

    def test_length_matches_input(self):
        """The length of the result should equal the length of the input string."""
        for s in ['', 'a', 'ab', 'abc', 'hello world']:
            assert len(all_prefixes(s)) == len(s)

    def test_no_duplicates(self):
        """Each prefix should be unique."""
        result = all_prefixes('aaa')
        assert len(result) == len(set(result))
        assert result == ['a', 'aa', 'aaa']
