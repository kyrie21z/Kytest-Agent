import pytest
from solution import separate_paren_groups


class TestSeparateParenGroups:
    """Tests for the separate_paren_groups function."""

    def test_basic_example(self):
        """Test the example from the docstring."""
        result = separate_paren_groups('( ) (( )) (( )( ))')
        assert result == ['()', '(())', '(()())']

    def test_single_group_no_spaces(self):
        """Test a single group without spaces."""
        result = separate_paren_groups('()')
        assert result == ['()']

    def test_single_group_nested(self):
        """Test a single deeply nested group."""
        result = separate_paren_groups('((()))')
        assert result == ['((()))']

    def test_multiple_simple_groups(self):
        """Test multiple simple groups separated by spaces."""
        result = separate_paren_groups('() () ()')
        assert result == ['()', '()', '()']

    def test_mixed_nesting_depths(self):
        """Test groups with varying nesting depths."""
        result = separate_paren_groups('() (()) ((( )))')
        assert result == ['()', '(())', '((()))']

    def test_empty_input(self):
        """Test with an empty string."""
        result = separate_paren_groups('')
        assert result == []

    def test_only_spaces(self):
        """Test with a string containing only spaces."""
        result = separate_paren_groups('   ')
        assert result == []

    def test_spaces_ignored(self):
        """Test that spaces within groups are properly ignored."""
        result = separate_paren_groups('(  )')
        assert result == ['()']

    def test_complex_balanced_groups(self):
        """Test complex balanced groups."""
        result = separate_paren_groups('(()) (()) (())')
        assert result == ['(())', '(())', '(())']

    def test_interleaved_nesting(self):
        """Test groups with interleaved open/close patterns."""
        result = separate_paren_groups('(()()) (()())')
        assert result == ['(()())', '(()())']

    def test_deeply_nested_single_group(self):
        """Test a single very deeply nested group."""
        result = separate_paren_groups('((((()))))')
        assert result == ['((((()))))']

    def test_alternating_groups(self):
        """Test alternating between simple and nested groups."""
        result = separate_paren_groups('() (()) () (())')
        assert result == ['()', '(())', '()', '(())']

    def test_three_level_nesting(self):
        """Test three-level deep nesting."""
        result = separate_paren_groups('((()))')
        assert result == ['((()))']

    def test_multiple_three_level_groups(self):
        """Test multiple three-level deep groups."""
        result = separate_paren_groups('((())) ((()))')
        assert result == ['((()))', '((()))']

    def test_unbalanced_raises_or_returns_partial(self):
        """Test behavior with unbalanced parentheses - should not crash."""
        # The function doesn't raise; it just processes what it can
        result = separate_paren_groups('(()')
        # cnt never reaches 0 after the first '(', so nothing is appended
        assert result == []

    def test_extra_close_bracket(self):
        """Test with extra closing brackets."""
        result = separate_paren_groups('())')
        # After '()', cnt goes back to 0, then ')' makes cnt=-1
        # The ')' gets added but cnt != 0, so nothing more is appended
        assert result == ['())']

    def test_well_known_doctest(self):
        """Re-run the exact doctest example."""
        assert separate_paren_groups('( ) (( )) (( )( ))') == ['()', '(())', '(()())']

    def test_single_char_open(self):
        """Test with a single opening parenthesis."""
        result = separate_paren_groups('(')
        assert result == []

    def test_single_char_close(self):
        """Test with a single closing parenthesis."""
        result = separate_paren_groups(')')
        assert result == [')']

    def test_two_separated_pairs(self):
        """Test two separated pairs."""
        result = separate_paren_groups('( ) ( )')
        assert result == ['()', '()']

    def test_no_spaces_between_groups(self):
        """Test groups directly adjacent without spaces."""
        result = separate_paren_groups('()()')
        assert result == ['()', '()']

    def test_nested_with_inner_spaces(self):
        """Test nested groups with spaces inside."""
        result = separate_paren_groups('(( ))')
        assert result == ['(())']

    def test_large_number_of_groups(self):
        """Test with many small groups."""
        input_str = '() ' * 10
        result = separate_paren_groups(input_str)
        assert len(result) == 10
        assert all(g == '()' for g in result)
