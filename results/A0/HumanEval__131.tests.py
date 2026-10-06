import pytest
from solution import digits


class TestDigits:
    """Tests for the digits() function."""

    # --- Examples from the docstring ---

    def test_single_odd_digit(self):
        assert digits(1) == 1

    def test_single_even_digit(self):
        assert digits(4) == 0

    def test_mixed_digits(self):
        assert digits(235) == 15  # 3 * 5 = 15

    # --- Single-digit inputs ---

    @pytest.mark.parametrize("n, expected", [
        (1, 1),
        (3, 3),
        (5, 5),
        (7, 7),
        (9, 9),
        (2, 0),
        (4, 0),
        (6, 0),
        (8, 0),
        (0, 0),
    ])
    def test_single_digit(self, n, expected):
        assert digits(n) == expected

    # --- All-even-digit numbers (should return 0) ---

    @pytest.mark.parametrize("n, expected", [
        (2, 0),
        (22, 0),
        (246, 0),
        (8888, 0),
        (20468, 0),
    ])
    def test_all_even_digits(self, n, expected):
        assert digits(n) == expected

    # --- All-odd-digit numbers ---

    @pytest.mark.parametrize("n, expected", [
        (1, 1),
        (3, 3),
        (13, 3),       # 1 * 3 = 3
        (357, 105),    # 3 * 5 * 7 = 105
        (13579, 945),  # 1 * 3 * 5 * 7 * 9 = 945
    ])
    def test_all_odd_digits(self, n, expected):
        assert digits(n) == expected

    # --- Mixed digits with at least one odd ---

    @pytest.mark.parametrize("n, expected", [
        (235, 15),     # 3 * 5 = 15
        (12345, 15),   # 1 * 3 * 5 = 15
        (24681, 1),    # 1 = 1
        (11111, 1),    # 1 * 1 * 1 * 1 * 1 = 1
        (22223, 3),    # 3 = 3
        (123, 3),      # 1 * 3 = 3
        (987654321, 945),  # 9 * 7 * 5 * 3 * 1 = 945
    ])
    def test_mixed_digits_with_odds(self, n, expected):
        assert digits(n) == expected

    # --- Large numbers ---

    def test_large_number(self):
        # Product of odd digits in 99999999999999999999
        assert digits(99999999999999999999) == 9**20

    def test_large_number_no_odds(self):
        assert digits(22222222222222222222) == 0

    # --- Edge case: number containing zero ---

    @pytest.mark.parametrize("n, expected", [
        (10, 1),       # 1 is odd; 0 is even -> product = 1
        (20, 0),       # no odd digits
        (305, 15),     # 3 * 5 = 15
        (101, 1),      # 1 * 1 = 1
    ])
    def test_zero_in_digits(self, n, expected):
        assert digits(n) == expected
