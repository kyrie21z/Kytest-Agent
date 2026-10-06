import pytest
from solution import separate_paren_groups


class TestSeparateParenGroups_NormalCases:
    """Test normal/typical inputs."""

    def test_example_from_docstring(self):
        """The exact example from the docstring."""
        assert separate_paren_groups('( ) (( )) (( )( ))') == ['()', '(())', '(()())']

    def test_single_simple_group(self):
        """A single pair of parentheses."""
        assert separate_paren_groups('()') == ['()']

    def test_multiple_simple_groups_no_spaces(self):
        """Multiple simple groups concatenated without spaces."""
        assert separate_paren_groups('()()()') == ['()', '()', '()']

    def test_deeply_nested_single_group(self):
        """A single deeply nested group."""
        assert separate_paren_groups('((()))') == ['((()))']

    def test_complex_single_group(self):
        """A single group with mixed nesting."""
        assert separate_paren_groups('(()(()))') == ['(()(()))']

    def test_two_balanced_groups_no_spaces(self):
        """Two balanced groups concatenated."""
        assert separate_paren_groups('()(())') == ['()', '(())']

    def test_mixed_depth_groups(self):
        """Groups with varying nesting depths."""
        assert separate_paren_groups('() (()) (()())') == ['()', '(())', '(()())']

    def test_three_groups_with_spaces(self):
        """Three groups separated by spaces."""
        assert separate_paren_groups('(()) (()) (())') == ['(())', '(())', '(())']

    def test_single_group_with_internal_spaces(self):
        """A single group with spaces inside."""
        assert separate_paren_groups('( ( ) )') == ['(())']


class TestSeparateParenGroups_EmptyAndWhitespace:
    """Test empty, whitespace-only, and zero-size inputs."""

    def test_empty_string(self):
        """Empty string should return empty list."""
        assert separate_paren_groups('') == []

    def test_only_spaces(self):
        """String with only spaces should return empty list."""
        assert separate_paren_groups('     ') == []

    def test_only_newlines_and_spaces(self):
        """Non-space whitespace characters (newlines, tabs) are NOT ignored.
        They become individual groups since cnt stays 0 throughout."""
        assert separate_paren_groups('\n\t  \n') == ['\n', '\t', '\n']

    def test_space_between_groups(self):
        """Spaces between groups are ignored correctly."""
        assert separate_paren_groups('()  (())  (()())') == ['()', '(())', '(()())']


class TestSeparateParenGroups_BoundaryCases:
    """Test boundary conditions at edges of valid input ranges."""

    def test_minimal_valid_input(self):
        """Minimal valid input: just one pair."""
        assert separate_paren_groups('()') == ['()']

    def test_maximal_nesting_single_group(self):
        """Very deep nesting in a single group."""
        deep = '(' * 50 + ')' * 50
        assert separate_paren_groups(deep) == [deep]

    def test_many_small_groups(self):
        """Many small groups concatenated."""
        many = '()' * 20
        expected = ['()'] * 20
        assert separate_paren_groups(many) == expected

    def test_alternating_depth_groups(self):
        """Alternating between shallow and deep groups."""
        assert separate_paren_groups('() (()) () (())') == ['()', '(())', '()', '(())']

    def test_group_with_single_inner_pair(self):
        """Group containing exactly one inner pair."""
        assert separate_paren_groups('(()())') == ['(()())']

    def test_consecutive_same_depth_groups(self):
        """Consecutive groups all at the same depth."""
        assert separate_paren_groups('()()()()') == ['()', '()', '()', '()']


class TestSeparateParenGroups_InvalidInputs:
    """Test invalid/unbalanced inputs — behavior may be undefined but should be consistent."""

    def test_extra_open_paren(self):
        """Unbalanced: more opening than closing parens."""
        # cnt never returns to 0 after the first char, so nothing gets appended
        assert separate_paren_groups('(()') == []

    def test_extra_close_paren(self):
        """Unbalanced: more closing than opening parens."""
        # First '()' is balanced and captured; trailing ')' leaves cnt=-1
        assert separate_paren_groups('())') == ['()']

    def test_only_closing_parens(self):
        """Only closing parentheses — cnt goes negative immediately."""
        assert separate_paren_groups(')))') == []

    def test_only_opening_parens(self):
        """Only opening parentheses — cnt grows but never returns to 0."""
        assert separate_paren_groups('(((') == []

    def test_interleaved_unbalanced(self):
        """Interleaved open/close that never fully balances."""
        assert separate_paren_groups('()()') == ['()', '()']

    def test_unbalanced_trailing_close(self):
        """Balanced group followed by extra closing parens."""
        assert separate_paren_groups('(())() )') == ['(())', '()']

    def test_unbalanced_leading_close(self):
        """Extra closing parens before any balanced group.
        Tracing: ')' -> cnt=-1, group=')'; '(' -> cnt=0, group=')( ', append ')( ', group='';
        '(' -> cnt=1, group='('; ')' -> cnt=0, group='()', append '()', group=''"""
        assert separate_paren_groups(')(()') == [')(', '()']

    def test_completely_reverse(self):
        """Reverse of a valid group — unbalanced until the last character.
        Tracing: ')' -> cnt=-1, group=')'; ')' -> cnt=-2, group='))';
        '(' -> cnt=-1, group='))('; '(' -> cnt=0, group='))((', append '))(('"""
        assert separate_paren_groups('))((') == ['))((']


class TestSeparateParenGroups_EdgePatterns:
    """Test specific structural patterns."""

    def test_wide_group(self):
        """A wide group with siblings alternating inside."""
        assert separate_paren_groups('(()()())') == ['(()()())']

    def test_nested_within_nested(self):
        """Deeply nested structure with internal groups — single balanced group."""
        assert separate_paren_groups('((())(()))') == ['((())(()))']

    def test_single_char_groups(self):
        """Each group is just a minimal pair."""
        assert separate_paren_groups('()()()()()') == ['()', '()', '()', '()', '()']

    def test_spaces_everywhere(self):
        """Spaces between every character."""
        assert separate_paren_groups('( ) ( ( ) )') == ['()', '(())']

    def test_tab_and_newline_chars(self):
        """Tabs and newlines are NOT treated as spaces — they become separate groups.
        Tracing: '(' -> cnt=1, group='('; ')' -> cnt=0, group='()', append '()';
        '\\t' -> cnt=0, group='\\t', append '\\t';
        '\\n' -> cnt=0, group='\\n', append '\\n';
        '(' -> cnt=1, group='('; ')' -> cnt=0, group='()', append '()'"""
        assert separate_paren_groups('()\t\n()') == ['()', '\t', '\n', '()']
