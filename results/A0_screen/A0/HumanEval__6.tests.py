import pytest
from solution import parse_nested_parens


class TestParseNestedParens:
    """Tests for the parse_nested_parens function."""

    def test_example_from_docstring(self):
        """Test the example provided in the docstring."""
        result = parse_nested_parens('(()()) ((())) () ((())()())')
        assert result == [2, 3, 1, 3]

    def test_single_group_no_nesting(self):
        """A single pair of parentheses has depth 1."""
        result = parse_nested_parens('()')
        assert result == [1]

    def test_single_group_deep_nesting(self):
        """Deeply nested single group."""
        result = parse_nested_parens('((()))')
        assert result == [3]

    def test_single_group_very_deep_nesting(self):
        """Very deeply nested single group (depth 6)."""
        # '(((((())))))' has 6 opens then 6 closes -> max depth 6
        result = parse_nested_parens('(((((())))))')
        assert result == [6]

    def test_multiple_groups_same_depth(self):
        """Multiple groups all with the same nesting depth."""
        result = parse_nested_parens('() () ()')
        assert result == [1, 1, 1]

    def test_multiple_groups_different_depths(self):
        """Groups with varying nesting depths."""
        result = parse_nested_parens('() (()) ((())) (((())))')
        assert result == [1, 2, 3, 4]

    def test_alternating_depths(self):
        """Groups alternating between different depths."""
        result = parse_nested_parens('(()) () (())')
        assert result == [2, 1, 2]

    def test_empty_string(self):
        """Empty input string should return an empty list."""
        result = parse_nested_parens('')
        assert result == []

    def test_only_spaces(self):
        """String containing only spaces should return an empty list."""
        result = parse_nested_parens('   ')
        assert result == []

    def test_mixed_spaces_and_empty_groups(self):
        """Multiple spaces between groups should be handled correctly."""
        result = parse_nested_parens('()  (())   ((()))')
        assert result == [1, 2, 3]

    def test_unbalanced_parentheses_opening(self):
        """Unbalanced parentheses with extra opening brackets."""
        # '(()' has max depth 2: first '(' -> cnt=1, second '(' -> cnt=2, ')' -> cnt=1
        result = parse_nested_parens('(()')
        assert result == [2]

    def test_unbalanced_parentheses_closing(self):
        """Unbalanced parentheses with extra closing brackets."""
        result = parse_nested_parens('())')
        assert result == [1]

    def test_complex_balanced_groups(self):
        """Complex balanced groups with mixed nesting."""
        result = parse_nested_parens('(()()) ((())) () ((())()())')
        assert result == [2, 3, 1, 3]

    def test_maximal_nesting_in_one_group(self):
        """Group with many levels of nesting."""
        # '((((((((()))))))))' has 8 opens + 1 from inner () + 8 closes = max depth 9
        result = parse_nested_parens('((((((((()))))))))')
        assert result == [9]

    def test_single_char_groups(self):
        """Each group is just a single pair of parentheses."""
        result = parse_nested_parens('() (()) (()()) ((()))')
        assert result == [1, 2, 2, 3]

    def test_groups_with_inner_structure(self):
        """Groups with inner structure but same max depth."""
        result = parse_nested_parens('(()()) (()())')
        assert result == [2, 2]

    def test_well_known_patterns(self):
        """Test well-known parenthesis patterns."""
        # Dyck path patterns
        result = parse_nested_parens('() (()) (()()) ((()))')
        assert result == [1, 2, 2, 3]

    def test_large_input(self):
        """Test with a large number of groups."""
        groups = '() ' * 100
        result = parse_nested_parens(groups.strip())
        assert len(result) == 100
        assert all(depth == 1 for depth in result)

    def test_deep_nesting_large_input(self):
        """Test with many deeply nested groups."""
        groups = '((())) ' * 50
        result = parse_nested_parens(groups.strip())
        assert len(result) == 50
        assert all(depth == 3 for depth in result)
