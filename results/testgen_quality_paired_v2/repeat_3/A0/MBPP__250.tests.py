import pytest
from solution import count_X


class TestCountX:
    """Tests for the count_X function."""

    # --- Basic functionality ---

    def test_single_occurrence(self):
        assert count_X((1, 2, 3), 2) == 1

    def test_multiple_occurrences(self):
        assert count_X((1, 2, 2, 3, 2), 2) == 3

    def test_zero_occurrences(self):
        assert count_X((1, 2, 3), 4) == 0

    def test_empty_tuple(self):
        assert count_X((), 1) == 0

    def test_all_same_elements(self):
        assert count_X((5, 5, 5, 5), 5) == 4

    def test_all_same_elements_not_found(self):
        assert count_X((5, 5, 5, 5), 3) == 0

    # --- Edge cases ---

    def test_single_element_tuple_found(self):
        assert count_X((42,), 42) == 1

    def test_single_element_tuple_not_found(self):
        assert count_X((42,), 99) == 0

    def test_count_first_element(self):
        assert count_X((1, 2, 3), 1) == 1

    def test_count_last_element(self):
        assert count_X((1, 2, 3), 3) == 1

    def test_count_consecutive_duplicates(self):
        assert count_X((1, 1, 1, 2, 2), 1) == 3

    # --- Different data types ---

    def test_string_elements(self):
        assert count_X(("a", "b", "a", "c"), "a") == 2

    def test_mixed_types(self):
        assert count_X((1, "a", 1, 2), 1) == 2

    def test_float_elements(self):
        assert count_X((1.5, 2.5, 1.5, 3.5), 1.5) == 2

    def test_none_element(self):
        assert count_X((None, 1, None), None) == 2

    def test_boolean_elements(self):
        assert count_X((True, False, True, True), True) == 3

    # --- Negative / zero values ---

    def test_negative_numbers(self):
        assert count_X((-1, -2, -1, -3), -1) == 2

    def test_zero_value(self):
        assert count_X((0, 1, 0, 2), 0) == 2

    # --- Return type check ---

    def test_returns_integer(self):
        assert isinstance(count_X((1, 2, 3), 2), int)
