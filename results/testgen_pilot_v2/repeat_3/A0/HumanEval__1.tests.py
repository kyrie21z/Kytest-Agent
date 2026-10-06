"""Unit tests for solution.separate_paren_groups."""

import pytest
from solution import separate_paren_groups


class TestSeparateParenGroups:
    """Tests for the separate_paren_groups function."""

    # ------------------------------------------------------------------
    # Docstring examples
    # ------------------------------------------------------------------

    def test_docstring_example(self):
        """Example from the docstring."""
        assert separate_paren_groups('( ) (( )) (( )( ))') == [
            '()', '(())', '(()())'
        ]

    # ------------------------------------------------------------------
    # Single-group inputs
    # ------------------------------------------------------------------

    def test_single_pair(self):
        """A single pair of parentheses."""
        assert separate_paren_groups('()') == ['()']

    def test_single_nested_group(self):
        """One deeply-nested group."""
        assert separate_paren_groups('((()))') == ['((()))']

    def test_single_group_with_spaces(self):
        """Spaces inside a single group are ignored; structure preserved."""
        # '( ( ) )' -> remove spaces -> '(())'
        assert separate_paren_groups('( ( ) )') == ['(())']

    # ------------------------------------------------------------------
    # Multiple-group inputs
    # ------------------------------------------------------------------

    def test_two_simple_groups(self):
        """Two adjacent simple groups."""
        assert separate_paren_groups('() ()') == ['()', '()']

    def test_two_different_groups(self):
        """Two groups with different nesting levels."""
        assert separate_paren_groups('(()) (())') == ['(())', '(())']

    def test_three_groups(self):
        """Three groups of varying complexity."""
        result = separate_paren_groups('() (()) (()())')
        assert result == ['()', '(())', '(()())']

    def test_multiple_groups_no_spaces(self):
        """Groups concatenated without spaces should still be split correctly."""
        assert separate_paren_groups('()()') == ['()', '()']

    def test_mixed_complexity_groups(self):
        """Groups with mixed nesting depths."""
        result = separate_paren_groups('() ((())) (()(()))')
        assert result == ['()', '((()))', '(()(()))']

    # ------------------------------------------------------------------
    # Edge cases – empty / whitespace-only
    # ------------------------------------------------------------------

    def test_empty_string(self):
        """Empty input returns an empty list."""
        assert separate_paren_groups('') == []

    def test_only_spaces(self):
        """Input containing only spaces returns an empty list."""
        assert separate_paren_groups('   ') == []

    def test_spaces_between_groups(self):
        """Multiple spaces between groups are handled."""
        assert separate_paren_groups('()    (())') == ['()', '(())']

    # ------------------------------------------------------------------
    # Deeply nested groups
    # ------------------------------------------------------------------

    def test_deeply_nested(self):
        """A very deeply nested single group."""
        deep = '(' * 10 + ')' * 10
        assert separate_paren_groups(deep) == [deep]

    def test_deeply_nested_with_space(self):
        """Deeply nested group with internal spaces."""
        deep = '( ' * 5 + ' ' + ') ' * 5
        expected = '(' * 5 + ')' * 5
        assert separate_paren_groups(deep) == [expected]

    # ------------------------------------------------------------------
    # Complex / interleaved patterns
    # ------------------------------------------------------------------

    def test_alternating_nesting(self):
        """Group with alternating open/close at various depths."""
        assert separate_paren_groups('(()(()))') == ['(()(()))']

    def test_many_simple_groups(self):
        """Many simple groups in sequence."""
        input_str = '() ' * 5
        expected = ['()'] * 5
        assert separate_paren_groups(input_str) == expected

    # ------------------------------------------------------------------
    # Return type checks
    # ------------------------------------------------------------------

    def test_returns_list(self):
        """Ensure the return type is always a list."""
        assert isinstance(separate_paren_groups('()'), list)
        assert isinstance(separate_paren_groups(''), list)

    def test_returns_list_of_strings(self):
        """Every element in the returned list must be a string."""
        result = separate_paren_groups('(()) (())')
        assert all(isinstance(item, str) for item in result)

    # ------------------------------------------------------------------
    # Balanced-pair validation
    # ------------------------------------------------------------------

    def test_balanced_but_unusual(self):
        """A balanced group that isn't trivially simple."""
        assert separate_paren_groups('()(())') == ['()', '(())']
