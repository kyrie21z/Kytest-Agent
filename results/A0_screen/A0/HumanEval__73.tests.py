import pytest
from solution import smallest_change


class TestSmallestChange:
    """Tests for the smallest_change function."""

    def test_already_palindrome(self):
        """Array is already a palindrome — zero changes needed."""
        assert smallest_change([1, 2, 3, 2, 1]) == 0

    def test_single_element(self):
        """A single-element array is trivially a palindrome."""
        assert smallest_change([42]) == 0

    def test_empty_array(self):
        """An empty array is trivially a palindrome."""
        assert smallest_change([]) == 0

    def test_two_identical_elements(self):
        """Two identical elements form a palindrome."""
        assert smallest_change([5, 5]) == 0

    def test_two_different_elements(self):
        """Two different elements require one change."""
        assert smallest_change([1, 2]) == 1

    def test_example_1(self):
        """Example from docstring: [1,2,3,5,4,7,9,6] -> 4."""
        assert smallest_change([1, 2, 3, 5, 4, 7, 9, 6]) == 4

    def test_example_2(self):
        """Example from docstring: [1, 2, 3, 4, 3, 2, 2] -> 1."""
        assert smallest_change([1, 2, 3, 4, 3, 2, 2]) == 1

    def test_all_same_elements(self):
        """All identical elements — no changes needed."""
        assert smallest_change([7, 7, 7, 7, 7]) == 0

    def test_one_mismatch_in_odd_length(self):
        """Odd-length array with one mismatched pair."""
        assert smallest_change([1, 2, 3, 2, 1]) == 0

    def test_one_mismatch_in_even_length(self):
        """Even-length array with one mismatched pair."""
        assert smallest_change([1, 2, 3, 4]) == 2

    def test_negative_numbers(self):
        """Arrays containing negative numbers."""
        assert smallest_change([-1, -2, -1]) == 0

    def test_negative_and_positive_mix(self):
        """Mix of negative and positive numbers."""
        assert smallest_change([-1, 2, -1]) == 0

    def test_large_values(self):
        """Arrays with large integer values."""
        assert smallest_change([10**9, 10**9]) == 0

    def test_alternating_pattern(self):
        """Alternating pattern requiring many changes."""
        assert smallest_change([1, 2, 1, 2, 1]) == 0

    def test_requires_half_changes(self):
        """Every pair differs — needs len(arr)//2 changes."""
        assert smallest_change([1, 2, 3, 4, 5, 6]) == 3

    def test_three_elements_one_change(self):
        """Three elements where middle differs from outer pairs."""
        assert smallest_change([1, 5, 2]) == 1

    def test_four_elements_two_changes(self):
        """Four elements where all pairs differ."""
        assert smallest_change([1, 2, 3, 4]) == 2

    def test_five_elements_one_change(self):
        """Five elements with only center differing."""
        assert smallest_change([1, 2, 5, 2, 1]) == 0

    def test_center_element_doesnt_matter(self):
        """Center element in odd-length arrays doesn't affect count."""
        assert smallest_change([1, 2, 999, 2, 1]) == 0

    def test_all_pairs_differ(self):
        """Every symmetric pair differs."""
        assert smallest_change([1, 2, 3, 4, 5, 6, 7]) == 3

    def test_docstring_examples_preserved(self):
        """Ensure all examples from the docstring still pass."""
        assert smallest_change([1, 2, 3, 5, 4, 7, 9, 6]) == 4
        assert smallest_change([1, 2, 3, 4, 3, 2, 2]) == 1
        assert smallest_change([1, 2, 3, 2, 1]) == 0
