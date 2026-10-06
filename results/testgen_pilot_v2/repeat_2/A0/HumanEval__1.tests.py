import pytest
from solution import separate_paren_groups


class TestSeparateParenGroups:
    """Tests for the separate_paren_groups function."""

    def test_docstring_example(self):
        """Test the example from the docstring."""
        assert separate_paren_groups('( ) (( )) (( )( ))') == ['()', '(())', '(()())']

    def test_single_group_no_spaces(self):
        """A single balanced group with no spaces."""
        assert separate_paren_groups('()') == ['()']

    def test_single_deeply_nested_group(self):
        """A single deeply nested group."""
        assert separate_paren_groups('((()))') == ['((()))']

    def test_multiple_simple_groups_no_spaces(self):
        """Multiple simple groups without any spaces."""
        assert separate_paren_groups('()(())') == ['()', '(())']

    def test_multiple_simple_groups_with_spaces(self):
        """Multiple simple groups separated by spaces."""
        assert separate_paren_groups('( ) ( )') == ['()', '()']

    def test_mixed_nesting_levels(self):
        """Groups with different nesting depths; spaces are stripped in output."""
        assert separate_paren_groups('( () (()) )') == ['(()(()))']

    def test_complex_groups(self):
        """Complex groups with mixed nesting."""
        assert separate_paren_groups('(()(()))') == ['(()(()))']

    def test_empty_string(self):
        """Empty input string should return empty list."""
        assert separate_paren_groups('') == []

    def test_only_spaces(self):
        """Input with only spaces should return empty list."""
        assert separate_paren_groups('   ') == []

    def test_spaces_between_groups(self):
        """Spaces between groups are ignored."""
        assert separate_paren_groups('( )  (())  (()())') == ['()', '(())', '(()())']

    def test_single_pair_with_surrounding_spaces(self):
        """Single pair surrounded by spaces."""
        assert separate_paren_groups('  ( )  ') == ['()']

    def test_many_groups(self):
        """Many small groups in sequence."""
        result = separate_paren_groups('( ) ( ) ( ) ( )')
        assert result == ['()', '()', '()', '()']

    def test_deeply_nested_single_group(self):
        """A very deeply nested single group."""
        assert separate_paren_groups('((((()))))') == ['((((()))))']

    def test_alternating_depth_groups(self):
        """Groups with alternating depth patterns."""
        assert separate_paren_groups('(()()) (())') == ['(()())', '(())']

    def test_group_with_internal_spaces(self):
        """Group that has internal spaces within it; spaces are stripped."""
        assert separate_paren_groups('( ( ) )') == ['(())']

    def test_two_deeply_nested_groups(self):
        """Two deeply nested groups."""
        assert separate_paren_groups('((())) ((()))') == ['((()))', '((()))']

    def test_unbalanced_input_behavior(self):
        """Test behavior when parentheses are unbalanced (incomplete group)."""
        # An incomplete group at the end won't be added since cnt != 0
        assert separate_paren_groups('() (') == ['()']

    def test_all_open_then_close(self):
        """All opens followed by all closes forms one group."""
        assert separate_paren_groups('(((') == []
        assert separate_paren_groups(')))') == []
