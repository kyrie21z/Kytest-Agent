"""Unit tests for solution.compare."""

import pytest
from solution import compare


class TestCompareBasic:
    """Tests for basic functionality of compare()."""

    def test_all_correct_guesses(self):
        game = [1, 2, 3, 4, 5]
        guess = [1, 2, 3, 4, 5]
        assert compare(game, guess) == [0, 0, 0, 0, 0]

    def test_all_incorrect_guesses(self):
        game = [1, 2, 3, 4, 5]
        guess = [2, 3, 4, 5, 6]
        assert compare(game, guess) == [1, 1, 1, 1, 1]

    def test_mixed_correct_and_incorrect(self):
        game = [1, 2, 3, 4, 5]
        guess = [1, 3, 3, 6, 2]
        assert compare(game, guess) == [0, 1, 0, 2, 3]

    def test_single_element_correct(self):
        assert compare([5], [5]) == [0]

    def test_single_element_incorrect(self):
        assert compare([5], [3]) == [2]


class TestCompareDocstringExamples:
    """Tests using the examples from the docstring."""

    def test_example_1(self):
        game = [1, 2, 3, 4, 5, 1]
        guess = [1, 2, 3, 4, 2, -2]
        assert compare(game, guess) == [0, 0, 0, 0, 3, 3]

    def test_example_2(self):
        game = [0, 5, 0, 0, 0, 4]
        guess = [4, 1, 1, 0, 0, -2]
        assert compare(game, guess) == [4, 4, 1, 0, 0, 6]


class TestCompareEdgeCases:
    """Tests for edge cases."""

    def test_empty_arrays(self):
        assert compare([], []) == []

    def test_negative_scores_and_guesses(self):
        game = [-3, -1, 0]
        guess = [-1, -1, -5]
        assert compare(game, guess) == [2, 0, 5]

    def test_large_values(self):
        game = [1000000, 999999]
        guess = [0, 1000000]
        assert compare(game, guess) == [1000000, 1]

    def test_zero_values(self):
        game = [0, 0, 0]
        guess = [0, 0, 0]
        assert compare(game, guess) == [0, 0, 0]

    def test_guess_larger_than_score(self):
        game = [1, 2, 3]
        guess = [10, 20, 30]
        assert compare(game, guess) == [9, 18, 27]

    def test_guess_smaller_than_score(self):
        game = [10, 20, 30]
        guess = [1, 2, 3]
        assert compare(game, guess) == [9, 18, 27]

    def test_mixed_positive_and_negative(self):
        game = [-5, 0, 5]
        guess = [5, 0, -5]
        assert compare(game, guess) == [10, 0, 10]

    def test_long_array(self):
        game = list(range(100))
        guess = list(range(100))
        assert compare(game, guess) == [0] * 100

    def test_long_array_with_differences(self):
        game = list(range(100))
        guess = [i + 1 for i in range(100)]
        result = compare(game, guess)
        assert all(r == 1 for r in result)


class TestCompareReturnTypes:
    """Tests to verify return type is a list."""

    def test_returns_list(self):
        result = compare([1, 2], [3, 4])
        assert isinstance(result, list)

    def test_returns_integers(self):
        result = compare([1, 2, 3], [4, 5, 6])
        assert all(isinstance(x, int) for x in result)

    def test_does_not_mutate_input(self):
        game = [1, 2, 3]
        guess = [4, 5, 6]
        game_copy = game[:]
        guess_copy = guess[:]
        compare(game, guess)
        assert game == game_copy
        assert guess == guess_copy
