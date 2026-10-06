import pytest
from solution import match_parens


class TestMatchParens:
    """Tests for the match_parens function."""

    # --- Docstring examples ---

    def test_example_1(self):
        """Example 1: ['()(', ')'] -> 'Yes'"""
        assert match_parens(['()(', ')']) == 'Yes'

    def test_example_2(self):
        """Example 2: [')', ')'] -> 'No'"""
        assert match_parens([')', ')']) == 'No'

    # --- Basic balanced cases ---

    def test_both_already_balanced(self):
        """Both strings are individually balanced."""
        assert match_parens(['()', '()']) == 'Yes'

    def test_one_balanced_one_empty_like(self):
        """One balanced string paired with empty-like single chars."""
        assert match_parens(['(())', '']) == 'Yes'

    def test_simple_pair(self):
        """Simple '(' + ')' combination."""
        assert match_parens(['(', ')']) == 'Yes'

    def test_reversed_simple_pair(self):
        """Reversed order of simple pair."""
        assert match_parens([')', '(']) == 'Yes'

    # --- Cases that should return 'No' ---

    def test_all_open_parens(self):
        """All open parentheses cannot be balanced."""
        assert match_parens(['(((', '))']) == 'No'

    def test_imbalanced_total_count(self):
        """Total number of '(' and ')' differ, so impossible to balance."""
        assert match_parens(['(()', '))']) == 'No'

    def test_two_closing_parens(self):
        """Two closing parens alone."""
        assert match_parens([')', ')']) == 'No'

    def test_two_opening_parens(self):
        """Two opening parens alone."""
        assert match_parens(['(', '(']) == 'No'

    # --- Both orders produce balanced results ---

    def test_both_orders_work(self):
        """Both concatenation orders produce balanced strings."""
        assert match_parens(['()', '()']) == 'Yes'

    # --- Longer strings ---

    def test_longer_balanced_combo(self):
        """Longer strings that together form a balanced result."""
        assert match_parens(['((()))', '))(((']) == 'No'

    def test_nested_balanced(self):
        """Nested parentheses across both strings."""
        assert match_parens(['(((', ')))']) == 'Yes'

    def test_complex_mixed_no_match(self):
        """Complex mixed parentheses that do NOT balance."""
        assert match_parens([')()(', '))']) == 'No'

    # --- Edge cases with single characters ---

    def test_single_open_and_single_close(self):
        """Single '(' and single ')'."""
        assert match_parens(['(', ')']) == 'Yes'

    def test_single_close_and_single_open(self):
        """Single ')' and single '('."""
        assert match_parens([')', '(']) == 'Yes'

    def test_two_single_open(self):
        """Two single '(' characters."""
        assert match_parens(['(', '(']) == 'No'

    def test_two_single_close(self):
        """Two single ')' characters."""
        assert match_parens([')', ')']) == 'No'

    # --- Symmetric / identity-like cases ---

    def test_identical_balanced_strings(self):
        """Both strings are identical and balanced."""
        assert match_parens(['()', '()']) == 'Yes'

    def test_identical_unbalanced_strings(self):
        """Both strings are identical and unbalanced."""
        assert match_parens([')( ', ')( ']) == 'No'

    # --- Additional tricky cases ---

    def test_deeply_nested(self):
        """Deeply nested parentheses split across strings."""
        assert match_parens(['(((', ')))']) == 'Yes'

    def test_interleaves_with_extra_close(self):
        """Pattern where extra close paren makes it unbalanced in one order."""
        assert match_parens(['()()(', '))']) == 'No'

    def test_interleaves_with_one_close(self):
        """Pattern where one close paren completes the balance."""
        assert match_parens(['()()(', ')']) == 'Yes'
