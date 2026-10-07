import pytest
from solution import rearrange_bigger


class TestRearrangeBiggerBasic:
    """Tests for basic functionality of rearrange_bigger."""

    def test_two_digits(self):
        # 12 -> 21
        assert rearrange_bigger(12) == 21

    def test_two_digits_reversed(self):
        # 21 -> False (no bigger number possible)
        assert rearrange_bigger(21) is False

    def test_three_digits_simple(self):
        # 123 -> 132
        assert rearrange_bigger(123) == 132

    def test_three_digits_middle_change(self):
        # 132 -> 213
        assert rearrange_bigger(132) == 213

    def test_three_digits_last_change(self):
        # 231 -> 312
        assert rearrange_bigger(231) == 312

    def test_no_bigger_possible(self):
        # 321 -> False (digits in descending order)
        assert rearrange_bigger(321) is False

    def test_all_same_digits(self):
        # 111 -> False (all digits same, no bigger arrangement)
        assert rearrange_bigger(111) is False


class TestRearrangeBiggerEdgeCases:
    """Tests for edge cases."""

    def test_single_digit(self):
        # Single digit has no bigger arrangement
        assert rearrange_bigger(5) is False

    def test_two_same_digits(self):
        # 22 -> False
        assert rearrange_bigger(22) is False

    def test_zero_in_number(self):
        # 102 -> 120
        assert rearrange_bigger(102) == 120

    def test_leading_zero_after_rearrange(self):
        # 1999999999 -> 9199999999 (large number with 1 followed by many 9s)
        assert rearrange_bigger(1999999999) == 9199999999

    def test_largest_permutation(self):
        # 987654321 -> False (already largest)
        assert rearrange_bigger(987654321) is False

    def test_smallest_permutation(self):
        # 123456789 -> 123456798
        assert rearrange_bigger(123456789) == 123456798


class TestRearrangeBiggerRepeatedDigits:
    """Tests for numbers with repeated digits."""

    def test_two_repeated_digits(self):
        # 122 -> 212
        assert rearrange_bigger(122) == 212

    def test_multiple_repeated_digits(self):
        # 121 -> 211
        assert rearrange_bigger(121) == 211

    def test_many_repeated_digits(self):
        # 199 -> 919
        assert rearrange_bigger(199) == 919

    def test_repeated_at_end(self):
        # 1233 -> 1323
        assert rearrange_bigger(1233) == 1323

    def test_repeated_middle(self):
        # 1332 -> 2133
        assert rearrange_bigger(1332) == 2133

    def test_all_zeros_except_one(self):
        # 1000 -> 1000 (next bigger would need more digits, so check behavior)
        # Actually 1000 -> we look for next bigger: digits are [1,0,0,0]
        # i=0: nums[0]='1' < nums[1]='0'? No. So no swap found.
        # Wait, '1' > '0', so condition fails. Let's trace carefully.
        # nums = ['1','0','0','0']
        # i=2: nums[2]='0' < nums[3]='0'? No ('0' is not < '0')
        # i=1: nums[1]='0' < nums[2]='0'? No
        # i=0: nums[0]='1' < nums[1]='0'? No
        # Returns False
        assert rearrange_bigger(1000) is False


class TestRearrangeBiggerLargerNumbers:
    """Tests for larger numbers."""

    def test_five_digits(self):
        # 54321 -> False
        assert rearrange_bigger(54321) is False

    def test_five_digits_with_solution(self):
        # 12345 -> 12354
        assert rearrange_bigger(12345) == 12354

    def test_six_digits(self):
        # 123456 -> 123465
        assert rearrange_bigger(123456) == 123465

    def test_large_number_with_solution(self):
        # 1999999999 -> 9199999999
        assert rearrange_bigger(1999999999) == 9199999999

    def test_number_ending_in_nine(self):
        # 129 -> 192
        assert rearrange_bigger(129) == 192

    def test_number_with_descending_suffix(self):
        # 1322 -> 2123
        assert rearrange_bigger(1322) == 2123


class TestRearrangeBiggerReturnTypes:
    """Tests for return type correctness."""

    def test_returns_int_on_success(self):
        result = rearrange_bigger(12)
        assert isinstance(result, int)

    def test_returns_false_on_failure(self):
        result = rearrange_bigger(321)
        assert result is False

    def test_result_is_larger_than_input(self):
        n = 123
        result = rearrange_bigger(n)
        assert result > n

    def test_result_has_same_digits(self):
        n = 1234
        result = rearrange_bigger(n)
        assert sorted(str(n)) == sorted(str(result))


class TestRearrangeBiggerNextPermutationProperty:
    """Tests that verify the result is indeed the *next* bigger number."""

    def test_immediate_next(self):
        # The result should be the smallest number bigger than input
        # using the same digits
        n = 1234
        result = rearrange_bigger(n)
        # Check that no permutation between n and result uses same digits
        all_perms = sorted(int(''.join(p)) for p in __import__('itertools').permutations(str(n)))
        assert result == all_perms[all_perms.index(n) + 1]

    def test_immediate_next_complex(self):
        n = 543210
        result = rearrange_bigger(n)
        if result is not False:
            all_perms = sorted(int(''.join(p)) for p in __import__('itertools').permutations(str(n)))
            assert result == all_perms[all_perms.index(n) + 1]

    def test_immediate_next_with_duplicates(self):
        n = 122
        result = rearrange_bigger(n)
        all_perms = sorted(set(int(''.join(p)) for p in __import__('itertools').permutations(str(n))))
        assert result == all_perms[all_perms.index(n) + 1]
