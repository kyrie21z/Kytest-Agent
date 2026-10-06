import pytest
from solution import histogram


class TestHistogram:
    """Tests for the histogram function."""

    def test_empty_string(self):
        """Empty input should return an empty dictionary."""
        assert histogram("") == {}

    def test_all_unique_letters(self):
        """When all letters appear once, all should be returned."""
        assert histogram("a b c") == {"a": 1, "b": 1, "c": 1}

    def test_single_letter(self):
        """A single letter should return it with count 1."""
        assert histogram("a") == {"a": 1}

    def test_one_dominant_letter(self):
        """When one letter appears more often, only it should be returned."""
        assert histogram("b b b b a") == {"b": 4}

    def test_two_tied_letters(self):
        """When two letters tie for most frequent, both should be returned."""
        assert histogram("a b b a") == {"a": 2, "b": 2}

    def test_multiple_tied_letters(self):
        """When multiple letters tie, all tied ones should be returned."""
        assert histogram("a b c a b") == {"a": 2, "b": 2}

    def test_three_tied_letters(self):
        """Three letters can also tie for most frequent."""
        assert histogram("x y z x y z") == {"x": 2, "y": 2, "z": 2}

    def test_most_frequent_with_others_present(self):
        """Only the most frequent letter(s) should be in the result."""
        assert histogram("a a a b c") == {"a": 3}

    def test_all_same_letter(self):
        """All same letters should return that letter with total count."""
        assert histogram("d d d d") == {"d": 4}

    def test_complex_case(self):
        """A more complex case with varying frequencies."""
        assert histogram("a a b b b c c d") == {"b": 3}

    def test_complex_case_with_tie(self):
        """Complex case where two letters tie for most frequent."""
        assert histogram("a a a b b b c d d") == {"a": 3, "b": 3}

    def test_double_spaces_between_words(self):
        """Double spaces should not cause issues (split handles them)."""
        # split(" ") with double spaces produces empty strings which are skipped
        assert histogram("a  b  c") == {"a": 1, "b": 1, "c": 1}

    def test_leading_trailing_spaces(self):
        """Leading and trailing spaces should be handled gracefully."""
        assert histogram(" a b c ") == {"a": 1, "b": 1, "c": 1}

    def test_many_occurrences(self):
        """Test with many occurrences of a single letter."""
        assert histogram("x x x x x x x x x x") == {"x": 10}

    def test_four_way_tie(self):
        """Four letters can tie for most frequent."""
        assert histogram("p q r s p q r s") == {"p": 2, "q": 2, "r": 2, "s": 2}

    def test_result_is_dict(self):
        """Return value should always be a dictionary."""
        assert isinstance(histogram(""), dict)
        assert isinstance(histogram("a"), dict)
        assert isinstance(histogram("a b c"), dict)

    def test_values_are_integers(self):
        """All values in the result dictionary should be integers."""
        result = histogram("a a b b c")
        assert all(isinstance(v, int) for v in result.values())

    def test_keys_are_strings(self):
        """All keys in the result dictionary should be strings."""
        result = histogram("a a b b c")
        assert all(isinstance(k, str) for k in result.keys())

    def test_no_extra_keys(self):
        """Result should only contain the most frequent letter(s)."""
        result = histogram("a a a b c c")
        assert len(result) == 1
        assert result == {"a": 3}

    def test_preserves_order_of_insertion_py37plus(self):
        """In Python 3.7+, dict preserves insertion order; check keys match expected."""
        result = histogram("a b c")
        assert set(result.keys()) == {"a", "b", "c"}

    def test_large_input(self):
        """Test with a large number of letters."""
        letters = " ".join(["m"] * 100 + ["n"] * 99 + ["o"] * 50)
        assert histogram(letters) == {"m": 100}

    def test_alternating_pattern(self):
        """Alternating pattern where two letters alternate equally."""
        assert histogram("x y x y x y") == {"x": 3, "y": 3}
