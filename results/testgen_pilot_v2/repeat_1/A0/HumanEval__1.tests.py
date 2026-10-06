import pytest
from solution import separate_paren_groups


class TestSeparateParenGroups:
    """Tests for the separate_paren_groups function."""

    # ── Doctest / basic examples ────────────────────────────────────────

    def test_example_from_docstring(self):
        """Example from the docstring."""
        assert separate_paren_groups('( ) (( )) (( )( ))') == ['()', '(())', '(()())']

    # ── Single group cases ─────────────────────────────────────────────

    def test_single_simple_pair(self):
        """A single empty-ish pair."""
        assert separate_paren_groups('( )') == ['()']

    def test_single_nested_pair(self):
        """A single group with one level of nesting."""
        assert separate_paren_groups('(( ))') == ['(())']

    def test_single_deeply_nested(self):
        """A single group with multiple levels of nesting."""
        assert separate_paren_groups('((( )))') == ['((()))']

    def test_single_complex_group(self):
        """A single group with mixed nesting."""
        assert separate_paren_groups('(()(()))') == ['(()(()))']

    # ── Multiple groups ────────────────────────────────────────────────

    def test_two_groups(self):
        """Two separate groups."""
        assert separate_paren_groups('( ) ( )') == ['()', '()']

    def test_two_different_groups(self):
        """Two groups with different structures."""
        assert separate_paren_groups('(() ) (())') == ['(())', '(())']

    def test_multiple_groups_no_spaces(self):
        """Multiple groups concatenated without spaces (should still separate)."""
        assert separate_paren_groups('()()') == ['()', '()']

    def test_multiple_groups_mixed_depths(self):
        """Groups at various nesting depths."""
        assert separate_paren_groups('() (()) () ((( )))') == ['()', '(())', '()', '((()))']

    # ── Whitespace handling ────────────────────────────────────────────

    def test_only_spaces(self):
        """Input consisting solely of spaces."""
        assert separate_paren_groups('   ') == []

    def test_empty_string(self):
        """Empty input string."""
        assert separate_paren_groups('') == []

    def test_spaces_around_groups(self):
        """Spaces before, between, and after groups."""
        assert separate_paren_groups('  ( )  (())  ') == ['()', '(())']

    def test_spaces_inside_groups(self):
        """Spaces inside groups should be ignored."""
        assert separate_paren_groups('( ( ) )') == ['(())']

    def test_extra_whitespace_between_groups(self):
        """Extra whitespace between groups does not affect separation."""
        assert separate_paren_groups('( )      (())') == ['()', '(())']

    # ── Edge cases ─────────────────────────────────────────────────────

    def test_single_open_paren(self):
        """Unbalanced: single opening parenthesis — should return empty list
        because cnt never reaches 0 after adding characters."""
        result = separate_paren_groups('(')
        assert result == []

    def test_single_close_paren(self):
        """Unbalanced: single closing parenthesis — cnt goes negative,
        but group is non-empty so it gets appended when cnt == 0 check fails."""
        result = separate_paren_groups(')')
        # cnt starts at 0, ch=')' → cnt=-1, group=")", cnt != 0 → nothing appended
        assert result == []

    def test_unbalanced_more_closes(self):
        """More closing than opening parentheses."""
        result = separate_paren_groups('())')
        # After first "()": cnt=0, group="()", appended. Then ")": cnt=-1, group=")"
        # cnt never returns to 0, so trailing ")" is not appended.
        assert result == ['()']

    def test_unbalanced_more_opens(self):
        """More opening than closing parentheses."""
        result = separate_paren_groups('(()')
        # cnt goes 1→2→1, never hits 0 again, so nothing appended.
        assert result == []

    def test_alternating_groups(self):
        """Many small alternating groups."""
        assert separate_paren_groups('()()()()') == ['()', '()', '()', '()']

    def test_nested_within_same_level(self):
        """Adjacent groups where one is nested inside another conceptually
        but they are actually separate top-level groups."""
        assert separate_paren_groups('(() ) (())') == ['(())', '(())']

    # ── Larger / stress cases ──────────────────────────────────────────

    def test_many_groups(self):
        """A larger number of groups."""
        input_str = ' '.join(['( )'] * 10)
        expected = ['()'] * 10
        assert separate_paren_groups(input_str) == expected

    def test_deep_nesting(self):
        """Very deep nesting in a single group."""
        depth = 20
        input_str = '(' * depth + ')' * depth
        expected = ['(' * depth + ')' * depth]
        assert separate_paren_groups(input_str) == expected

    def test_complex_balanced_expression(self):
        """A complex but valid expression with multiple groups."""
        input_str = '(()) (()(())) ((()))'
        assert separate_paren_groups(input_str) == ['(())', '(()(()))', '((()))']

    def test_groups_with_inner_content(self):
        """Groups containing multiple sibling sub-groups."""
        assert separate_paren_groups('(()())') == ['(()())']

    def test_space_before_first_group(self):
        """Leading spaces before the first group."""
        assert separate_paren_groups('   (())') == ['(())']

    def test_space_after_last_group(self):
        """Trailing spaces after the last group."""
        assert separate_paren_groups('(())   ') == ['(())']
