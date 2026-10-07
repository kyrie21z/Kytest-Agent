import pytest
from solution import count_X


class TestCountXBasic:
    """Tests for basic functionality of count_X."""

    def test_single_occurrence(self):
        assert count_X((1, 2, 3), 2) == 1

    def test_multiple_occurrences(self):
        assert count_X((1, 2, 2, 3, 2), 2) == 3

    def test_no_occurrence(self):
        assert count_X((1, 2, 3), 4) == 0

    def test_all_same_elements(self):
        assert count_X((5, 5, 5, 5), 5) == 4


class TestCountXEdgeCases:
    """Tests for edge cases of count_X."""

    def test_empty_tuple(self):
        assert count_X((), 1) == 0

    def test_single_element_tuple_found(self):
        assert count_X((42,), 42) == 1

    def test_single_element_tuple_not_found(self):
        assert count_X((42,), 99) == 0

    def test_counting_zero(self):
        assert count_X((0, 0, 1), 0) == 2

    def test_counting_false(self):
        assert count_X((False, True, False), False) == 2

    def test_counting_none(self):
        assert count_X((None, 1, None), None) == 2

    def test_counting_empty_string(self):
        assert count_X(("", "a", ""), "") == 2


class TestCountXTypes:
    """Tests with different data types."""

    def test_strings(self):
        assert count_X(("apple", "banana", "apple"), "apple") == 2

    def test_mixed_types(self):
        assert count_X((1, "a", 2, "b"), 1) == 1

    def test_floats(self):
        assert count_X((1.5, 2.5, 1.5, 3.5), 1.5) == 2

    def test_negative_numbers(self):
        assert count_X((-1, -2, -1, -3), -1) == 2


class TestCountXTuples:
    """Tests where the tuple itself contains tuples."""

    def test_nested_tuples(self):
        t = ((1, 2), (3, 4), (1, 2))
        assert count_X(t, (1, 2)) == 2

    def test_nested_tuple_not_present(self):
        t = ((1, 2), (3, 4), (5, 6))
        assert count_X(t, (7, 8)) == 0


class TestCountXLargeInput:
    """Tests with larger inputs."""

    def test_large_tuple(self):
        tup = (7,) * 1000
        assert count_X(tup, 7) == 1000

    def test_large_tuple_with_mixed(self):
        tup = [i % 3 for i in range(10000)]
        assert count_X(tuple(tup), 0) == 3334
        assert count_X(tuple(tup), 1) == 3333
        assert count_X(tuple(tup), 2) == 3333
