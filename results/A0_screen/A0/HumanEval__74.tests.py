import pytest
from solution import total_match


class TestTotalMatch:
    """Tests for the total_match function."""

    def test_both_empty(self):
        """When both lists are empty, return an empty list."""
        assert total_match([], []) == []

    def test_first_list_fewer_chars(self):
        """Return the first list when it has fewer total characters."""
        assert total_match(['hi', 'admin'], ['hi', 'hi', 'admin', 'project']) == ['hi', 'admin']

    def test_second_list_fewer_chars(self):
        """Return the second list when it has fewer total characters."""
        assert total_match(['hi', 'admin'], ['hI', 'Hi']) == ['hI', 'Hi']

    def test_equal_char_counts_returns_first(self):
        """When both lists have the same number of characters, return the first list."""
        assert total_match(['hi', 'admin'], ['hI', 'hi', 'hi']) == ['hI', 'hi', 'hi']

    def test_single_element_lists(self):
        """Test with single-element lists."""
        assert total_match(['4'], ['1', '2', '3', '4', '5']) == ['4']

    def test_single_vs_multiple(self):
        """Single short string vs multiple longer strings."""
        assert total_match(['a'], ['hello', 'world']) == ['a']

    def test_single_vs_multiple_reversed(self):
        """Single long string vs multiple short strings."""
        assert total_match(['hello', 'world'], ['a', 'b']) == ['a', 'b']

    def test_empty_first_list(self):
        """Empty first list should always be returned (0 chars)."""
        assert total_match([], ['anything']) == []

    def test_empty_second_list(self):
        """Non-empty first list vs empty second list: empty list has fewer chars, so it's returned."""
        assert total_match(['hello'], []) == []

    def test_strings_with_spaces(self):
        """Strings containing spaces count toward total length."""
        assert total_match(['a b'], ['c d e']) == ['a b']

    def test_case_sensitivity(self):
        """Function is case-sensitive in terms of content but only counts length."""
        result = total_match(['ABC'], ['abc'])
        # Both have 3 chars, so first list is returned
        assert result == ['ABC']

    def test_numbers_as_strings(self):
        """Numbers stored as strings should be counted by their character length."""
        assert total_match(['12345'], ['1', '2']) == ['1', '2']

    def test_unicode_characters(self):
        """Unicode characters should be counted correctly."""
        assert total_match(['café'], ['hello']) == ['café']

    def test_longer_first_list_still_wins_if_shorter_total(self):
        """A longer list can still win if its total character count is smaller."""
        assert total_match(['a', 'b', 'c', 'd'], ['hello']) == ['a', 'b', 'c', 'd']

    def test_identical_lists(self):
        """Identical lists have equal char counts; return first."""
        lst = ['hello', 'world']
        assert total_match(lst, lst) == lst

    def test_whitespace_only_strings(self):
        """Whitespace-only strings contribute to character count."""
        assert total_match(['   '], ['a']) == ['a']

    def test_mixed_content(self):
        """Lists with mixed alphanumeric content."""
        assert total_match(['a1', 'b2'], ['x', 'y', 'z']) == ['x', 'y', 'z']
