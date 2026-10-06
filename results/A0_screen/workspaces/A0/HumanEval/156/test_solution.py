import pytest
from solution import int_to_mini_roman


class TestIntToMiniRoman:
    """Unit tests for the int_to_mini_roman function."""

    # --- Boundary values ---

    def test_one(self):
        assert int_to_mini_roman(1) == "i"

    def test_nine(self):
        assert int_to_mini_roman(9) == "ix"

    def test_ten(self):
        assert int_to_mini_roman(10) == "x"

    def test_forty(self):
        assert int_to_mini_roman(40) == "xl"

    def test_fifty(self):
        assert int_to_mini_roman(50) == "l"

    def test_ninety(self):
        assert int_to_mini_roman(90) == "xc"

    def test_hundred(self):
        assert int_to_mini_roman(100) == "c"

    def test_four_hundred(self):
        assert int_to_mini_roman(400) == "cd"

    def test_five_hundred(self):
        assert int_to_mini_roman(500) == "d"

    def test_nine_hundred(self):
        assert int_to_mini_roman(900) == "cm"

    def test_thousand(self):
        assert int_to_mini_roman(1000) == "m"

    # --- Examples from docstring ---

    def test_example_19(self):
        assert int_to_mini_roman(19) == "xix"

    def test_example_152(self):
        assert int_to_mini_roman(152) == "clii"

    def test_example_426(self):
        assert int_to_mini_roman(426) == "cdxxvi"

    # --- Single-digit numbers ---

    @pytest.mark.parametrize("number, expected", [
        (1, "i"),
        (2, "ii"),
        (3, "iii"),
        (4, "iv"),
        (5, "v"),
        (6, "vi"),
        (7, "vii"),
        (8, "viii"),
        (9, "ix"),
    ])
    def test_single_digits(self, number, expected):
        assert int_to_mini_roman(number) == expected

    # --- Tens ---

    @pytest.mark.parametrize("number, expected", [
        (10, "x"),
        (20, "xx"),
        (30, "xxx"),
        (40, "xl"),
        (50, "l"),
        (60, "lx"),
        (70, "lxx"),
        (80, "lxxx"),
        (90, "xc"),
    ])
    def test_tens(self, number, expected):
        assert int_to_mini_roman(number) == expected

    # --- Hundreds ---

    @pytest.mark.parametrize("number, expected", [
        (100, "c"),
        (200, "cc"),
        (300, "ccc"),
        (400, "cd"),
        (500, "d"),
        (600, "dc"),
        (700, "dcc"),
        (800, "dccc"),
        (900, "cm"),
    ])
    def test_hundreds(self, number, expected):
        assert int_to_mini_roman(number) == expected

    # --- Combined / mixed values ---

    @pytest.mark.parametrize("number, expected", [
        (11, "xi"),
        (12, "xii"),
        (13, "xiii"),
        (14, "xiv"),
        (15, "xv"),
        (21, "xxi"),
        (31, "xxxi"),
        (41, "xli"),
        (51, "li"),
        (91, "xci"),
        (101, "ci"),
        (111, "cxi"),
        (199, "cxcix"),
        (200, "cc"),
        (250, "ccl"),
        (300, "ccc"),
        (350, "cccl"),
        (499, "cdxcix"),
        (500, "d"),
        (501, "di"),
        (600, "dc"),
        (700, "dcc"),
        (800, "dccc"),
        (900, "cm"),
        (999, "cmxcix"),
    ])
    def test_combined_values(self, number, expected):
        assert int_to_mini_roman(number) == expected

    # --- Output is always lowercase ---

    def test_output_is_lowercase(self):
        for n in range(1, 1001):
            result = int_to_mini_roman(n)
            assert result == result.lower(), f"{n} produced non-lowercase: {result}"

    # --- Invalid inputs: out-of-range behavior ---

    def test_zero_returns_empty_string(self):
        assert int_to_mini_roman(0) == ""

    def test_negative_returns_unexpected_result(self):
        # Negative numbers use Python's negative list indexing, producing
        # a seemingly random roman numeral; we just check it's not empty.
        result = int_to_mini_roman(-1)
        assert isinstance(result, str) and len(result) > 0

    def test_over_thousand_returns_m(self):
        # 1001 // 1000 = 1, so thousands = "m"; rest is "i" -> "mi"
        assert int_to_mini_roman(1001) == "mi"
