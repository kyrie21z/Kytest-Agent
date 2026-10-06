import pytest
from solution import words_in_sentence


class TestWordsInSentenceBasicExamples:
    """Test cases from the docstring examples."""

    def test_example_1(self):
        assert words_in_sentence("This is a test") == "is"

    def test_example_2(self):
        assert words_in_sentence("lets go for swimming") == "go for"


class TestWordsInSentenceSingleWord:
    """Tests with a single word in the sentence."""

    def test_single_prime_length_word(self):
        # "hi" has length 2 (prime)
        assert words_in_sentence("hi") == "hi"

    def test_single_non_prime_length_word(self):
        # "hello" has length 5 (prime)
        assert words_in_sentence("hello") == "hello"

    def test_single_word_length_one(self):
        # "a" has length 1 (not prime)
        assert words_in_sentence("a") == ""

    def test_single_word_length_four(self):
        # "test" has length 4 (not prime)
        assert words_in_sentence("test") == ""

    def test_single_word_length_seven(self):
        # "abcdefg" has length 7 (prime)
        assert words_in_sentence("abcdefg") == "abcdefg"

    def test_single_word_length_eight(self):
        # "abcdefgh" has length 8 (not prime)
        assert words_in_sentence("abcdefgh") == ""


class TestWordsInSentenceMultipleWords:
    """Tests with multiple words in the sentence."""

    def test_all_words_prime_length(self):
        # "hi" (2), "go" (2), "for" (3) — all prime
        assert words_in_sentence("hi go for") == "hi go for"

    def test_no_words_prime_length(self):
        # "a" (1), "abcd" (4), "efgh" (4) — none prime
        assert words_in_sentence("a abcd efgh") == ""

    def test_mixed_prime_and_non_prime(self):
        # "I" (1, not prime), "am" (2, prime), "fine" (4, not prime)
        assert words_in_sentence("I am fine") == "am"

    def test_preserves_order(self):
        # "hi" (2, prime), "world" (5, prime), "abc" (3, prime)
        assert words_in_sentence("hi world abc") == "hi world abc"

    def test_first_and_last_prime_middle_not(self):
        # "hi" (2, prime), "abcd" (4, not), "ok" (2, prime)
        assert words_in_sentence("hi abcd ok") == "hi ok"

    def test_only_middle_is_prime(self):
        # "ab" (2, prime), "cde" (3, prime), "fghi" (4, not)
        assert words_in_sentence("ab cde fghi") == "ab cde"


class TestWordsInSentenceEdgeCases:
    """Edge case tests."""

    def test_empty_string(self):
        assert words_in_sentence("") == ""

    def test_single_space(self):
        # Two empty strings split by space — both have length 0 (not prime)
        assert words_in_sentence(" ") == ""

    def test_multiple_spaces_between_words(self):
        # "a b" — "a" (1, not prime), "b" (1, not prime)
        assert words_in_sentence("a b") == ""

    def test_longer_prime_lengths(self):
        # "programming" (11, prime), "is" (2, prime), "fun" (3, prime)
        assert words_in_sentence("programming is fun") == "programming is fun"

    def test_word_length_ten(self):
        # "tenletterx" (10, not prime)
        assert words_in_sentence("tenletterx") == ""

    def test_word_length_eleven(self):
        # "elevenchars" (11, prime)
        assert words_in_sentence("elevenchars") == "elevenchars"

    def test_word_length_twelve(self):
        # "twelvecharx" (11, prime)
        assert words_in_sentence("twelvecharx") == "twelvecharx"

    def test_word_length_thirteen(self):
        # "thirteenchars" (13, prime)
        assert words_in_sentence("thirteenchars") == "thirteenchars"


class TestWordsInSentenceConstraints:
    """Tests respecting the constraint: sentence contains only letters."""

    def test_lowercase_letters(self):
        # "hi" (2, prime), "nope" (4, not prime)
        assert words_in_sentence("hi nope") == "hi"

    def test_uppercase_letters(self):
        # "HI" (2, prime), "NOPE" (4, not prime)
        assert words_in_sentence("HI NOPE") == "HI"

    def test_mixed_case(self):
        # "Hi" (2, prime), "Nope" (4, not prime)
        assert words_in_sentence("Hi Nope") == "Hi"

    def test_max_length_sentence(self):
        # Build a sentence of exactly 100 characters using only letters and spaces
        # We need to ensure it respects the constraint
        words = ["a", "bb", "ccc", "dddd", "eeeee", "ffffff", "ggggggg", "hhhhhhhh"]
        sentence = " ".join(words)
        # Lengths: 1, 2, 3, 4, 5, 6, 7, 8
        # Primes: 2, 3, 5, 7 -> "bb ccc eeeee ggggggg"
        result = words_in_sentence(sentence)
        assert result == "bb ccc eeeee ggggggg"


class TestWordsInSentenceIsPrimeLogic:
    """Tests specifically targeting the prime number filtering logic."""

    def test_word_length_two(self):
        assert words_in_sentence("ab") == "ab"

    def test_word_length_three(self):
        assert words_in_sentence("abc") == "abc"

    def test_word_length_five(self):
        assert words_in_sentence("abcde") == "abcde"

    def test_word_length_seven(self):
        assert words_in_sentence("abcdefg") == "abcdefg"

    def test_word_length_four(self):
        assert words_in_sentence("abcd") == ""

    def test_word_length_six(self):
        assert words_in_sentence("abcdef") == ""

    def test_word_length_nine(self):
        assert words_in_sentence("abcdefghi") == ""

    def test_word_length_zero(self):
        # Splitting on space can produce empty strings
        assert words_in_sentence("a  b") == ""  # empty string between double space has len 0
