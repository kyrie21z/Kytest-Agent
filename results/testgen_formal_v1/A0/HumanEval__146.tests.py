import pytest
from solution import specialFilter


class TestSpecialFilterBasicExamples:
    """Tests using the examples from the docstring."""

    def test_example_1(self):
        # [15, -73, 14, -15] => 1
        # 15: >10, first='1'(odd), last='5'(odd) ✓
        # -73: not >10 ✗
        # 14: >10, first='1'(odd), last='4'(even) ✗
        # -15: not >10 ✗
        assert specialFilter([15, -73, 14, -15]) == 1

    def test_example_2(self):
        # [33, -2, -3, 45, 21, 109] => 2
        # 33: >10, first='3'(odd), last='3'(odd) ✓
        # -2: not >10 ✗
        # -3: not >10 ✗
        # 45: >10, first='4'(even) ✗
        # 21: >10, first='2'(even) ✗
        # 109: >10, first='1'(odd), last='9'(odd) ✓
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2


class TestEmptyAndSingleElement:
    """Tests for edge cases with empty or single-element lists."""

    def test_empty_list(self):
        assert specialFilter([]) == 0

    def test_single_element_passes(self):
        assert specialFilter([15]) == 1

    def test_single_element_fails(self):
        assert specialFilter([5]) == 0

    def test_single_negative_fails(self):
        assert specialFilter([-15]) == 0


class TestAllPassing:
    """Tests where all elements satisfy the condition."""

    def test_all_pass(self):
        assert specialFilter([11, 33, 55, 79, 91]) == 5

    def test_all_pass_large_numbers(self):
        assert specialFilter([111, 333, 5555, 77777]) == 4


class TestNonePassing:
    """Tests where no elements satisfy the condition."""

    def test_no_elements_gt_10(self):
        assert specialFilter([1, 3, 5, 7, 9]) == 0

    def test_even_first_digit(self):
        assert specialFilter([21, 43, 65, 89]) == 0

    def test_even_last_digit(self):
        assert specialFilter([12, 34, 56, 78]) == 0

    def test_all_negative(self):
        assert specialFilter([-11, -33, -55, -77]) == 0

    def test_mixed_none_qualify(self):
        assert specialFilter([10, 20, 30, 40]) == 0


class TestBoundaryValues:
    """Tests around boundary conditions."""

    def test_exactly_10(self):
        # 10 is not > 10
        assert specialFilter([10]) == 0

    def test_exactly_11(self):
        # 11: >10, first='1', last='1' — both odd
        assert specialFilter([11]) == 1

    def test_just_above_10(self):
        assert specialFilter([11, 12, 13, 14, 15, 16, 17, 18, 19]) == 5
        # 11✓, 12✗(last even), 13✓, 14✗, 15✓, 16✗, 17✓, 18✗, 19✓

    def test_two_digit_odd_both(self):
        # All two-digit numbers with odd first and odd last
        nums = [11, 13, 15, 17, 19, 31, 33, 35, 37, 39,
                51, 53, 55, 57, 59, 71, 73, 75, 77, 79,
                91, 93, 95, 97, 99]
        assert specialFilter(nums) == 25

    def test_three_digit_numbers(self):
        # 101: >10, first='1'(odd), last='1'(odd) ✓
        # 109: >10, first='1'(odd), last='9'(odd) ✓
        # 100: >10, first='1'(odd), last='0'(even) ✗
        assert specialFilter([101, 109, 100]) == 2


class TestNegativeNumbers:
    """Tests specifically for negative number handling."""

    def test_negative_with_odd_digits(self):
        # Negative numbers are not > 10, so none should pass
        assert specialFilter([-11, -13, -15, -17, -19]) == 0

    def test_mixed_positive_and_negative(self):
        # Only positive numbers > 10 with odd first/last digits count
        result = specialFilter([15, -15, 33, -33, 55, -55])
        assert result == 3  # 15, 33, 55 pass; negatives don't


class TestLargeNumbers:
    """Tests with larger numbers."""

    def test_large_number_passes(self):
        assert specialFilter([11111, 99999]) == 2

    def test_large_number_fails(self):
        # 12345: first='1'(odd), last='5'(odd) — actually passes!
        # 21111: first='2'(even) — fails
        assert specialFilter([21111, 12345]) == 1

    def test_many_elements(self):
        nums = list(range(1, 101))
        # Count manually: numbers > 10 with odd first and odd last digit
        expected = 0
        for n in range(11, 101):
            s = str(n)
            if s[0] in "13579" and s[-1] in "13579":
                expected += 1
        assert specialFilter(nums) == expected


class TestReturnTypes:
    """Tests to verify return type is int."""

    def test_returns_int_for_empty(self):
        result = specialFilter([])
        assert isinstance(result, int)

    def test_returns_int_for_nonempty(self):
        result = specialFilter([15])
        assert isinstance(result, int)

    def test_returns_zero_not_none(self):
        assert specialFilter([]) != None


class TestDuplicates:
    """Tests with duplicate values."""

    def test_duplicate_values(self):
        assert specialFilter([15, 15, 15]) == 3

    def test_duplicate_nonqualifying(self):
        assert specialFilter([12, 12, 12]) == 0
