"""Unit tests for separate_paren_groups in solution.py."""

import pytest
from solution import separate_paren_groups


class TestSeparateParenGroups_NormalCases:
    """Test normal / typical inputs."""

    def test_example_from_docstring(self):
        """The exact example from the docstring."""
        result = separate_paren_groups('( ) (( )) (( )( ))')
        assert result == ['()', '(())', '(()())']

    def test_single_group_no_spaces(self):
        """A single balanced group with no spaces."""
        result = separate_paren_groups('(())')
        assert result == ['(())']

    def test_two_simple_groups(self):
        """Two simple top-level groups concatenated."""
        result = separate_paren_groups('()()')
        assert result == ['()', '()']

    def test_mixed_depth_groups(self):
        """Groups with different nesting depths side by side."""
        result = separate_paren_groups('(())(())')
        assert result == ['(())', '(())']

    def test_deeply_nested_single_group(self):
        """A single group with deep nesting."""
        result = separate_paren_groups('(((())))')
        assert result == ['(((())))']

    def test_many_simple_groups(self):
        """Many simple groups separated by spaces."""
        result = separate_paren_groups('() () () ()')
        assert result == ['()', '()', '()', '()']

    def test_complex_mixed(self):
        """Multiple groups with varying complexity and spaces."""
        result = separate_paren_groups('(()(())) (()) ()')
        assert result == ['(()(()))', '(())', '()']

    def test_single_char_pairs_repeated(self):
        """Repeated single-pair groups."""
        result = separate_paren_groups('()()()')
        assert result == ['()', '()', '()']


class TestSeparateParenGroups_BoundaryCases:
    """Test boundary values at edges of valid input ranges."""

    def test_minimal_valid_input(self):
        """Minimal valid non-empty input: one pair."""
        result = separate_paren_groups('()')
        assert result == ['()']

    def test_maximal_nesting_single_group(self):
        """Single group with many levels of nesting."""
        # Build a deeply nested string programmatically
        n = 100
        inner = '(' * n + ')' * n
        result = separate_paren_groups(inner)
        assert result == [inner]

    def test_many_groups_boundary(self):
        """Large number of groups."""
        n = 100
        input_str = ' '.join(['()'] * n)
        result = separate_paren_groups(input_str)
        assert result == ['()'] * n

    def test_adjacent_groups_no_space(self):
        """Two groups directly adjacent without space separator."""
        result = separate_paren_groups('()()')
        assert result == ['()', '()']

    def test_trailing_and_leading_spaces(self):
        """Spaces before the first group and after the last."""
        result = separate_paren_groups('  (())  (()())  ')
        assert result == ['(())', '(()())']

    def test_spaces_between_all_chars(self):
        """Every character separated by a space."""
        result = separate_paren_groups('( ) ( ( ) )')
        assert result == ['()', '(())']


class TestSeparateParenGroups_EmptyAndWhitespace:
    """Test empty, null-like, or whitespace-only inputs."""

    def test_empty_string(self):
        """Completely empty string should return an empty list."""
        result = separate_paren_groups('')
        assert result == []

    def test_only_spaces(self):
        """String containing only spaces."""
        result = separate_paren_groups('     ')
        assert result == []

    def test_only_newlines_and_tabs(self):
        """String with newlines and tabs but no parens.
        
        Note: the function only ignores spaces (' '), not newlines or tabs.
        So non-space characters like \\n and \\t are kept as-is.
        """
        result = separate_paren_groups('\n\n\t\t')
        # Non-space chars are preserved; they never form a paren group
        # cnt stays 0 throughout, but group accumulates non-space chars
        # Since cnt==0 after each char and group != "", each non-space char
        # gets appended individually.
        assert result == ['\n', '\n', '\t', '\t']

    def test_single_space(self):
        """Just one space character."""
        result = separate_paren_groups(' ')
        assert result == []

    def test_newline_with_parens(self):
        """Newlines between parens are NOT ignored (only spaces are)."""
        result = separate_paren_groups('(\n)')
        # All chars including \n are part of the group since only spaces are skipped
        assert result == ['(\n)']


class TestSeparateParenGroups_InvalidInputs:
    """Test inputs that are unbalanced or otherwise malformed.

    The function does not explicitly validate input; it processes whatever
    characters it finds. We document its actual behavior on invalid inputs.
    """

    def test_unclosed_open_paren(self):
        """An open paren without a matching close — never reaches cnt==0
        after starting a group, so nothing is emitted."""
        result = separate_paren_groups('(()')
        assert result == []

    def test_unclosed_open_paren_with_valid_prefix(self):
        """Valid group followed by an unclosed group."""
        result = separate_paren_groups('()((')
        assert result == ['()']

    def test_extra_closing_paren(self):
        """Extra closing paren causes negative count; group still emitted
        when cnt returns to 0."""
        # Input: )( -> cnt goes -1 then 0, group = ")("
        result = separate_paren_groups(')( ')
        assert result == [')(']

    def test_extra_closing_paren_after_valid(self):
        """Valid group, then extra close, then open — they cancel."""
        # Input: ()) ( -> first () emits, then )( emits when cnt hits 0
        result = separate_paren_groups('())(')
        assert result == ['()', ')(']

    def test_reverse_order_parens(self):
        """All closes before opens."""
        # Input: ))(( -> cnt goes -1,-2,-1,0; group = ")) (("
        result = separate_paren_groups('))((')
        assert result == ['))((']

    def test_interleaved_invalid(self):
        """Interleaved open/close that never form a balanced group."""
        result = separate_paren_groups('()(()')
        assert result == ['()']


class TestSeparateParenGroups_TypeErrors:
    """Test that passing non-string types raises TypeError."""

    @pytest.mark.parametrize("invalid_input", [None, 42, 3.14, True])
    def test_non_string_raises_type_error(self, invalid_input):
        """Passing a non-string should raise TypeError."""
        with pytest.raises(TypeError):
            separate_paren_groups(invalid_input)

    def test_list_does_not_raise(self):
        """Lists are iterable, so no TypeError is raised (but result is odd)."""
        # This is documented as NOT raising TypeError since lists are iterable
        result = separate_paren_groups([])
        assert result == []

    def test_dict_does_not_raise(self):
        """Dicts are iterable (over keys), so no TypeError is raised."""
        result = separate_paren_groups({})
        assert result == []


class TestSeparateParenGroups_EdgeGroupings:
    """Additional edge-case groupings."""

    def test_single_nested_pair(self):
        """One level of nesting inside another."""
        result = separate_paren_groups('(()')
        assert result == []

    def test_alternating_groups(self):
        """Alternating simple and nested groups."""
        result = separate_paren_groups('()(())()((()))')
        assert result == ['()', '(())', '()', '((()))']

    def test_group_with_inner_spaces(self):
        """Spaces inside a group should be ignored."""
        result = separate_paren_groups('( ( ) )')
        assert result == ['(())']

    def test_consecutive_same_depth_groups(self):
        """Multiple same-depth groups back to back."""
        result = separate_paren_groups('(())(())(())')
        assert result == ['(())', '(())', '(())']

    def test_wide_flat_structure(self):
        """Wide structure: many siblings at the same level."""
        result = separate_paren_groups('(()()()())')
        assert result == ['(()()()())']
