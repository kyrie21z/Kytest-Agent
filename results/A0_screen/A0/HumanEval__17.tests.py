import pytest
from solution import parse_music


class TestParseMusic:
    """Tests for the parse_music function."""

    def test_example_from_docstring(self):
        """Test the example provided in the docstring."""
        result = parse_music('o o| .| o| o| .| .| .| .| o o')
        expected = [4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]
        assert result == expected

    def test_single_whole_note(self):
        """Test parsing a single whole note."""
        assert parse_music('o') == [4]

    def test_single_half_note(self):
        """Test parsing a single half note."""
        assert parse_music('o|') == [2]

    def test_single_quarter_note(self):
        """Test parsing a single quarter note."""
        assert parse_music('.|') == [1]

    def test_all_whole_notes(self):
        """Test parsing multiple whole notes."""
        assert parse_music('o o o') == [4, 4, 4]

    def test_all_half_notes(self):
        """Test parsing multiple half notes."""
        assert parse_music('o| o| o|') == [2, 2, 2]

    def test_all_quarter_notes(self):
        """Test parsing multiple quarter notes."""
        assert parse_music('.| .| .|') == [1, 1, 1]

    def test_empty_string(self):
        """Test parsing an empty string."""
        assert parse_music('') == []

    def test_two_notes_different_types(self):
        """Test parsing two different note types."""
        assert parse_music('o o|') == [4, 2]
        assert parse_music('o| o') == [2, 4]

    def test_alternating_notes(self):
        """Test parsing alternating note types."""
        assert parse_music('o .| o| .|') == [4, 1, 2, 1]

    def test_long_sequence(self):
        """Test parsing a longer sequence of notes."""
        result = parse_music('o o| .| o| .| o o| .|')
        expected = [4, 2, 1, 2, 1, 4, 2, 1]
        assert result == expected

    def test_returns_list_of_integers(self):
        """Ensure the return type is a list of integers."""
        result = parse_music('o o| .|')
        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)

    def test_order_preserved(self):
        """Ensure the order of beats matches the order of notes."""
        result = parse_music('o o| .| o| o')
        assert result == [4, 2, 1, 2, 4]
