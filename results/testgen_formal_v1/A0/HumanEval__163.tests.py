import pytest
from solution import generate_integers


class TestGenerateIntegers:
    """Tests for the generate_integers function."""

    # --- Basic functionality ---

    def test_basic_range(self):
        """Even digits between 2 and 8."""
        assert generate_integers(2, 8) == [2, 4, 6, 8]

    def test_reversed_order(self):
        """When a > b, the arguments should be swapped."""
        assert generate_integers(8, 2) == [2, 4, 6, 8]

    def test_no_even_digits_in_range(self):
        """Range 10-14 contains no single-digit even numbers."""
        assert generate_integers(10, 14) == []

    def test_single_number_range(self):
        """When a == b, check if that number is an even digit."""
        assert generate_integers(4, 4) == [4]
        assert generate_integers(3, 3) == []

    # --- Edge cases at boundaries ---

    def test_start_at_zero(self):
        """Zero is an even digit."""
        assert generate_integers(0, 5) == [0, 2, 4]

    def test_end_at_nine(self):
        """Upper bound of 9 should include all even digits up to 8."""
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_full_single_digit_range(self):
        """Range covering all single digits."""
        assert generate_integers(0, 9) == [0, 2, 4, 6, 8]

    def test_range_exceeds_single_digits(self):
        """Numbers >= 10 are excluded; only single-digit evens returned."""
        assert generate_integers(1, 100) == [2, 4, 6, 8]

    def test_large_range(self):
        """Large ranges still only return single-digit even numbers."""
        assert generate_integers(0, 10000) == [0, 2, 4, 6, 8]

    # --- Specific boundary values ---

    def test_start_at_one(self):
        """Starting from 1 excludes 0."""
        assert generate_integers(1, 8) == [2, 4, 6, 8]

    def test_start_at_two(self):
        """Starting from 2 includes 2."""
        assert generate_integers(2, 2) == [2]

    def test_start_at_three(self):
        """Starting from 3 excludes 2."""
        assert generate_integers(3, 8) == [4, 6, 8]

    def test_start_at_five(self):
        """Starting from 5 excludes 2 and 4."""
        assert generate_integers(5, 8) == [6, 8]

    def test_start_at_seven(self):
        """Starting from 7 excludes 2, 4, 6."""
        assert generate_integers(7, 8) == [8]

    def test_start_at_eight(self):
        """Starting from 8 includes only 8."""
        assert generate_integers(8, 8) == [8]

    def test_start_at_nine(self):
        """Starting from 9 has no even digits."""
        assert generate_integers(9, 9) == []

    # --- Negative / zero handling (actual behavior) ---

    def test_negative_a(self):
        """Negative start value: range includes negative even numbers too."""
        # range(-5, 6) with i % 2 == 0 => [-4, -2, 0, 2, 4]
        assert generate_integers(-5, 5) == [-4, -2, 0, 2, 4]

    def test_both_negative(self):
        """Both negative: after swap, range stays negative, no positives included."""
        # range(-8, -1) with i % 2 == 0 => [-8, -6, -4, -2]
        assert generate_integers(-8, -2) == [-8, -6, -4, -2]

    def test_mixed_negative_positive(self):
        """One negative, one positive: covers negatives through positive end."""
        # range(-10, 7) with i % 2 == 0 => [-10, -8, -6, -4, -2, 0, 2, 4, 6]
        assert generate_integers(-10, 6) == [-10, -8, -6, -4, -2, 0, 2, 4, 6]

    # --- Return type checks ---

    def test_returns_list(self):
        """Ensure the result is a list."""
        result = generate_integers(2, 8)
        assert isinstance(result, list)

    def test_empty_result_is_list(self):
        """Empty results should still be lists."""
        result = generate_integers(10, 14)
        assert isinstance(result, list)
        assert len(result) == 0

    # --- Ascending order verification ---

    def test_result_is_sorted(self):
        """Result should always be in ascending order."""
        result = generate_integers(5, 2)
        assert result == sorted(result)

    # --- Comprehensive range tests ---

    @pytest.mark.parametrize("a, b, expected", [
        (1, 1, []),
        (2, 2, [2]),
        (3, 3, []),
        (4, 4, [4]),
        (5, 5, []),
        (6, 6, [6]),
        (7, 7, []),
        (8, 8, [8]),
        (9, 9, []),
        (0, 0, [0]),
        (1, 2, [2]),
        (1, 3, [2]),
        (1, 4, [2, 4]),
        (1, 5, [2, 4]),
        (1, 6, [2, 4, 6]),
        (1, 7, [2, 4, 6]),
        (1, 8, [2, 4, 6, 8]),
        (1, 9, [2, 4, 6, 8]),
        (0, 1, [0]),
        (0, 2, [0, 2]),
        (0, 3, [0, 2]),
        (0, 4, [0, 2, 4]),
        (0, 5, [0, 2, 4]),
        (0, 6, [0, 2, 4, 6]),
        (0, 7, [0, 2, 4, 6]),
        (0, 8, [0, 2, 4, 6, 8]),
        (0, 9, [0, 2, 4, 6, 8]),
        (10, 10, []),
        (11, 11, []),
        (100, 200, []),
        (9, 1, [2, 4, 6, 8]),
        (8, 1, [2, 4, 6, 8]),
        (7, 1, [2, 4, 6]),
        (6, 1, [2, 4, 6]),
        (5, 1, [2, 4]),
        (4, 1, [2, 4]),
        (3, 1, [2]),
        (2, 1, [2]),
    ])
    def test_parametrized(self, a, b, expected):
        """Parametrized tests covering many input combinations."""
        assert generate_integers(a, b) == expected
