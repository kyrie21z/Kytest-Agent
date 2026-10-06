import pytest
from solution import generate_integers


class TestGenerateIntegersNormalCases:
    """Test typical / normal inputs as documented."""

    def test_example_1(self):
        # From docstring: generate_integers(2, 8) => [2, 4, 6, 8]
        assert generate_integers(2, 8) == [2, 4, 6, 8]

    def test_example_2_swapped(self):
        # From docstring: generate_integers(8, 2) => [2, 4, 6, 8]
        assert generate_integers(8, 2) == [2, 4, 6, 8]

    def test_example_3_no_single_digit(self):
        # From docstring: generate_integers(10, 14) => []
        assert generate_integers(10, 14) == []

    def test_full_range_1_to_9(self):
        # All single-digit numbers; should return all even ones
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_partial_range(self):
        # Range 3..7 contains evens 4 and 6
        assert generate_integers(3, 7) == [4, 6]

    def test_reverse_partial_range(self):
        # Same range but reversed arguments
        assert generate_integers(7, 3) == [4, 6]

    def test_range_including_zero_even(self):
        # Even digit 0 is included when range covers it
        assert generate_integers(0, 5) == [0, 2, 4]

    def test_range_starting_at_even(self):
        assert generate_integers(2, 5) == [2, 4]

    def test_range_ending_at_even(self):
        assert generate_integers(3, 8) == [4, 6, 8]

    def test_large_range_covering_all_digits(self):
        # range(-5, min(16, 10)) = range(-5, 10) -> evens: -4, -2, 0, 2, 4, 6, 8
        assert generate_integers(-5, 15) == [-4, -2, 0, 2, 4, 6, 8]


class TestGenerateIntegersBoundaryCases:
    """Test edges of valid input ranges."""

    def test_min_positive_a_b_equal(self):
        # Smallest positive integers, equal
        assert generate_integers(1, 1) == []

    def test_single_even_number(self):
        # Both args point to the same even number
        assert generate_integers(4, 4) == [4]

    def test_single_odd_number(self):
        # Both args point to the same odd number
        assert generate_integers(3, 3) == []

    def test_boundary_at_9(self):
        # Upper boundary of single-digit range
        assert generate_integers(8, 9) == [8]

    def test_boundary_at_9_reversed(self):
        assert generate_integers(9, 8) == [8]

    def test_boundary_at_10_exclusive(self):
        # b+1 = 11, min(11, 10) = 10, range(1, 10) = 1..9
        assert generate_integers(1, 10) == [2, 4, 6, 8]

    def test_boundary_at_10_reversed(self):
        assert generate_integers(10, 1) == [2, 4, 6, 8]

    def test_range_just_above_single_digits(self):
        # No single-digit numbers in range 10..12
        assert generate_integers(10, 12) == []

    def test_range_straddling_boundary(self):
        # Range 8..12 includes single-digit evens 8, 10 is excluded by min
        assert generate_integers(8, 12) == [8]

    def test_range_0_to_0(self):
        assert generate_integers(0, 0) == [0]

    def test_range_0_to_1(self):
        assert generate_integers(0, 1) == [0]

    def test_range_0_to_9(self):
        assert generate_integers(0, 9) == [0, 2, 4, 6, 8]

    def test_range_0_to_8(self):
        assert generate_integers(0, 8) == [0, 2, 4, 6, 8]

    def test_negative_range(self):
        # Negative numbers: range(-2, 0) after swap is (-2, 0), min(0+1,10)=1
        # range(-2, 1) gives -2, -1, 0 -> evens: -2, 0
        assert generate_integers(-2, 0) == [-2, 0]


class TestGenerateIntegersEmptyAndZeroSize:
    """Test empty results and zero-size-like inputs."""

    def test_identical_odd_inputs(self):
        assert generate_integers(7, 7) == []

    def test_identical_even_inputs(self):
        assert generate_integers(6, 6) == [6]

    def test_adjacent_odd_numbers(self):
        # Two consecutive odds, no evens between them
        assert generate_integers(3, 5) == [4]

    def test_adjacent_even_numbers(self):
        # Two consecutive evens
        assert generate_integers(2, 4) == [2, 4]

    def test_consecutive_numbers_one_even(self):
        assert generate_integers(5, 6) == [6]

    def test_consecutive_numbers_no_even(self):
        assert generate_integers(5, 7) == [6]


class TestGenerateIntegersEdgeBehavior:
    """Test additional edge behaviors and corner cases."""

    def test_very_large_values(self):
        # Large values beyond single digits should produce empty list
        assert generate_integers(100, 200) == []

    def test_very_large_values_reversed(self):
        assert generate_integers(200, 100) == []

    def test_negative_and_positive_mix(self):
        # range(-10, min(6, 10)) = range(-10, 6) -> evens: -10, -8, -6, -4, -2, 0, 2, 4
        assert generate_integers(-10, 5) == [-10, -8, -6, -4, -2, 0, 2, 4]

    def test_both_negative(self):
        # Both negative: range(-8, -2) after swap is (-8, -2)
        # min(-2+1, 10) = min(-1, 10) = -1
        # range(-8, -1) = -8,-7,...,-2 -> evens: -8,-6,-4,-2
        assert generate_integers(-8, -2) == [-8, -6, -4, -2]

    def test_both_negative_reversed(self):
        assert generate_integers(-2, -8) == [-8, -6, -4, -2]

    def test_one_is_zero(self):
        assert generate_integers(0, 10) == [0, 2, 4, 6, 8]

    def test_returned_list_is_sorted(self):
        # Verify ascending order regardless of input order
        result = generate_integers(9, 1)
        assert result == sorted(result)

    def test_returned_list_contains_only_evens(self):
        result = generate_integers(1, 9)
        assert all(n % 2 == 0 for n in result)

    def test_returned_list_contains_only_single_digits(self):
        result = generate_integers(1, 9)
        assert all(-1 < n < 10 for n in result)

    def test_result_is_list_type(self):
        assert isinstance(generate_integers(1, 9), list)

    def test_empty_result_is_list(self):
        assert isinstance(generate_integers(10, 20), list)
        assert len(generate_integers(10, 20)) == 0
