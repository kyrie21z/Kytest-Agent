import pytest
from solution import sort_numbers


class TestSortNumbers:
    """Tests for the sort_numbers function."""

    def test_basic_sort(self):
        """Test basic unsorted input."""
        assert sort_numbers('three one five') == 'one three five'

    def test_empty_string(self):
        """Test empty string input."""
        assert sort_numbers('') == ''

    def test_single_number(self):
        """Test input with only one number word."""
        assert sort_numbers('seven') == 'seven'

    def test_already_sorted(self):
        """Test input that is already sorted."""
        assert sort_numbers('zero one two three four five six seven eight nine') == \
            'zero one two three four five six seven eight nine'

    def test_reverse_sorted(self):
        """Test input sorted in reverse order."""
        assert sort_numbers('nine eight seven six five four three two one zero') == \
            'zero one two three four five six seven eight nine'

    def test_duplicate_numbers(self):
        """Test input with duplicate number words."""
        assert sort_numbers('five three five one three') == 'one three three five five'

    def test_all_zeros(self):
        """Test input with all the same number."""
        assert sort_numbers('zero zero zero') == 'zero zero zero'

    def test_two_numbers(self):
        """Test input with exactly two numbers."""
        assert sort_numbers('nine zero') == 'zero nine'
        assert sort_numbers('zero nine') == 'zero nine'

    def test_adjacent_numbers(self):
        """Test sorting adjacent number words."""
        assert sort_numbers('two one') == 'one two'
        assert sort_numbers('eight nine') == 'eight nine'

    def test_mixed_order(self):
        """Test various mixed-order inputs."""
        assert sort_numbers('four two six zero') == 'zero two four six'
        assert sort_numbers('seven three one') == 'one three seven'

    def test_docstring_example(self):
        """Verify the doctest example from the docstring."""
        assert sort_numbers('three one five') == 'one three five'
