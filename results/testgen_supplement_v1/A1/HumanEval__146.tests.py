import pytest
from solution import specialFilter


class TestSpecialFilterDocstringExamples:
    """Test cases directly from the function's docstring."""

    def test_example_1(self):
        assert specialFilter([15, -73, 14, -15]) == 1

    def test_example_2(self):
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2


class TestSpecialFilterNormalCases:
    """Typical inputs covering various combinations."""

    def test_all_match(self):
        """All numbers satisfy every condition."""
        assert specialFilter([11, 33, 55, 77, 99]) == 5

    def test_none_match_small_numbers(self):
        """All numbers are <= 10, so none qualify."""
        assert specialFilter([1, 2, 3, 4, 5]) == 0

    def test_even_digits_fail(self):
        """Numbers with at least one even digit should not match."""
        assert specialFilter([12, 21, 22, 45, 68]) == 0

    def test_mixed_positive_negative(self):
        """Negative numbers cannot match (first char is '-')."""
        assert specialFilter([-11, -33, 11, 33]) == 2

    def test_numbers_ending_in_even(self):
        """Only those with both first AND last digit odd count."""
        assert specialFilter([11, 13, 14, 16, 18]) == 2

    def test_large_odd_odd_numbers(self):
        """Multi-digit numbers with all odd digits."""
        assert specialFilter([111, 333, 555, 777, 999]) == 5

    def test_hundreds_range(self):
        """Numbers in 100s range with odd first and last digits."""
        assert specialFilter([101, 103, 105, 107, 109]) == 5

    def test_single_matching_element(self):
        """A list with exactly one qualifying element."""
        assert specialFilter([42, 11, 999]) == 2


class TestSpecialFilterBoundaryCases:
    """Edge-of-range inputs."""

    def test_exactly_ten(self):
        """10 is not strictly greater than 10."""
        assert specialFilter([10]) == 0

    def test_just_above_ten(self):
        """11 is the smallest integer > 10 with odd first and last digit."""
        assert specialFilter([11]) == 1

    def test_single_non_matching(self):
        """Single element that does not qualify."""
        assert specialFilter([5]) == 0

    def test_single_large_qualifying(self):
        """Largest two-digit number with odd first and last digit."""
        assert specialFilter([99]) == 1

    def test_boundary_10_and_11(self):
        """10 fails (> 10), 11 passes."""
        assert specialFilter([10, 11]) == 1

    def test_numbers_at_100(self):
        """100 has last digit 0 (even), so it fails."""
        assert specialFilter([100]) == 0

    def test_101_passes(self):
        """101: > 10, first='1' (odd), last='1' (odd)."""
        assert specialFilter([101]) == 1

    def test_199_passes(self):
        """199: > 10, first='1' (odd), last='9' (odd)."""
        assert specialFilter([199]) == 1

    def test_91_passes(self):
        """91: > 10, first='9' (odd), last='1' (odd)."""
        assert specialFilter([91]) == 1

    def test_99_is_max_two_digit(self):
        """99 is the max two-digit number with both digits odd."""
        assert specialFilter([99]) == 1


class TestSpecialFilterEmptyAndZeroInputs:
    """Empty, null-like, and zero-value inputs."""

    def test_empty_list(self):
        assert specialFilter([]) == 0

    def test_zeros_only(self):
        assert specialFilter([0, 0, 0]) == 0

    def test_single_zero(self):
        assert specialFilter([0]) == 0

    def test_negative_zeros(self):
        assert specialFilter([-0, 0]) == 0


class TestSpecialFilterEdgeValues:
    """Additional edge cases around digit patterns."""

    def test_first_digit_even_last_odd(self):
        """First digit even means no match regardless of last digit."""
        assert specialFilter([21, 43, 65, 87]) == 0

    def test_first_digit_odd_last_even(self):
        """Last digit even means no match regardless of first digit."""
        assert specialFilter([12, 34, 56, 78]) == 0

    def test_all_same_digit(self):
        """Numbers like 11, 33, 55, 77, 99 — all same odd digit."""
        assert specialFilter([11, 33, 55, 77, 99]) == 5

    def test_single_digit_numbers(self):
        """Single-digit numbers are all <= 10, so none qualify."""
        assert specialFilter([1, 3, 5, 7, 9]) == 0

    def test_three_digit_all_odd(self):
        """Three-digit numbers with all odd digits."""
        assert specialFilter([111, 333, 555]) == 3

    def test_three_digit_middle_even_no_match(self):
        """Middle digit can be even; only first and last matter for qualification."""
        # 121: first='1'(odd), last='1'(odd) -> qualifies
        # 112: first='1'(odd), last='2'(even) -> no
        # 211: first='2'(even) -> no
        assert specialFilter([121, 112, 211]) == 1

    def test_four_digit_all_odd(self):
        """Four-digit numbers with all odd digits."""
        assert specialFilter([1111, 3333, 5555]) == 3

    def test_large_gap_between_qualifiers(self):
        """Qualifying numbers spread far apart in the list."""
        assert specialFilter([11, 1000, 3333, 9999, 55]) == 4

    def test_no_qualifiers_in_large_list(self):
        """Large list with no qualifying elements."""
        nums = [i for i in range(1, 200) if i % 2 == 0]
        assert specialFilter(nums) == 0
