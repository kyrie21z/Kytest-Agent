import pytest
from solution import correct_bracketing


class TestCorrectBracketing:
    """Tests for the correct_bracketing function."""

    # --- Docstring examples ---

    def test_single_opening(self):
        assert correct_bracketing("<") is False

    def test_simple_pair(self):
        assert correct_bracketing("<>") is True

    def test_nested_pairs(self):
        assert correct_bracketing("<<><>>") is True

    def test_reversed_start(self):
        assert correct_bracketing("><<>") is False

    # --- Empty string ---

    def test_empty_string(self):
        assert correct_bracketing("") is True

    # --- Valid bracket sequences ---

    def test_multiple_separate_pairs(self):
        assert correct_bracketing("<><>") is True

    def test_deeply_nested(self):
        assert correct_bracketing("<<<<>>>>") is True

    def test_complex_valid(self):
        assert correct_bracketing("<><<<>>>") is True

    def test_alternating(self):
        assert correct_bracketing("<><><><>") is True

    def test_all_open_then_all_close(self):
        assert correct_bracketing("<<<>>>") is True

    # --- Invalid bracket sequences ---

    def test_single_closing(self):
        assert correct_bracketing(">") is False

    def test_more_closing_than_opening(self):
        assert correct_bracketing("<<>>>") is False

    def test_more_opening_than_closing(self):
        assert correct_bracketing("<<<>>") is False

    def test_closing_before_opening(self):
        assert correct_bracketing("><") is False

    def test_mixed_invalid(self):
        assert correct_bracketing("<<>>><") is False

    def test_interleaved_invalid(self):
        assert correct_bracketing("<><<>>") is True  # actually valid
        assert correct_bracketing("<><><") is False

    def test_ending_with_open(self):
        assert correct_bracketing("<<>> <") is False

    def test_starting_with_close(self):
        assert correct_bracketing("> <>") is False

    # --- Edge cases with longer strings ---

    def test_long_valid(self):
        s = "<" * 50 + ">" * 50
        assert correct_bracketing(s) is True

    def test_long_invalid_extra_close(self):
        s = "<" * 50 + ">" * 51
        assert correct_bracketing(s) is False

    def test_long_invalid_extra_open(self):
        s = "<" * 51 + ">" * 50
        assert correct_bracketing(s) is False

    def test_long_alternating_valid(self):
        s = ("<>" * 50)
        assert correct_bracketing(s) is True

    def test_long_alternating_invalid(self):
        s = ("<><" * 25)
        assert correct_bracketing(s) is False

    # --- Only one type of character ---

    def test_only_opening(self):
        assert correct_bracketing("<<<<") is False

    def test_only_closing(self):
        assert correct_bracketing(">>>>") is False

    # --- Boundary / single-character cases ---

    def test_one_char_open(self):
        assert correct_bracketing("<") is False

    def test_one_char_close(self):
        assert correct_bracketing(">") is False

    def test_two_char_valid(self):
        assert correct_bracketing("<>") is True

    def test_two_char_invalid(self):
        assert correct_bracketing("><") is False
