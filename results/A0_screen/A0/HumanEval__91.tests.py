import pytest
from solution import is_bored


class TestIsBored:
    """Tests for the is_bored function."""

    def test_no_sentences(self):
        assert is_bored("Hello world") == 0

    def test_single_sentence_starting_with_i(self):
        assert is_bored("I love this weather") == 1

    def test_single_sentence_not_starting_with_i(self):
        assert is_bored("The sky is blue") == 0

    def test_multiple_sentences_one_boredom(self):
        assert is_bored("The sky is blue. The sun is shining. I love this weather") == 1

    def test_multiple_sentences_no_boredoms(self):
        assert is_bored("The sky is blue. The sun is shining.") == 0

    def test_multiple_sentences_multiple_boredoms(self):
        assert is_bored("I am happy. You are sad. I am tired.") == 2

    def test_sentences_delimited_by_question_mark(self):
        assert is_bored("How are you? I am fine? What about you?") == 1

    def test_sentences_delimited_by_exclamation(self):
        assert is_bored("Wow! I can believe it! Great day!") == 1

    def test_mixed_delimiters(self):
        assert is_bored("Hi! How are you? I am great. Bye!") == 1

    def test_empty_string(self):
        assert is_bored("") == 0

    def test_only_whitespace(self):
        assert is_bored("   ") == 0

    def test_i_at_end_of_sentence(self):
        assert is_bored("Who is there? I am here.") == 1

    def test_i_as_part_of_word(self):
        assert is_bored("Inside the house. It is raining.") == 0

    def test_consecutive_delimiters(self):
        assert is_bored("I am here.. I am there.") == 2

    def test_sentence_with_leading_spaces_after_split(self):
        assert is_bored("First sentence. I am second.") == 1

    def test_all_boredoms(self):
        assert is_bored("I like apples. I like bananas. I like oranges.") == 3

    def test_no_boredoms_mixed(self):
        assert is_bored("We went home. They played games. She sang songs.") == 0

    def test_single_period(self):
        assert is_bored(".") == 0

    def test_i_without_space_after(self):
        assert is_bored("Ice cream is good. I like it.") == 1
