import pytest
from solution import sum_squares


class TestSumSquares:
    """Tests for the sum_squares function."""

    # --- Basic examples from docstring ---

    def test_example_1(self):
        assert sum_squares([1, 2, 3]) == 6

    def test_empty_list(self):
        assert sum_squares([]) == 0

    def test_example_3(self):
        assert sum_squares([-1, -5, 2, -1, -5]) == -126

    # --- Index 0 (multiple of 3 → square) ---

    def test_index_0_squared(self):
        # index 0 is multiple of 3 → square
        assert sum_squares([2]) == 4  # 2^2 = 4

    def test_index_0_negative_squared(self):
        assert sum_squares([-3]) == 9  # (-3)^2 = 9

    # --- Index 1 (not multiple of 3 or 4 → keep as-is) ---

    def test_index_1_unchanged(self):
        # index 1 is neither multiple of 3 nor 4 → add as-is
        assert sum_squares([0, 5]) == 5  # 0 + 5 = 5

    def test_index_1_positive(self):
        assert sum_squares([0, 7]) == 7

    # --- Index 2 (not multiple of 3 or 4 → keep as-is) ---

    def test_index_2_unchanged(self):
        # index 2 is neither multiple of 3 nor 4
        assert sum_squares([0, 0, 4]) == 4

    # --- Index 3 (multiple of 3 → square) ---

    def test_index_3_squared(self):
        # index 3 is multiple of 3 → square
        assert sum_squares([0, 0, 0, 2]) == 4  # 2^2 = 4

    def test_index_3_negative_squared(self):
        assert sum_squares([0, 0, 0, -2]) == 4  # (-2)^2 = 4

    # --- Index 4 (multiple of 4 but NOT 3 → cube) ---

    def test_index_4_cubed(self):
        # index 4 is multiple of 4 and not 3 → cube
        assert sum_squares([0, 0, 0, 0, 2]) == 8  # 2^3 = 8

    def test_index_4_negative_cubed(self):
        assert sum_squares([0, 0, 0, 0, -2]) == -8  # (-2)^3 = -8

    def test_index_4_zero_cubed(self):
        assert sum_squares([0, 0, 0, 0, 0]) == 0

    # --- Index 5 (not multiple of 3 or 4 → keep as-is) ---

    def test_index_5_unchanged(self):
        assert sum_squares([0, 0, 0, 0, 0, 6]) == 6

    # --- Index 6 (multiple of 3 → square) ---

    def test_index_6_squared(self):
        # index 6 is multiple of 3 → square
        assert sum_squares([0, 0, 0, 0, 0, 0, 3]) == 9  # 3^2 = 9

    # --- Index 8 (multiple of 4 but NOT 3 → cube) ---

    def test_index_8_cubed(self):
        # index 8 is multiple of 4 and not 3 → cube
        assert sum_squares([0]*8 + [2]) == 8  # 2^3 = 8

    # --- Index 12 (multiple of both 3 and 4 → square wins per elif logic) ---

    def test_index_12_squared(self):
        # index 12 is multiple of both 3 and 4; since i%3==0 check comes first, it squares
        lst = [0] * 12 + [3]
        assert sum_squares(lst) == 9  # 3^2 = 9

    def test_index_12_negative_squared(self):
        lst = [0] * 12 + [-3]
        assert sum_squares(lst) == 9  # (-3)^2 = 9

    # --- Larger lists with mixed operations ---

    def test_mixed_operations(self):
        # indices: 0(sq), 1(keep), 2(keep), 3(sq), 4(cube), 5(keep), 6(sq), 7(keep), 8(cube), 9(sq)
        # values:  [1,   2,     3,     4,     5,     6,     7,     8,     9,     10]
        # result:   1^2 + 2 + 3 + 4^2 + 5^3 + 6 + 7^2 + 8 + 9^3 + 10^2
        #         = 1 + 2 + 3 + 16 + 125 + 6 + 49 + 8 + 729 + 100 = 1039
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        assert sum_squares(lst) == 1039

    def test_all_zeros(self):
        assert sum_squares([0, 0, 0, 0, 0]) == 0

    def test_single_element_zero(self):
        assert sum_squares([0]) == 0

    def test_single_element_one(self):
        assert sum_squares([1]) == 1  # index 0 → 1^2 = 1

    def test_single_element_negative(self):
        assert sum_squares([-1]) == 1  # index 0 → (-1)^2 = 1

    # --- Edge cases with larger numbers ---

    def test_large_values(self):
        # index 0: 10^2=100, index 1: 1, index 2: 1, index 3: 2^2=4, index 4: 3^3=27
        lst = [10, 1, 1, 2, 3]
        assert sum_squares(lst) == 100 + 1 + 1 + 4 + 27  # = 133

    def test_negative_with_cubes(self):
        # index 4: (-3)^3 = -27
        lst = [0, 0, 0, 0, -3]
        assert sum_squares(lst) == -27

    def test_mixed_positive_negative(self):
        # index 0: 2^2=4, index 1: -1, index 2: 3, index 3: (-2)^2=4, index 4: 1^3=1
        lst = [2, -1, 3, -2, 1]
        assert sum_squares(lst) == 4 + (-1) + 3 + 4 + 1  # = 11
