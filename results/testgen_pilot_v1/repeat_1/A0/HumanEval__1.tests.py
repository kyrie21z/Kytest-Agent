import pytest
from solution import separate_paren_groups


class TestSeparateParenGroups:
    """Tests for the separate_paren_groups function."""

    # ── Doctest / basic examples ──────────────────────────────────────

    def test_basic_example(self):
        """The example from the docstring."""
        assert separate_paren_groups('( ) (( )) (( )( ))') == ['()', '(())', '(()())']

    # ── Single group ──────────────────────────────────────────────────

    def test_single_group_no_spaces(self):
        """A single balanced group with no spaces."""
        assert separate_paren_groups('()') == ['()']

    def test_single_group_nested(self):
        """A single deeply nested group."""
        assert separate_paren_groups('((()))') == ['((()))']

    def test_single_group_with_spaces(self):
        """A single group that contains spaces."""
        assert separate_paren_groups('( ( ) )') == ['()']

    def test_single_group_mixed_nesting(self):
        """A single group with mixed nesting levels."""
        assert separate_paren_groups('(()(()))') == ['(()(()))']

    # ── Multiple groups ───────────────────────────────────────────────

    def test_two_simple_groups(self):
        """Two simple adjacent groups."""
        assert separate_paren_groups('() ()') == ['()', '()']

    def test_two_groups_no_space(self):
        """Two groups concatenated without space — should be treated as one."""
        assert separate_paren_groups('()()') == ['()()']

    def test_three_groups_different_depths(self):
        """Three groups with varying nesting depths."""
        assert separate_paren_groups('() (()) (()())') == ['()', '(())', '(()())']

    def test_multiple_groups_no_spaces(self):
        """Multiple groups separated only by implicit boundaries."""
        assert separate_paren_groups('()(())(()())') == ['()', '(())', '(()())']

    # ── Edge cases ────────────────────────────────────────────────────

    def test_empty_string(self):
        """Empty input should return an empty list."""
        assert separate_paren_groups('') == []

    def test_only_spaces(self):
        """Input consisting solely of spaces."""
        assert separate_paren_groups('     ') == []

    def test_deeply_nested(self):
        """Very deep nesting in a single group."""
        assert separate_paren_groups('((((()))))') == ['((((()))))']

    def test_wide_nesting(self):
        """Many siblings at the same level."""
        assert separate_paren_groups('()()()()()') == ['()', '()', '()', '()', '()']

    def test_complex_mixed(self):
        """Complex mix of nesting and spacing."""
        result = separate_paren_groups('( ) ( ( ) ) ( ( ) ( ) )')
        assert result == ['()', '(())', '(()())']

    def test_alternating_depth(self):
        """Groups with alternating depth patterns."""
        assert separate_paren_groups('(()(())) (()) ()') == ['(()(()))', '(())', '()']

    # ── Return type checks ────────────────────────────────────────────

    def test_returns_list(self):
        """Ensure the return type is always a list."""
        assert isinstance(separate_paren_groups('()'), list)
        assert isinstance(separate_paren_groups(''), list)

    def test_returns_strings_in_list(self):
        """Every element in the returned list must be a string."""
        result = separate_paren_groups('(()) (()())')
        assert all(isinstance(item, str) for item in result)

    # ── Boundary / stress cases ───────────────────────────────────────

    def test_very_long_input(self):
        """A long string of many small groups."""
        many = '()' * 100
        expected = ['()'] * 100
        assert separate_paren_groups(many) == expected

    def test_balanced_but_not_separable(self):
        """A fully balanced expression that is one group."""
        assert separate_paren_groups('(()(()(())))') == ['(()(()(())))']

    def test_extra_spaces_between_groups(self):
        """Extra whitespace between groups should be ignored."""
        assert separate_paren_groups('()   (())   (()())') == ['()', '(())', '(()())']

    def test_spaces_inside_groups(self):
        """Spaces inside a group should be stripped."""
        assert separate_paren_groups('( ( ( ) ) )') == ['((()))']
