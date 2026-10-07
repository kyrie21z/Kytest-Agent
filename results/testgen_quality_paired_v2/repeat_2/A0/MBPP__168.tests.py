import pytest
from solution import frequency


class TestFrequency:
    """Unit tests for the frequency function."""

    # --- Basic positive cases ---

    def test_single_occurrence(self):
        """Count when the target appears exactly once."""
        assert frequency([1, 2, 3], 2) == 1

    def test_multiple_occurrences(self):
        """Count when the target appears multiple times."""
        assert frequency([1, 2, 2, 3, 2], 2) == 3

    def test_all_elements_match(self):
        """Count when every element matches the target."""
        assert frequency([5, 5, 5, 5], 5) == 4

    def test_target_not_present(self):
        """Count is zero when the target does not appear."""
        assert frequency([1, 2, 3], 4) == 0

    # --- Edge cases with empty / single-element lists ---

    def test_empty_list(self):
        """Empty list should always return 0."""
        assert frequency([], 1) == 0

    def test_single_element_no_match(self):
        """Single-element list where element != target."""
        assert frequency([7], 3) == 0

    def test_single_element_match(self):
        """Single-element list where element == target."""
        assert frequency([7], 7) == 1

    # --- Different data types ---

    def test_string_list(self):
        """Count occurrences of a string in a list of strings."""
        assert frequency(["apple", "banana", "apple"], "apple") == 2

    def test_float_list(self):
        """Count occurrences of a float in a list of floats."""
        assert frequency([1.5, 2.5, 1.5, 3.5], 1.5) == 2

    def test_negative_numbers(self):
        """Count with negative numbers."""
        assert frequency([-1, -2, -1, -3], -1) == 2

    def test_mixed_positive_negative(self):
        """Count with a mix of positive and negative numbers."""
        assert frequency([1, -1, 2, -1, 3], -1) == 2

    # --- Large inputs ---

    def test_large_list(self):
        """Count in a large list to ensure correctness at scale."""
        lst = [1] * 10_000 + [2] * 5_000
        assert frequency(lst, 1) == 10_000
        assert frequency(lst, 2) == 5_000
        assert frequency(lst, 3) == 0

    # --- Mixed-type list (Python allows this) ---

    def test_mixed_types_in_list(self):
        """List containing mixed types; count still works correctly.
        
        Note: In Python, True == 1 is True (bool is a subclass of int),
        so True will be counted as a match for 1.
        """
        lst = [1, "hello", 2, 1, True, 1]
        assert frequency(lst, 1) == 4  # three 1s + True

    # --- Boundary value tests ---

    def test_zero_as_target(self):
        """Target value is zero."""
        assert frequency([0, 1, 0, 2], 0) == 2

    def test_zero_in_list(self):
        """Zero appears in the list but target is different."""
        assert frequency([0, 0, 0], 1) == 0

    # --- Idempotency / no side-effects ---

    def test_does_not_modify_input(self):
        """Ensure the function does not mutate the input list."""
        original = [1, 2, 3, 2, 1]
        frequency(original, 2)
        assert original == [1, 2, 3, 2, 1]
