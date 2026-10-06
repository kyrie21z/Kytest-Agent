import pytest
from solution import find_max


class TestFindMax:
    """Tests for the find_max function."""

    # --- Basic functionality from docstring examples ---

    def test_basic_example_1(self):
        """Word with most unique characters wins."""
        assert find_max(["name", "of", "string"]) == "string"

    def test_basic_example_2(self):
        """Tie broken by lexicographical order."""
        assert find_max(["name", "enam", "game"]) == "enam"

    def test_basic_example_3(self):
        """Single unique character repeated many times."""
        assert find_max(["aaaaaaa", "bb", "cc"]) == "aaaaaaa"

    # --- Edge cases ---

    def test_empty_list(self):
        """Empty list should return empty string."""
        assert find_max([]) == ""

    def test_single_word(self):
        """Single word in list should return that word."""
        assert find_max(["hello"]) == "hello"

    def test_all_same_unique_count(self):
        """When all words have same unique count, pick lexicographically first."""
        assert find_max(["abc", "def", "ghi"]) == "abc"

    def test_duplicate_words(self):
        """List with duplicate words — duplicates don't change result."""
        # "apple" has 4 unique chars, "banana" has 3 → "apple" wins
        assert find_max(["apple", "apple", "banana"]) == "apple"

    def test_case_sensitivity(self):
        """Uppercase and lowercase are distinct characters."""
        # 'Aa' has 2 unique chars ('A', 'a'), 'aa' has 1 unique char ('a')
        assert find_max(["aa", "Aa"]) == "Aa"

    def test_mixed_case_lexicographic_tie(self):
        """Lexicographic ordering considers ASCII values."""
        # Both have 2 unique chars; 'Bb' < 'aa' in ASCII order
        assert find_max(["aa", "Bb"]) == "Bb"

    def test_empty_string_in_list(self):
        """Empty string has 0 unique characters."""
        assert find_max(["", "abc"]) == "abc"

    def test_empty_string_only(self):
        """List containing only empty strings."""
        assert find_max(["", "", ""]) == ""

    def test_single_character_words(self):
        """Words with single characters — all have 1 unique char."""
        assert find_max(["z", "a", "m"]) == "a"

    def test_longer_word_fewer_uniques(self):
        """Longer word doesn't win if it has fewer unique characters."""
        # "aabbc" has 3 unique chars (a,b,c), "xyz" has 3 unique chars (x,y,z)
        # Tie on unique count; "aabbc" < "xyz" lexicographically
        assert find_max(["aabbc", "xyz"]) == "aabbc"

    def test_numbers_and_special_chars(self):
        """Words containing digits and special characters."""
        assert find_max(["a1b2c3", "abc"]) == "a1b2c3"

    def test_spaces_in_words(self):
        """Words containing spaces count as unique characters."""
        # "a b" has 3 unique chars (a, space, b), "abc" has 3 unique chars (a,b,c)
        # Tie on unique count; "a b" < "abc" (space < 'c' in ASCII)
        assert find_max(["a b", "abc"]) == "a b"

    def test_two_way_tie_corrected(self):
        """Two words with different unique counts — higher unique count wins."""
        # "zebra" has 5 unique chars, "apple" has 4 unique chars
        assert find_max(["zebra", "apple"]) == "zebra"

    def test_three_way_tie(self):
        """Three words with same unique count — pick first lexicographically."""
        assert find_max(["cab", "bac", "abc"]) == "abc"

    def test_prefix_relationship(self):
        """One word is a prefix of another."""
        # "app" has 2 unique chars, "apple" has 4 unique chars
        assert find_max(["app", "apple"]) == "apple"

    def test_repeated_characters_dominant(self):
        """Word with many repeats but still more unique chars wins."""
        assert find_max(["aabbccdd", "abcdef"]) == "abcdef"

    def test_unicode_characters(self):
        """Unicode characters are treated as distinct."""
        # "café" has 4 unique chars (c,a,f,é), "cafe" has 4 unique chars (c,a,f,e)
        # Tie on unique count; "cafe" < "café" lexicographically
        assert find_max(["café", "cafe"]) == "cafe"

    def test_all_identical_words(self):
        """All words identical — return any one (the first)."""
        result = find_max(["test", "test", "test"])
        assert result == "test"

    def test_large_list(self):
        """Test with a larger list of words."""
        words = ["a", "ab", "abc", "abcd", "abcde"]
        assert find_max(words) == "abcde"

    def test_reverse_order_large_to_small(self):
        """Largest unique-count word appears last."""
        words = ["abcde", "abcd", "abc", "ab", "a"]
        assert find_max(words) == "abcde"

    def test_lexicographic_first_among_equals(self):
        """Ensure lexicographic ordering picks the correct winner on ties."""
        # All have 3 unique chars: abc, bac, cab
        assert find_max(["cab", "bac", "abc"]) == "abc"

    def test_word_with_all_same_chars(self):
        """Word where every character is the same."""
        assert find_max(["zzzz", "abc"]) == "abc"

    def test_none_values_not_expected(self):
        """Function expects strings; None is not a valid input per contract."""
        # This test documents expected behavior — passing None would raise TypeError.
        with pytest.raises(TypeError):
            find_max([None])

    def test_tie_with_different_lengths(self):
        """Tie broken by lex order even when lengths differ."""
        # "ab" has 2 unique chars, "cd" has 2 unique chars
        assert find_max(["cd", "ab"]) == "ab"

    def test_many_words_same_unique_count(self):
        """Many words with same unique count — lex first wins."""
        words = ["zyx", "cba", "fed", "abc"]
        assert find_max(words) == "abc"

    def test_word_with_repeating_pattern(self):
        """Word with repeating pattern has fewer unique chars."""
        # "abab" has 2 unique chars, "abcd" has 4 unique chars
        assert find_max(["abab", "abcd"]) == "abcd"
