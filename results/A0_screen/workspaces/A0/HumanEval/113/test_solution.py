import pytest
from solution import odd_count


class TestOddCountBasic:
    """Test basic functionality as described in the docstring."""

    def test_single_string_four_odds(self):
        """From docstring: '1234567' has 4 odd digits (1,3,5,7)."""
        result = odd_count(['1234567'])
        expected = ["the number of odd elements 4n the str4ng 4 of the 4nput."]
        assert result == expected

    def test_two_strings(self):
        """From docstring: '3' has 1 odd, '11111111' has 8 odds."""
        result = odd_count(['3', '11111111'])
        expected = [
            "the number of odd elements 1n the str1ng 1 of the 1nput.",
            "the number of odd elements 8n the str8ng 8 of the 8nput.",
        ]
        assert result == expected


class TestOddCountEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_list(self):
        """An empty input list should return an empty list."""
        result = odd_count([])
        assert result == []

    def test_empty_string(self):
        """An empty string has zero odd digits."""
        result = odd_count([''])
        expected = ["the number of odd elements 0n the str0ng 0 of the 0nput."]
        assert result == expected

    def test_no_odd_digits(self):
        """A string with only even digits should yield count 0."""
        result = odd_count(['2468'])
        expected = ["the number of odd elements 0n the str0ng 0 of the 0nput."]
        assert result == expected

    def test_all_odd_digits(self):
        """A string with all odd digits."""
        result = odd_count(['13579'])
        expected = ["the number of odd elements 5n the str5ng 5 of the 5nput."]
        assert result == expected

    def test_single_even_digit(self):
        """A single even digit string."""
        result = odd_count(['8'])
        expected = ["the number of odd elements 0n the str0ng 0 of the 0nput."]
        assert result == expected

    def test_single_odd_digit(self):
        """A single odd digit string."""
        result = odd_count(['7'])
        expected = ["the number of odd elements 1n the str1ng 1 of the 1nput."]
        assert result == expected


class TestOddCountMultipleStrings:
    """Test with multiple strings in the input list."""

    def test_mixed_odds_and_evens(self):
        """Mix of strings with varying odd counts."""
        result = odd_count(['123', '456', '789'])
        # '123' -> 2 odds (1,3), '456' -> 1 odd (5), '789' -> 2 odds (7,9)
        expected = [
            "the number of odd elements 2n the str2ng 2 of the 2nput.",
            "the number of odd elements 1n the str1ng 1 of the 1nput.",
            "the number of odd elements 2n the str2ng 2 of the 2nput.",
        ]
        assert result == expected

    def test_repeated_strings(self):
        """Same string appearing multiple times."""
        result = odd_count(['111', '111'])
        expected = [
            "the number of odd elements 3n the str3ng 3 of the 3nput.",
            "the number of odd elements 3n the str3ng 3 of the 3nput.",
        ]
        assert result == expected

    def test_large_number_of_odds(self):
        """String with many odd digits (count > 9)."""
        result = odd_count(['11111111111111111111'])  # 20 ones
        expected = ["the number of odd elements 20n the str20ng 20 of the 20nput."]
        assert result == expected


class TestOddCountOutputFormat:
    """Test that the output format is correct."""

    def test_output_is_list(self):
        """Return value should be a list."""
        result = odd_count(['1'])
        assert isinstance(result, list)

    def test_output_elements_are_strings(self):
        """Each element in the returned list should be a string."""
        result = odd_count(['1'])
        assert all(isinstance(s, str) for s in result)

    def test_output_length_matches_input(self):
        """Length of output list should equal length of input list."""
        for n in range(6):
            lst = [str(i) for i in range(n)]
            result = odd_count(lst)
            assert len(result) == len(lst)

    def test_template_structure_preserved(self):
        """The template text structure should be preserved after replacement."""
        result = odd_count(['1'])
        # The function replaces every 'i' with the count, so check key parts
        assert "the number of odd elements" in result[0]
        assert "of the" in result[0]
        assert "nput." in result[0]
