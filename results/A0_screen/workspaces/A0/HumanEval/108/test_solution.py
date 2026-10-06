import pytest
from solution import count_nums


class TestCountNums:
    """Tests for the count_nums function."""

    def test_empty_array(self):
        assert count_nums([]) == 0

    def test_example_1(self):
        assert count_nums([-1, 11, -11]) == 1

    def test_example_2(self):
        assert count_nums([1, 1, 2]) == 3

    def test_all_positive(self):
        assert count_nums([1, 2, 3]) == 3

    def test_all_negative_with_positive_digit_sum(self):
        # -1 has signed digits [-1], sum = -1 -> not counted
        # -11 has signed digits [-1, 1], sum = 0 -> not counted
        # -12 has signed digits [-1, 2], sum = 1 -> counted
        assert count_nums([-1, -11, -12]) == 1

    def test_single_zero(self):
        assert count_nums([0]) == 0

    def test_mixed_values(self):
        # 5 -> sum=5 > 0 (counted)
        # -5 -> sum=-5 <= 0 (not counted)
        # 10 -> sum=1 > 0 (counted)
        # -10 -> sum=-1 <= 0 (not counted)
        # 99 -> sum=18 > 0 (counted)
        assert count_nums([5, -5, 10, -10, 99]) == 3

    def test_large_numbers(self):
        # 999999 -> sum=54 > 0 (counted)
        # -999999 -> signed digits [-9,9,9,9,9,9], sum=45 > 0 (counted)
        assert count_nums([999999, -999999]) == 2

    def test_number_with_zero_digits(self):
        # 101 -> sum=2 > 0 (counted)
        # -101 -> sum=-1+0+1=0 (not counted)
        assert count_nums([101, -101]) == 1

    def test_only_zeros(self):
        assert count_nums([0, 0, 0]) == 0

    def test_negative_one(self):
        # -1 has signed digit [-1], sum = -1 <= 0
        assert count_nums([-1]) == 0

    def test_positive_one(self):
        assert count_nums([1]) == 1
