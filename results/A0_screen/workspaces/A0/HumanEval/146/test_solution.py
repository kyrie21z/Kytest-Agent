import pytest
from solution import specialFilter


class TestSpecialFilter:
    """Tests for the specialFilter function."""

    def test_example_from_docstring_1(self):
        """Test case from docstring: [15, -73, 14, -15] => 1"""
        assert specialFilter([15, -73, 14, -15]) == 1

    def test_example_from_docstring_2(self):
        """Test case from docstring: [33, -2, -3, 45, 21, 109] => 2"""
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2

    def test_empty_list(self):
        """Empty input should return 0."""
        assert specialFilter([]) == 0

    def test_all_elements_match(self):
        """All elements satisfy the conditions."""
        # 11, 13, 31, 33 all have first and last digit odd and > 10
        assert specialFilter([11, 13, 31, 33]) == 4

    def test_no_elements_match(self):
        """No element satisfies the conditions."""
        assert specialFilter([1, 2, 3, 4, 5]) == 0

    def test_negative_numbers_excluded(self):
        """Negative numbers are excluded because they are not > 10."""
        assert specialFilter([-11, -13, -31, -33]) == 0

    def test_single_digit_numbers_excluded(self):
        """Single digit numbers are <= 10, so excluded."""
        assert specialFilter([1, 3, 5, 7, 9]) == 0

    def test_first_digit_even(self):
        """Numbers with even first digit should not match."""
        # 21: first digit 2 (even), last digit 1 (odd) -> no match
        # 45: first digit 4 (even), last digit 5 (odd) -> no match
        assert specialFilter([21, 45]) == 0

    def test_last_digit_even(self):
        """Numbers with even last digit should not match."""
        # 12: first digit 1 (odd), last digit 2 (even) -> no match
        # 34: first digit 3 (odd), last digit 4 (even) -> no match
        assert specialFilter([12, 34]) == 0

    def test_boundary_value_10(self):
        """Number exactly 10 should not match (not > 10)."""
        assert specialFilter([10]) == 0

    def test_boundary_value_11(self):
        """Number 11 should match (first=1 odd, last=1 odd, > 10)."""
        assert specialFilter([11]) == 1

    def test_mixed_positive_and_negative(self):
        """Mix of positive and negative numbers."""
        # 15 matches (>10, first=1 odd, last=5 odd)
        # -73 doesn't match (<=10 false)
        # 14 doesn't match (last=4 even)
        # -15 doesn't match (<=10 false)
        assert specialFilter([15, -73, 14, -15]) == 1

    def test_large_numbers(self):
        """Large numbers with odd first and last digits."""
        # 1991: first=1 odd, last=1 odd, >10 -> match
        # 9999: first=9 odd, last=9 odd, >10 -> match
        # 2002: first=2 even -> no match
        assert specialFilter([1991, 9999, 2002]) == 2

    def test_duplicate_values(self):
        """Duplicates should each be counted."""
        assert specialFilter([11, 11, 11]) == 3

    def test_only_non_matching_positive(self):
        """Positive numbers but none satisfy both digit conditions."""
        # 10: not > 10
        # 12: last digit even
        # 21: first digit even
        # 22: first and last even
        assert specialFilter([10, 12, 21, 22]) == 0

    def test_three_digit_numbers(self):
        """Three-digit numbers with odd first and last digits."""
        # 101: first=1 odd, last=1 odd, >10 -> match
        # 100: last=0 even -> no match
        # 201: first=2 even -> no match
        assert specialFilter([101, 100, 201]) == 1
