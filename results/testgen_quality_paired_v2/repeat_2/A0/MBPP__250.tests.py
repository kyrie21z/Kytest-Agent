import pytest
from solution import count_X


class TestCountXBasic:
    """Tests for basic counting scenarios."""

    def test_single_occurrence(self):
        """Element appears exactly once."""
        assert count_X((1, 2, 3), 2) == 1

    def test_multiple_occurrences(self):
        """Element appears more than once."""
        assert count_X((1, 2, 2, 3, 2), 2) == 3

    def test_no_occurrence(self):
        """Element does not appear in the tuple."""
        assert count_X((1, 2, 3), 4) == 0

    def test_empty_tuple(self):
        """Empty tuple should always return 0."""
        assert count_X((), 1) == 0


class TestCountXEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_single_element_tuple_matching(self):
        """Single-element tuple where element matches."""
        assert count_X((5,), 5) == 1

    def test_single_element_tuple_not_matching(self):
        """Single-element tuple where element does not match."""
        assert count_X((5,), 3) == 0

    def test_all_elements_match(self):
        """All elements in the tuple are the target."""
        assert count_X((7, 7, 7, 7), 7) == 4

    def test_first_and_last_match(self):
        """Target element is at both ends of the tuple."""
        assert count_X((1, 2, 3, 1), 1) == 2

    def test_consecutive_duplicates(self):
        """Target element appears consecutively."""
        assert count_X(('a', 'a', 'b', 'a', 'a'), 'a') == 4


class TestCountXTypes:
    """Tests with different data types."""

    def test_string_elements(self):
        """Tuple containing strings."""
        assert count_X(('hello', 'world', 'hello', 'hello'), 'hello') == 3

    def test_negative_numbers(self):
        """Tuple containing negative numbers."""
        assert count_X((-1, -2, -1, 3, -1), -1) == 3

    def test_float_elements(self):
        """Tuple containing floats."""
        assert count_X((1.5, 2.5, 1.5, 3.5), 1.5) == 2

    def test_mixed_types(self):
        """Tuple containing mixed types."""
        assert count_X((1, 'a', 2, 'a', 3), 'a') == 2

    def test_none_value(self):
        """Tuple containing None values."""
        assert count_X((None, 1, None, 2), None) == 2

    def test_boolean_values(self):
        """Tuple containing boolean values."""
        assert count_X((True, False, True, True), True) == 3


class TestCountXLargeInput:
    """Tests with larger inputs."""

    def test_large_tuple(self):
        """Large tuple with many occurrences."""
        tup = (42,) * 1000
        assert count_X(tup, 42) == 1000

    def test_large_tuple_no_match(self):
        """Large tuple where element doesn't exist."""
        tup = list(range(1000))
        assert count_X(tuple(tup), 9999) == 0
