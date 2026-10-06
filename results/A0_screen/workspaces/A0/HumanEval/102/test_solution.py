import pytest
from solution import choose_num


class TestChooseNumBasicCases:
    """Test basic cases from the docstring."""

    def test_basic_example_1(self):
        assert choose_num(12, 15) == 14

    def test_basic_example_2(self):
        assert choose_num(13, 12) == -1

    def test_basic_example_3(self):
        assert choose_num(1, 2) == 2

    def test_basic_example_4(self):
        assert choose_num(1, 1) == -1


class TestEvenRangeEndpoints:
    """When both endpoints are even, the answer should be y."""

    def test_both_even(self):
        assert choose_num(2, 8) == 8

    def test_same_even(self):
        assert choose_num(4, 4) == 4

    def test_single_even_number(self):
        assert choose_num(10, 10) == 10


class TestOddRangeEndpoints:
    """When y is odd, the largest even <= y is y - 1, provided y - 1 >= x."""

    def test_y_odd_larger_range(self):
        assert choose_num(2, 7) == 6

    def test_y_odd_x_smaller(self):
        assert choose_num(1, 9) == 8

    def test_y_odd_adjacent(self):
        assert choose_num(5, 6) == 6

    def test_y_odd_equal_to_x(self):
        # x == y and both odd => no even number in [x, y]
        assert choose_num(7, 7) == -1


class TestNoEvenInRange:
    """When there is no even number in [x, y], return -1."""

    def test_single_odd_number(self):
        assert choose_num(3, 3) == -1

    def test_single_odd_one(self):
        assert choose_num(1, 1) == -1

    def test_reversed_range(self):
        assert choose_num(10, 5) == -1

    def test_reversed_range_with_even(self):
        assert choose_num(8, 3) == -1


class TestEdgeCases:
    """Edge cases involving small numbers and boundary conditions."""

    def test_min_positive_numbers(self):
        assert choose_num(1, 2) == 2

    def test_two_consecutive_odds_impossible(self):
        # [3, 3] has no even number
        assert choose_num(3, 3) == -1

    def test_large_numbers(self):
        assert choose_num(100, 200) == 200

    def test_large_numbers_y_odd(self):
        assert choose_num(100, 201) == 200

    def test_large_numbers_x_gt_y(self):
        assert choose_num(200, 100) == -1

    def test_x_equals_y_even(self):
        assert choose_num(100, 100) == 100

    def test_x_equals_y_odd(self):
        assert choose_num(101, 101) == -1


class TestBoundaryConditions:
    """Tests around the boundary between even and odd."""

    def test_range_with_only_two_numbers_even_at_end(self):
        assert choose_num(5, 6) == 6

    def test_range_with_only_two_numbers_odd_at_end(self):
        assert choose_num(4, 5) == 4

    def test_range_of_three_numbers_middle_even(self):
        assert choose_num(3, 5) == 4

    def test_range_of_three_numbers_all_odd(self):
        # [3, 5] = {3, 4, 5}, largest even is 4
        assert choose_num(3, 5) == 4

    def test_range_of_two_numbers_both_even(self):
        assert choose_num(4, 6) == 6

    def test_range_of_two_numbers_both_odd(self):
        # [3, 5] = {3, 4, 5} — wait, that's 3 numbers.
        # [3, 4] = {3, 4}, largest even is 4
        assert choose_num(3, 4) == 4


class TestNegativeAndZeroInput:
    """The docstring says 'positive numbers', but test behavior for non-positive inputs."""

    def test_zero_input(self):
        # 0 is even, so choose_num(0, 0) should return 0
        assert choose_num(0, 0) == 0

    def test_zero_and_positive(self):
        assert choose_num(0, 5) == 4

    def test_negative_start(self):
        # Negative numbers: -2 is even
        assert choose_num(-2, 5) == 4

    def test_both_negative_even(self):
        assert choose_num(-6, -2) == -2

    def test_both_negative_odd(self):
        # [-5, -1] = {-5, -4, -3, -2, -1}, largest even is -2
        assert choose_num(-5, -1) == -2

    def test_negative_reversed(self):
        assert choose_num(5, -5) == -1
