import pytest
from solution import separate_paren_groups


class TestSeparateParenGroups:
    """Tests for the separate_paren_groups function."""

    # --- Docstring examples ---

    def test_docstring_example(self):
        result = separate_paren_groups('( ) (( )) (( )( ))')
        assert result == ['()', '(())', '(()())']

    # --- Single group cases ---

    def test_single_group_simple(self):
        result = separate_paren_groups('( )')
        assert result == ['()']

    def test_single_group_nested(self):
        result = separate_paren_groups('(( ))')
        assert result == ['(())']

    def test_single_group_deeply_nested(self):
        result = separate_paren_groups('((( )))')
        assert result == ['((()))']

    def test_single_group_no_spaces(self):
        result = separate_paren_groups('()')
        assert result == ['()']

    def test_single_group_complex(self):
        result = separate_paren_groups('(()())')
        assert result == ['(()())']

    # --- Multiple groups ---

    def test_two_groups(self):
        result = separate_paren_groups('( ) ( )')
        assert result == ['()', '()']

    def test_two_groups_different_depths(self):
        result = separate_paren_groups('(( )) ( )')
        assert result == ['(())', '()']

    def test_multiple_groups_no_spaces(self):
        result = separate_paren_groups('()()()')
        assert result == ['()', '()', '()']

    def test_three_groups(self):
        result = separate_paren_groups('( ) (( )) ((( ))))')
        assert result == ['()', '(())', '((()))]

    # --- Empty / edge cases ---

    def test_empty_string(self):
        result = separate_paren_groups('')
        assert result == []

    def test_only_spaces(self):
        result = separate_paren_groups('   ')
        assert result == []

    def test_newlines_and_tabs_preserved(self):
        """The function only ignores spaces, not other whitespace like \\n or \\t."""
        result = separate_paren_groups('  \n  \t  ')
        assert result == ['\n', '\t']

    def test_single_empty_group(self):
        result = separate_paren_groups('()')
        assert result == ['()']

    # --- Whitespace handling ---

    def test_leading_trailing_spaces(self):
        result = separate_paren_groups('  ( )  ')
        assert result == ['()']

    def test_spaces_between_groups(self):
        result = separate_paren_groups('( )   (( ))')
        assert result == ['()', '(())']

    def test_mixed_whitespace_in_groups(self):
        result = separate_paren_groups(' ( )\t(( ))\n (( )( )) ')
        assert result == ['()', '(())', '(()())']

    # --- Complex nesting patterns ---

    def test_alternating_nesting(self):
        result = separate_paren_groups('(()())')
        assert result == ['(()())']

    def test_deeply_nested_with_inner_groups(self):
        result = separate_paren_groups('((()( )))')
        assert result == ['((()( )))']

    def test_many_small_groups(self):
        result = separate_paren_groups('() () () ()')
        assert result == ['()', '()', '()', '()']

    def test_large_input(self):
        # Build a large string with many groups
        groups = ['()'] * 100
        input_str = ' '.join(groups)
        result = separate_paren_groups(input_str)
        assert len(result) == 100
        assert all(g == '()' for g in result)

    # --- Invalid / malformed input (as much as we can test) ---

    def test_unbalanced_raises_nothing_but_returns_partial(self):
        """If the input is unbalanced, the function won't complete a group
        until cnt returns to 0. We test that partial results are returned."""
        result = separate_paren_groups('( ) (')
        # The second '(' never closes, so cnt never returns to 0 after it
        assert result == ['()']

    def test_extra_closing_braces(self):
        result = separate_paren_groups('( ) ) ( )')
        assert result == ['()', '()']

    # --- Return type checks ---

    def test_returns_list(self):
        result = separate_paren_groups('( )')
        assert isinstance(result, list)

    def test_returns_strings_in_list(self):
        result = separate_paren_groups('( ) (( ))')
        assert all(isinstance(s, str) for s in result)
