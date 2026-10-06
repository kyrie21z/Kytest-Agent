"""Unit tests for specialFilter in solution.py."""

import pytest
from solution import specialFilter


# ---------------------------------------------------------------------------
# 1. Normal / typical inputs (including the docstring examples)
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Typical inputs with a mix of qualifying and non-qualifying numbers."""

    def test_docstring_example_1(self):
        # [15, -73, 14, -15] => 1
        # 15: >10, first='1'(odd), last='5'(odd) ✓
        # -73: first='-' ✗
        # 14: >10, first='1'(odd), last='4'(even) ✗
        # -15: first='-' ✗
        assert specialFilter([15, -73, 14, -15]) == 1

    def test_docstring_example_2(self):
        # [33, -2, -3, 45, 21, 109] => 2
        # 33: >10, '3','3' ✓
        # -2: first='-' ✗
        # -3: first='-' ✗
        # 45: >10, '4'(even) ✗
        # 21: >10, '2'(even) ✗
        # 109: >10, '1','9' ✓
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2

    def test_all_qualifying(self):
        # Every number satisfies all three conditions
        assert specialFilter([11, 13, 15, 17, 19, 31, 33, 55, 77, 99]) == 10

    def test_none_qualifying(self):
        # No number meets all criteria
        assert specialFilter([2, 4, 6, 8, 10, 12, 20, 22]) == 0

    def test_mixed_positive_and_negative(self):
        # Mix of positives and negatives; only some qualify
        result = specialFilter([11, -11, 13, -13, 15, -15])
        # 11✓, -11✗, 13✓, -13✗, 15✓, -15✗
        assert result == 3

    def test_single_element_qualifying(self):
        assert specialFilter([11]) == 1

    def test_single_element_not_qualifying(self):
        assert specialFilter([7]) == 0  # 7 <= 10


# ---------------------------------------------------------------------------
# 2. Boundary cases at the edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:

    def test_exactly_10(self):
        # 10 is NOT > 10, so it should not count
        assert specialFilter([10]) == 0

    def test_just_above_10(self):
        # 11 is > 10, first='1', last='1' → qualifies
        assert specialFilter([11]) == 1

    def test_just_below_10(self):
        # 9 is not > 10
        assert specialFilter([9]) == 0

    def test_two_digit_odd_first_even_last(self):
        # 12: >10, first='1'(odd), last='2'(even) → no
        assert specialFilter([12]) == 0

    def test_two_digit_even_first_odd_last(self):
        # 21: >10, first='2'(even), last='1'(odd) → no
        assert specialFilter([21]) == 0

    def test_two_digit_even_first_even_last(self):
        # 22: >10, first='2'(even), last='2'(even) → no
        assert specialFilter([22]) == 0

    def test_three_digit_qualifying(self):
        # 111: >10, first='1', last='1' → yes
        assert specialFilter([111]) == 1

    def test_three_digit_non_qualifying(self):
        # 121: >10, first='1'(odd), last='1'(odd) → YES actually
        assert specialFilter([121]) == 1

    def test_largest_single_digit(self):
        # 9 is not > 10
        assert specialFilter([9]) == 0

    def test_smallest_qualifying_number(self):
        # 11 is the smallest number > 10 with both first and last odd
        assert specialFilter([11]) == 1


# ---------------------------------------------------------------------------
# 3. Empty, null-like, or zero-size inputs
# ---------------------------------------------------------------------------

class TestEmptyAndZeroInputs:

    def test_empty_list(self):
        assert specialFilter([]) == 0

    def test_list_of_zeros(self):
        # 0 is not > 10
        assert specialFilter([0, 0, 0]) == 0

    def test_single_zero(self):
        assert specialFilter([0]) == 0


# ---------------------------------------------------------------------------
# 4. Invalid / unusual inputs
# ---------------------------------------------------------------------------

class TestUnusualInputs:

    def test_all_negative_numbers(self):
        # Negative numbers start with '-', which is not in odd digits
        assert specialFilter([-11, -13, -15, -17, -19]) == 0

    def test_all_negative_large(self):
        assert specialFilter([-111, -333, -555]) == 0

    def test_mixed_with_duplicates(self):
        # [11, 11, 11] → all three qualify
        assert specialFilter([11, 11, 11]) == 3

    def test_numbers_with_same_first_and_last(self):
        # 33, 55, 77, 99 all have same odd first and last digit
        assert specialFilter([33, 55, 77, 99]) == 4

    def test_first_digit_odd_last_even(self):
        # 13: first='1'(odd), last='3'(odd) → YES
        assert specialFilter([13]) == 1

    def test_first_digit_even_last_odd(self):
        # 31: first='3'(odd), last='1'(odd) → YES
        assert specialFilter([31]) == 1

    def test_first_digit_even_last_even(self):
        # 24: first='2'(even), last='4'(even) → NO
        assert specialFilter([24]) == 0


# ---------------------------------------------------------------------------
# 5. Exception / error handling cases
# ---------------------------------------------------------------------------

class TestExceptionCases:

    def test_empty_input_no_exception(self):
        # Should not raise; returns 0
        assert specialFilter([]) == 0

    def test_single_element_no_exception(self):
        assert specialFilter([11]) == 1

    def test_large_list(self):
        # Stress test with many elements
        nums = [i for i in range(1, 201)]
        # Count manually: numbers > 10 with odd first and last digit
        expected = sum(
            1 for n in nums
            if n > 10 and str(n)[0] in "13579" and str(n)[-1] in "13579"
        )
        assert specialFilter(nums) == expected


# ---------------------------------------------------------------------------
# Additional thorough coverage: every odd-first-digit × odd-last-digit combo
# ---------------------------------------------------------------------------

class TestComprehensiveDigitCoverage:
    """Check each combination of odd first and odd last digits."""

    def _check(self, num, expected):
        assert specialFilter([num]) == expected

    def test_11(self):
        self._check(11, 1)

    def test_13(self):
        self._check(13, 1)

    def test_15(self):
        self._check(15, 1)

    def test_17(self):
        self._check(17, 1)

    def test_19(self):
        self._check(19, 1)

    def test_31(self):
        self._check(31, 1)

    def test_33(self):
        self._check(33, 1)

    def test_35(self):
        self._check(35, 1)

    def test_37(self):
        self._check(37, 1)

    def test_39(self):
        self._check(39, 1)

    def test_51(self):
        self._check(51, 1)

    def test_53(self):
        self._check(53, 1)

    def test_55(self):
        self._check(55, 1)

    def test_57(self):
        self._check(57, 1)

    def test_59(self):
        self._check(59, 1)

    def test_71(self):
        self._check(71, 1)

    def test_73(self):
        self._check(73, 1)

    def test_75(self):
        self._check(75, 1)

    def test_77(self):
        self._check(77, 1)

    def test_79(self):
        self._check(79, 1)

    def test_91(self):
        self._check(91, 1)

    def test_93(self):
        self._check(93, 1)

    def test_95(self):
        self._check(95, 1)

    def test_97(self):
        self._check(97, 1)

    def test_99(self):
        self._check(99, 1)

    # Now check that even-digit combos do NOT qualify
    def test_12_even_last(self):
        self._check(12, 0)

    def test_21_even_first(self):
        self._check(21, 0)

    def test_22_both_even(self):
        self._check(22, 0)

    def test_24_both_even(self):
        self._check(24, 0)

    def test_42_both_even(self):
        self._check(42, 0)

    def test_68_both_even(self):
        self._check(68, 0)

    def test_86_both_even(self):
        self._check(86, 0)

    def test_00_like_10(self):
        # 10: >10 is False
        self._check(10, 0)

    def test_01_like_1(self):
        # 1: not > 10
        self._check(1, 0)

    def test_03_like_3(self):
        # 3: not > 10
        self._check(3, 0)

    def test_05_like_5(self):
        # 5: not > 10
        self._check(5, 0)

    def test_07_like_7(self):
        # 7: not > 10
        self._check(7, 0)

    def test_09_like_9(self):
        # 9: not > 10
        self._check(9, 0)
