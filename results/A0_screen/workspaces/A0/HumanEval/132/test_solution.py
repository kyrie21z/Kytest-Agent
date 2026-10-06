import pytest
from solution import is_nested


class TestIsNestedBasicCases:
    """Tests based on the docstring examples."""

    def test_nested_brackets(self):
        assert is_nested('[[]]') is True

    def test_invalid_mixed_brackets(self):
        assert is_nested('[]]]]]]][[[[[]') is False

    def test_separate_pairs_no_nesting(self):
        assert is_nested('[][]') is False

    def test_single_pair_no_nesting(self):
        assert is_nested('[]') is False

    def test_nested_within_pairs(self):
        assert is_nested('[[][]]') is True

    def test_nested_with_trailing_open(self):
        assert is_nested('[[]][[') is True


class TestIsNestedEmptyAndSimple:
    """Tests for edge cases with empty or trivial inputs."""

    def test_empty_string(self):
        assert is_nested('') is False

    def test_single_open_bracket(self):
        assert is_nested('[') is False

    def test_single_close_bracket(self):
        assert is_nested(']') is False

    def test_only_open_brackets(self):
        assert is_nested('[[[') is False

    def test_only_close_brackets(self):
        assert is_nested(']]]') is False

    def test_two_open_brackets(self):
        assert is_nested('[[') is False

    def test_two_close_brackets(self):
        assert is_nested(']]') is False


class TestIsNestedNoNesting:
    """Tests for strings that are valid but have no nesting."""

    def test_alternating_pairs(self):
        assert is_nested('[][][][]') is False

    def test_four_pairs_in_a_row(self):
        assert is_nested('[][][][][][]') is False

    def test_two_pairs(self):
        assert is_nested('[][]') is False

    def test_three_pairs(self):
        assert is_nested('[][][]') is False


class TestIsNestedWithNesting:
    """Tests for strings that contain nested brackets."""

    def test_double_nesting(self):
        assert is_nested('[[[]]]') is True

    def test_triple_nesting(self):
        assert is_nested('[[[[]]]]') is True

    def test_nested_at_start(self):
        assert is_nested('[[]][][]') is True

    def test_nested_at_end(self):
        assert is_nested('[][[]]') is True

    def test_nested_in_middle(self):
        assert is_nested('[][[]][]') is True

    def test_deeply_nested(self):
        assert is_nested('[[[[]]]]') is True

    def test_complex_nested(self):
        assert is_nested('[[][][[]]]') is True

    def test_multiple_nested_sections(self):
        assert is_nested('[[]][[]]') is True

    def test_nested_inside_larger_structure(self):
        assert is_nested('[[[]][[]]]') is True


class TestIsNestedInvalidStrings:
    """Tests for invalid/unbalanced bracket strings."""

    def test_more_closes_than_opens(self):
        assert is_nested('][') is False

    def test_more_closes_than_opens_longer(self):
        assert is_nested(']][') is False

    def test_unbalanced_starting_with_close(self):
        assert is_nested('][[]') is False

    def test_unbalanced_ending_with_open(self):
        assert is_nested('[[][') is False

    def test_interleaved_invalid(self):
        assert is_nested('[]][') is False

    def test_all_close_then_all_open(self):
        assert is_nested(']][[') is False

    def test_random_unbalanced(self):
        assert is_nested('[]]]]][[[[') is False


class TestIsNestedLongerStrings:
    """Tests with longer bracket sequences."""

    def test_long_valid_no_nesting(self):
        assert is_nested('[]' * 10) is False

    def test_long_valid_with_nesting(self):
        assert is_nested('[]' * 5 + '[[]]' + '[]' * 5) is True

    def test_very_deep_nesting(self):
        s = '[' * 10 + ']' * 10
        assert is_nested(s) is True

    def test_alternating_with_one_nested_section(self):
        assert is_nested('[][][[]][][]') is True

    def test_large_balanced_no_nesting(self):
        assert is_nested('[]' * 100) is False


class TestIsNestedEdgeCases:
    """Additional edge case tests."""

    def test_minimal_nested(self):
        assert is_nested('[[]]') is True

    def test_nested_immediately_followed_by_nested(self):
        assert is_nested('[[][]]') is True

    def test_overlapping_nested_looks(self):
        assert is_nested('[[[]]]') is True

    def test_nested_but_not_fully_balanced_substring(self):
        # The whole string isn't balanced, but a balanced substring with nesting exists
        assert is_nested('[[]][[') is True

    def test_balanced_outer_with_nested_inner(self):
        assert is_nested('[[][[]]]') is True

    def test_nested_pair_surrounded_by_other_pairs(self):
        assert is_nested('[][[]][]') is True
