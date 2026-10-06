import pytest
from solution import flip_case


class TestFlipCase:
    """Tests for the flip_case function."""

    def test_basic_mixed_case(self):
        """Test basic mixed-case string from docstring."""
        assert flip_case('Hello') == 'hELLO'

    def test_all_lowercase(self):
        """Test converting all lowercase to uppercase."""
        assert flip_case('abc') == 'ABC'

    def test_all_uppercase(self):
        """Test converting all uppercase to lowercase."""
        assert flip_case('ABC') == 'abc'

    def test_empty_string(self):
        """Test with an empty string."""
        assert flip_case('') == ''

    def test_no_letters(self):
        """Test with a string containing only numbers and symbols."""
        assert flip_case('123!@#') == '123!@#'

    def test_numbers_preserved(self):
        """Test that numbers remain unchanged."""
        assert flip_case('a1B2c3') == 'A1b2C3'

    def test_special_characters_preserved(self):
        """Test that special characters remain unchanged."""
        assert flip_case('hello world!') == 'HELLO WORLD!'

    def test_spaces_preserved(self):
        """Test that spaces remain unchanged."""
        assert flip_case('hello world') == 'HELLO WORLD'

    def test_single_lowercase_char(self):
        """Test with a single lowercase character."""
        assert flip_case('a') == 'A'

    def test_single_uppercase_char(self):
        """Test with a single uppercase character."""
        assert flip_case('Z') == 'z'

    def test_alternating_case(self):
        """Test with alternating upper and lower case."""
        assert flip_case('AbCdEf') == 'aBcDeF'

    def test_long_string(self):
        """Test with a longer string."""
        result = flip_case('Python is Fun!')
        assert result == 'pYTHON IS fUN!'

    def test_unicode_letters(self):
        """Test with unicode characters that have case."""
        assert flip_case('café') == 'CAFÉ'

    def test_whitespace_only(self):
        """Test with only whitespace characters."""
        assert flip_case('   ') == '   '

    def test_returns_string_type(self):
        """Test that the return type is always str."""
        assert isinstance(flip_case('Hello'), str)
        assert isinstance(flip_case(''), str)
