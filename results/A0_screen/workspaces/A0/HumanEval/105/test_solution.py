import pytest
from solution import by_length


class TestByLength:
    """Tests for the by_length function."""

    # --- Basic / Happy-path tests ---

    def test_example_from_docstring(self):
        arr = [2, 1, 1, 4, 5, 8, 2, 3]
        expected = ["Eight", "Five", "Four", "Three", "Two", "Two", "One", "One"]
        assert by_length(arr) == expected

    def test_empty_array(self):
        assert by_length([]) == []

    def test_single_element_valid(self):
        assert by_length([5]) == ["Five"]

    def test_all_same_elements(self):
        assert by_length([3, 3, 3]) == ["Three", "Three", "Three"]

    def test_already_sorted_ascending(self):
        arr = [1, 2, 3, 4, 5]
        expected = ["Five", "Four", "Three", "Two", "One"]
        assert by_length(arr) == expected

    def test_reverse_sorted(self):
        arr = [9, 8, 7, 6, 5]
        expected = ["Nine", "Eight", "Seven", "Six", "Five"]
        assert by_length(arr) == expected

    def test_random_order(self):
        arr = [7, 3, 9, 1, 5]
        expected = ["Nine", "Seven", "Five", "Three", "One"]
        assert by_length(arr) == expected

    # --- Filtering tests ---

    def test_no_valid_numbers(self):
        arr = [0, -1, 10, 100, -5]
        assert by_length(arr) == []

    def test_mixed_valid_and_invalid(self):
        arr = [1, -1, 55, 0, 10, 3]
        expected = ["Three", "One"]
        assert by_length(arr) == expected

    def test_boundary_zero_excluded(self):
        assert by_length([0]) == []

    def test_boundary_nine_included(self):
        assert by_length([9]) == ["Nine"]

    def test_boundary_ten_excluded(self):
        assert by_length([10]) == []

    def test_negative_numbers_excluded(self):
        assert by_length([-5, -1, -100]) == []

    def test_large_positive_numbers_excluded(self):
        assert by_length([100, 999, 10000]) == []

    def test_duplicates_filtered_correctly(self):
        arr = [2, 2, 2, 1, 1]
        expected = ["Two", "Two", "Two", "One", "One"]
        assert by_length(arr) == expected

    # --- Edge cases ---

    def test_all_nines(self):
        assert by_length([9, 9, 9]) == ["Nine", "Nine", "Nine"]

    def test_all_ones(self):
        assert by_length([1, 1, 1]) == ["One", "One", "One"]

    def test_alternating_values(self):
        arr = [1, 9, 1, 9, 1]
        expected = ["Nine", "Nine", "One", "One", "One"]
        assert by_length(arr) == expected

    def test_numbers_1_through_9_each_once(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = ["Nine", "Eight", "Seven", "Six", "Five", "Four", "Three", "Two", "One"]
        assert by_length(arr) == expected

    def test_numbers_9_through_1_each_once(self):
        arr = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        expected = ["Nine", "Eight", "Seven", "Six", "Five", "Four", "Three", "Two", "One"]
        assert by_length(arr) == expected

    def test_preserves_duplicate_count(self):
        arr = [5, 5, 5, 5]
        expected = ["Five", "Five", "Five", "Five"]
        assert by_length(arr) == expected

    def test_mixed_with_zeros(self):
        arr = [0, 1, 0, 2, 0, 3]
        expected = ["Three", "Two", "One"]
        assert by_length(arr) == expected

    def test_only_invalid_numbers(self):
        arr = [-100, 0, 10, 50, 1000]
        assert by_length(arr) == []

    def test_result_is_list_of_strings(self):
        arr = [1, 2, 3]
        result = by_length(arr)
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)

    def test_word_spelling_correctness(self):
        """Verify every valid digit maps to the correct spelled-out name."""
        mapping = {
            1: "One",
            2: "Two",
            3: "Three",
            4: "Four",
            5: "Five",
            6: "Six",
            7: "Seven",
            8: "Eight",
            9: "Nine",
        }
        for num, expected_word in mapping.items():
            assert by_length([num]) == [expected_word]
