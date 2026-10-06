import pytest
from solution import triples_sum_to_zero


class TestTriplesSumToZero:
    """Tests for the triples_sum_to_zero function."""

    # --- Doctest examples from the docstring ---

    def test_doctest_example_1(self):
        """Example 1: no triple sums to zero."""
        assert triples_sum_to_zero([1, 3, 5, 0]) is False

    def test_doctest_example_2(self):
        """Example 2: [1, -2, 1] sums to zero."""
        assert triples_sum_to_zero([1, 3, -2, 1]) is True

    def test_doctest_example_3(self):
        """Example 3: no triple sums to zero."""
        assert triples_sum_to_zero([1, 2, 3, 7]) is False

    def test_doctest_example_4(self):
        """Example 4: [4, -5, 3] sums to zero."""
        assert triples_sum_to_zero([2, 4, -5, 3, 9, 7]) is True

    def test_doctest_example_5(self):
        """Example 5: single element cannot form a triple."""
        assert triples_sum_to_zero([1]) is False

    # --- Edge cases ---

    def test_empty_list(self):
        """An empty list has no triples."""
        assert triples_sum_to_zero([]) is False

    def test_two_elements(self):
        """Two elements cannot form a triple."""
        assert triples_sum_to_zero([1, -1]) is False

    def test_three_elements_sum_to_zero(self):
        """Exactly three elements that sum to zero."""
        assert triples_sum_to_zero([1, -1, 0]) is True

    def test_three_elements_no_zero_sum(self):
        """Exactly three elements that do not sum to zero."""
        assert triples_sum_to_zero([1, 2, 3]) is False

    # --- Cases with zeros ---

    def test_triple_of_zeros(self):
        """Three zeros sum to zero."""
        assert triples_sum_to_zero([0, 0, 0]) is True

    def test_zero_with_pair(self):
        """A zero paired with x and -x sums to zero."""
        assert triples_sum_to_zero([0, 5, -5]) is True

    def test_zero_in_middle(self):
        """Zero as one of three elements."""
        assert triples_sum_to_zero([-3, 0, 3]) is True

    # --- All positive / all negative ---

    def test_all_positive(self):
        """No triple of all-positive numbers can sum to zero."""
        assert triples_sum_to_zero([1, 2, 3, 4, 5]) is False

    def test_all_negative(self):
        """No triple of all-negative numbers can sum to zero."""
        assert triples_sum_to_zero([-1, -2, -3, -4, -5]) is False

    # --- Duplicates ---

    def test_duplicate_values(self):
        """Duplicates should still work based on distinct indices."""
        assert triples_sum_to_zero([1, 1, -2]) is True

    def test_many_duplicates_with_solution(self):
        """List with many duplicate values where a valid triple exists."""
        assert triples_sum_to_zero([2, 2, -4, 10]) is True

    def test_many_duplicates_no_solution(self):
        """List with many duplicates but no valid triple exists."""
        # Possible sums: 2+2+2=6, 2+2+(-6)=-2 → neither is zero
        assert triples_sum_to_zero([2, 2, 2, -6]) is False

    def test_no_valid_triple_with_duplicates(self):
        """Duplicates but no valid triple exists."""
        assert triples_sum_to_zero([1, 1, 1, 1]) is False

    # --- Larger lists ---

    def test_larger_list_with_solution(self):
        """Larger list containing a valid triple."""
        assert triples_sum_to_zero([10, -10, 5, 20, -15]) is True

    def test_larger_list_without_solution(self):
        """Larger list without any valid triple."""
        assert triples_sum_to_zero([1, 2, 3, 4, 5, 6, 7]) is False

    # --- Specific value combinations ---

    def test_negative_and_positive_pair(self):
        """Classic x + y + (-x-y) = 0 pattern."""
        assert triples_sum_to_zero([3, -5, 2]) is True

    def test_large_numbers(self):
        """Works with large integer values."""
        assert triples_sum_to_zero([1000000, -1000000, 0]) is True

    def test_mixed_signs_no_triple(self):
        """Mixed signs but no triple sums to zero."""
        assert triples_sum_to_zero([1, -2, 4, -8]) is False

    def test_exact_half_triplet(self):
        """[a, a, -2a] pattern."""
        assert triples_sum_to_zero([5, 5, -10]) is True

    # --- Boundary: exactly enough elements ---

    def test_four_elements_one_triple(self):
        """Four elements where only one triple works."""
        assert triples_sum_to_zero([1, 2, -3, 100]) is True

    def test_five_elements_no_triple(self):
        """Five elements with no valid triple."""
        assert triples_sum_to_zero([1, 2, 3, 4, 5]) is False
