"""Unit tests for solution.generate_integers."""

import pytest
from solution import generate_integers


# ---------------------------------------------------------------------------
# 1. Normal / typical cases from the docstring
# ---------------------------------------------------------------------------

class TestNormalCases:
    def test_docstring_example_1(self):
        """generate_integers(2, 8) => [2, 4, 6, 8]"""
        assert generate_integers(2, 8) == [2, 4, 6, 8]

    def test_docstring_example_2(self):
        """generate_integers(8, 2) => [2, 4, 6, 8]  (swapped order)"""
        assert generate_integers(8, 2) == [2, 4, 6, 8]

    def test_docstring_example_3(self):
        """generate_integers(10, 14) => []  (all above single digits)"""
        assert generate_integers(10, 14) == []

    def test_range_with_some_evens(self):
        """generate_integers(1, 9) => [2, 4, 6, 8]"""
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_range_partial_evens(self):
        """generate_integers(3, 7) => [4, 6]"""
        assert generate_integers(3, 7) == [4, 6]

    def test_range_single_even(self):
        """generate_integers(4, 4) => [4]"""
        assert generate_integers(4, 4) == [4]

    def test_range_no_evens(self):
        """generate_integers(1, 1) => []  (only 1, which is odd)"""
        assert generate_integers(1, 1) == []

    def test_range_all_odds(self):
        """generate_integers(1, 3) => [2]"""
        assert generate_integers(1, 3) == [2]

    def test_large_b_capped_at_10(self):
        """generate_integers(2, 100) => [2, 4, 6, 8]  (b capped at 9)"""
        assert generate_integers(2, 100) == [2, 4, 6, 8]

    def test_swapped_large_range(self):
        """generate_integers(100, 2) => [2, 4, 6, 8]"""
        assert generate_integers(100, 2) == [2, 4, 6, 8]


# ---------------------------------------------------------------------------
# 2. Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    def test_min_positive_inputs(self):
        """generate_integers(1, 2) => [2]"""
        assert generate_integers(1, 2) == [2]

    def test_max_single_digit(self):
        """generate_integers(8, 9) => [8]"""
        assert generate_integers(8, 9) == [8]

    def test_boundary_at_10(self):
        """generate_integers(9, 10) => []  (range is [9, 10), no evens)"""
        assert generate_integers(9, 10) == []

    def test_start_at_10(self):
        """generate_integers(10, 10) => []  (empty range after cap)"""
        assert generate_integers(10, 10) == []

    def test_both_above_nine(self):
        """generate_integers(12, 20) => []"""
        assert generate_integers(12, 20) == []

    def test_one_below_one_above(self):
        """generate_integers(5, 15) => [6, 8]"""
        assert generate_integers(5, 15) == [6, 8]

    def test_reverse_one_below_one_above(self):
        """generate_integers(15, 5) => [6, 8]"""
        assert generate_integers(15, 5) == [6, 8]


# ---------------------------------------------------------------------------
# 3. Empty / zero-size / edge inputs
# ---------------------------------------------------------------------------

class TestEdgeInputs:
    def test_zero_and_nonzero(self):
        """generate_integers(0, 8) => [0, 2, 4, 6, 8]  (0 is even)"""
        assert generate_integers(0, 8) == [0, 2, 4, 6, 8]

    def test_both_zero(self):
        """generate_integers(0, 0) => [0]  (range(0, 1) = [0], 0 is even)"""
        assert generate_integers(0, 0) == [0]

    def test_negative_a_positive_b(self):
        """generate_integers(-2, 5) => [-2, 0, 2, 4]
        range(-2, min(6, 10)) = range(-2, 6); evens: -2, 0, 2, 4"""
        assert generate_integers(-2, 5) == [-2, 0, 2, 4]

    def test_both_negative(self):
        """generate_integers(-5, -2) => [-4, -2]
        range(-5, min(-1, 10)) = range(-5, -1); evens: -4, -2"""
        assert generate_integers(-5, -2) == [-4, -2]

    def test_negative_to_positive(self):
        """generate_integers(-10, 10) => [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8]
        range(-10, min(11, 10)) = range(-10, 10)"""
        assert generate_integers(-10, 10) == [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8]


# ---------------------------------------------------------------------------
# 4. Invalid inputs (non-integers) — function does not validate type
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    def test_float_inputs(self):
        """Floats are accepted by Python; behaviour depends on implementation."""
        # range() rejects floats, so this will raise TypeError
        with pytest.raises(TypeError):
            generate_integers(2.5, 8.5)

    def test_string_inputs(self):
        """Strings are not valid for range(); expect TypeError."""
        with pytest.raises(TypeError):
            generate_integers("2", "8")

    def test_none_input(self):
        """None is not valid; expect TypeError."""
        with pytest.raises(TypeError):
            generate_integers(None, 8)

    def test_mixed_types(self):
        """Mixing int and str raises TypeError."""
        with pytest.raises(TypeError):
            generate_integers(2, "8")


# ---------------------------------------------------------------------------
# 5. Exception cases & return-type checks
# ---------------------------------------------------------------------------

class TestExceptionAndTypeChecks:
    def test_returns_list(self):
        """The result must always be a list."""
        result = generate_integers(2, 8)
        assert isinstance(result, list)

    def test_empty_result_is_list(self):
        """Even when empty, the result is still a list."""
        result = generate_integers(10, 14)
        assert isinstance(result, list)
        assert result == []

    def test_sorted_ascending(self):
        """Results are always in ascending order."""
        result = generate_integers(1, 9)
        assert result == sorted(result)

    def test_no_duplicates(self):
        """Each even number appears at most once."""
        result = generate_integers(1, 9)
        assert len(result) == len(set(result))

    def test_only_even_numbers(self):
        """Every element in the result is even."""
        result = generate_integers(1, 9)
        assert all(x % 2 == 0 for x in result)

    def test_values_within_single_digits(self):
        """All returned values are between 0 and 9 inclusive."""
        result = generate_integers(0, 9)
        assert all(0 <= x <= 9 for x in result)
