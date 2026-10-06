"""Unit tests for solution.search() using pytest."""

from solution import search


class TestSearch:
    """Tests for the search function."""

    # --- Provided examples from docstring ---

    def test_example_1(self):
        """search([4, 1, 2, 2, 3, 1]) == 2"""
        assert search([4, 1, 2, 2, 3, 1]) == 2

    def test_example_2(self):
        """search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3"""
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

    def test_example_3(self):
        """search([5, 5, 4, 4, 4]) == -1"""
        assert search([5, 5, 4, 4, 4]) == -1

    # --- Edge cases: single element lists ---

    def test_single_element_valid(self):
        """[1] -> frequency 1 >= value 1 => return 1"""
        assert search([1]) == 1

    def test_single_element_invalid(self):
        """[2] -> frequency 1 < value 2 => return -1"""
        assert search([2]) == -1

    def test_single_element_large(self):
        """[100] -> frequency 1 < value 100 => return -1"""
        assert search([100]) == -1

    # --- Cases where no element qualifies ---

    def test_all_frequencies_too_low(self):
        """Every number appears fewer times than its value."""
        assert search([3, 3, 2]) == -1  # 3 appears 2x (<3), 2 appears 1x (<2)

    def test_zeros_only(self):
        """List with only zeros — freq(0)=3 >= 0 => return 0."""
        assert search([0, 0, 0]) == 0

    # --- Cases where multiple candidates exist ---

    def test_multiple_candidates_returns_greatest(self):
        """Return the greatest integer whose freq >= itself."""
        # 2 appears 3x (>=2), 3 appears 3x (>=3), 4 appears 1x (<4)
        assert search([2, 2, 2, 3, 3, 3]) == 3

    def test_larger_value_with_enough_frequency(self):
        """Larger number that satisfies the condition should win."""
        # 5 appears 5x (>=5), 3 appears 3x (>=3) => max = 5
        assert search([5, 5, 5, 5, 5, 3, 3, 3]) == 5

    # --- All elements are the same ---

    def test_all_same_value_valid(self):
        """[2, 2, 2] -> 2 appears 3x (>=2) => return 2"""
        assert search([2, 2, 2]) == 2

    def test_all_same_value_invalid(self):
        """[5, 5] -> 5 appears 2x (<5) => return -1"""
        assert search([5, 5]) == -1

    def test_all_same_one(self):
        """[1, 1, 1] -> 1 appears 3x (>=1) => return 1"""
        assert search([1, 1, 1]) == 1

    # --- Frequency exactly equals value ---

    def test_freq_equals_value(self):
        """Frequency exactly equal to value should qualify."""
        # 3 appears exactly 3 times
        assert search([3, 3, 3]) == 3

    # --- Mixed valid and invalid ---

    def test_mixed_valid_invalid(self):
        """Some numbers qualify, some don't; pick the greatest valid."""
        # 1 appears 1x (>=1), 2 appears 1x (<2), 3 appears 2x (<3)
        assert search([1, 2, 3, 3]) == 1

    def test_only_smallest_qualifies(self):
        """Only 1 qualifies because it needs freq >= 1."""
        assert search([1, 100, 200]) == 1

    # --- Large repeated values ---

    def test_large_repeated_value(self):
        """A large number repeated enough times."""
        # 10 appears 10 times => 10 >= 10 => valid
        lst = [10] * 10
        assert search(lst) == 10

    def test_two_digit_number_qualifies(self):
        """12 appears 12 times => valid."""
        lst = [12] * 12
        assert search(lst) == 12

    def test_almost_qualifies_but_not(self):
        """12 appears 11 times => 11 < 12 => invalid."""
        lst = [12] * 11 + [1]
        assert search(lst) == 1  # only 1 qualifies

    # --- Boundary: value 1 always qualifies if present ---

    def test_one_present_always_returns_at_least_one(self):
        """If 1 is in the list, it always qualifies (freq >= 1)."""
        assert search([1, 999999]) == 1

    def test_one_with_other_valid(self):
        """1 and 2 both qualify; return 2."""
        assert search([1, 2, 2]) == 2

    # --- Performance / stress test ---

    def test_many_elements(self):
        """Stress test with many elements."""
        lst = list(range(1, 101)) * 10  # each number 1..100 appears 10 times
        # For n in 1..10: freq=10 >= n => valid. For n in 11..100: freq=10 < n => invalid.
        assert search(lst) == 10

    def test_max_valid_is_ten(self):
        """Verify that 10 is the max valid when each of 1..100 appears 10 times."""
        lst = list(range(1, 101)) * 10
        assert search(lst) == 10

    def test_repeated_small_number(self):
        """1 appears 100 times => valid."""
        assert search([1] * 100) == 1
