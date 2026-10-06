import pytest
from solution import separate_paren_groups


class TestSeparateParenGroups:
    """Tests for the separate_paren_groups function."""

    def test_example_from_docstring(self):
        """Test the example given in the docstring."""
        assert separate_paren_groups('( ) (( )) (( )( ))') == ['()', '(())', '(()())']

    def test_single_group_simple(self):
        """Test a single simple group."""
        assert separate_paren_groups('()') == ['()']

    def test_single_group_nested(self):
        """Test a single group with nesting."""
        assert separate_paren_groups('(())') == ['(())']

    def test_single_group_deeply_nested(self):
        """Test a single group with deep nesting."""
        assert separate_paren_groups('((()))') == ['((()))']

    def test_multiple_groups_no_spaces(self):
        """Test multiple groups without spaces."""
        assert separate_paren_groups('()()') == ['()', '()']

    def test_multiple_groups_with_spaces(self):
        """Test multiple groups separated by spaces."""
        assert separate_paren_groups('( ) ( )') == ['()', '()']

    def test_mixed_nesting_depths(self):
        """Test groups with different nesting depths."""
        assert separate_paren_groups('()(())') == ['()', '(())']

    def test_complex_groups(self):
        """Test complex mixed groups."""
        assert separate_paren_groups('(()())(())') == ['(()())', '(())']

    def test_empty_string(self):
        """Test with an empty string."""
        assert separate_paren_groups('') == []

    def test_only_spaces(self):
        """Test with a string containing only spaces."""
        assert separate_paren_groups('   ') == []

    def test_single_space_between_groups(self):
        """Test groups separated by a single space."""
        assert separate_paren_groups('( ) (())') == ['()', '(())']

    def test_multiple_spaces_between_groups(self):
        """Test groups separated by multiple spaces."""
        assert separate_paren_groups('( )  (())  (()())') == ['()', '(())', '(()())']

    def test_spaces_inside_groups(self):
        """Test spaces inside groups are ignored."""
        assert separate_paren_groups('( ( ) )') == ['(())']

    def test_unbalanced_raises_or_returns_partial(self):
        """Test behavior with unbalanced parentheses - should not crash."""
        # The function doesn't raise, it just processes what it can
        result = separate_paren_groups('(()')
        assert isinstance(result, list)

    def test_all_same_depth_groups(self):
        """Test multiple groups all at the same depth."""
        assert separate_paren_groups('()()()') == ['()', '()', '()']

    def test_three_different_groups(self):
        """Test three distinct groups."""
        assert separate_paren_groups('() (()) (()())') == ['()', '(())', '(()())']

    def test_group_with_inner_spaces(self):
        """Test that inner spaces don't affect grouping."""
        assert separate_paren_groups('(() ( ))') == ['(()())']

    def test_empty_group_ignored(self):
        """Test that empty parenthesized groups like '( )' become '()'."""
        assert separate_paren_groups('( )') == ['()']

    def test_large_number_of_groups(self):
        """Test with many small groups."""
        input_str = '() ' * 10
        expected = ['()'] * 10
        assert separate_paren_groups(input_str) == expected

    def test_alternating_depth_groups(self):
        """Test alternating between shallow and deep groups."""
        assert separate_paren_groups('()(())()(())') == ['()', '(())', '()', '(())']
