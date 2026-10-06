import pytest
from solution import count_upper


class TestCountUpper:
    """Unit tests for the count_upper function."""

    # --- Docstring examples ---

    def test_docstring_example_1(self):
        """count_upper('aBCdEf') returns 1"""
        assert count_upper("aBCdEf") == 1

    def test_docstring_example_2(self):
        """count_upper('abcdefg') returns 0"""
        assert count_upper("abcdefg") == 0

    def test_docstring_example_3(self):
        """count_upper('dBBE') returns 0"""
        assert count_upper("dBBE") == 0

    # --- Empty and single-character strings ---

    def test_empty_string(self):
        """An empty string should return 0."""
        assert count_upper("") == 0

    def test_single_lowercase_vowel_at_index_0(self):
        """Single lowercase vowel at index 0 should return 0."""
        assert count_upper("a") == 0

    def test_single_uppercase_vowel_at_index_0(self):
        """Single uppercase vowel at index 0 should return 1."""
        assert count_upper("A") == 1

    def test_single_consonant_at_index_0(self):
        """Single consonant at index 0 should return 0."""
        assert count_upper("B") == 0

    def test_single_non_letter_at_index_0(self):
        """Single non-letter character at index 0 should return 0."""
        assert count_upper("1") == 0

    # --- All uppercase vowels at even indices ---

    def test_all_uppercase_vowels_even_indices(self):
        """Every even index is an uppercase vowel."""
        assert count_upper("AEIOU") == 3  # indices 0, 2, 4

    def test_alternating_uppercase_vowel_and_consonant(self):
        """Uppercase vowels only at even indices."""
        assert count_upper("ABCD") == 1  # 'A' at index 0

    # --- No uppercase vowels at even indices ---

    def test_no_uppercase_vowels_at_even_indices(self):
        """No uppercase vowels appear at any even index."""
        assert count_upper("bcdFghj") == 0

    def test_lowercase_vowels_at_even_indices(self):
        """Lowercase vowels at even indices should not be counted."""
        assert count_upper("aeiou") == 0

    def test_uppercase_consonants_at_even_indices(self):
        """Uppercase consonants at even indices should not be counted."""
        assert count_upper("BCDFG") == 0

    # --- Mixed content ---

    def test_mixed_case_with_some_matches(self):
        """Mixed case string with some uppercase vowels at even indices.
        
        String: a E i O u
        Index:  0 1 2 3 4
        Even indices: 0='a', 2='i', 4='u' -> none are uppercase vowels
        But wait: we also need to check if there's an uppercase vowel at even index.
        Actually 'O' is at index 3 (odd), so it doesn't count.
        Result: 0 uppercase vowels at even indices.
        """
        assert count_upper("aEiOu") == 0

    def test_uppercase_vowels_only_at_odd_indices(self):
        """Uppercase vowels at odd indices should not be counted."""
        assert count_upper("bAdEd") == 0

    def test_special_characters_in_string(self):
        """Special characters at even indices should not affect count."""
        assert count_upper("!@#$%") == 0

    def test_numbers_in_string(self):
        """Numbers at even indices should not affect count."""
        assert count_upper("12345") == 0

    def test_longer_string_with_multiple_matches(self):
        """Longer string with multiple uppercase vowels at even indices.
        
        String: A b C d E f G h I j K l M n O p Q r S t U v W x Y z
        Index:  0 1 2 3 4 5 6 7 8 9 ...
        Even indices with uppercase vowels: 0=A, 4=E, 8=I, 14=O, 20=U -> 5 matches
        """
        assert count_upper("AbCdEfGhIjKlMnOpQrStUvWxYz") == 5

    def test_all_same_character(self):
        """String with repeated uppercase vowels."""
        assert count_upper("AAAAA") == 3  # indices 0, 2, 4

    def test_all_same_character_lowercase(self):
        """String with repeated lowercase vowels."""
        assert count_upper("aaaaa") == 0

    # --- Even-length strings ---

    def test_even_length_string(self):
        """Even-length string with uppercase vowels at even indices.
        
        String: A E a e
        Index:  0 1 2 3
        Even indices: 0='A'(uppercase vowel), 2='a'(lowercase) -> 1 match
        """
        assert count_upper("AEae") == 1

    def test_even_length_no_matches(self):
        """Even-length string with no uppercase vowels at even indices."""
        assert count_upper("bcda") == 0

    # --- Odd-length strings ---

    def test_odd_length_string(self):
        """Odd-length string with uppercase vowels at even indices."""
        assert count_upper("abcde") == 0

    def test_odd_length_with_matches(self):
        """Odd-length string with uppercase vowels at even indices.
        
        String: a E i
        Index:  0 1 2
        Even indices: 0='a'(lowercase), 2='i'(lowercase) -> 0 matches
        """
        assert count_upper("aEi") == 0

    # --- Edge cases with non-vowel uppercase letters ---

    def test_uppercase_consonant_pattern(self):
        """Only uppercase consonants at even indices."""
        assert count_upper("BCDFGH") == 0

    def test_mixed_vowels_and_consonants(self):
        """Mix of uppercase vowels and consonants at even indices.
        
        String: A B C D E F
        Index:  0 1 2 3 4 5
        Even indices: 0='A'(yes), 2='C'(no), 4='E'(yes) -> 2 matches
        """
        assert count_upper("ABCDEF") == 2

    # --- Whitespace handling ---

    def test_whitespace_at_even_indices(self):
        """Whitespace at even indices should not be counted."""
        assert count_upper("a b c d") == 0

    def test_spaces_between_uppercase_vowels(self):
        """Spaces between uppercase vowels at even indices."""
        assert count_upper("A B C D") == 1  # 'A' at index 0

    # --- Comprehensive stress-like test ---

    def test_comprehensive_mixed_string(self):
        """A longer string with a mix of characters.
        
        String: Hello World! This is a TEST.
        Even indices chars: 0=H, 2=l, 4=o, 6=W, 8=r, 10=d, 12=' ', 14=h, 16=s, 18=i, 20=' ', 22=' ', 24=E, 26=T
        Uppercase vowels at even indices: E at index 24 -> 1 match
        """
        s = "Hello World! This is a TEST."
        assert count_upper(s) == 1

    def test_string_with_many_uppercase_vowels(self):
        """String designed to have many uppercase vowels at even indices.
        
        String: A e I o U
        Index:  0 1 2 3 4
        Even indices: 0=A(yes), 2=I(yes), 4=U(yes) -> 3 matches
        """
        s = "AeIoU"
        assert count_upper(s) == 3
