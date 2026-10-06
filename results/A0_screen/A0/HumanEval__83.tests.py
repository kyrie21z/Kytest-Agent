import pytest
from solution import starts_one_ends


class TestStartsOneEnds:
    """Tests for the starts_one_ends function."""

    # --- Basic / Known Values ---

    def test_n_1(self):
        """n=1: only the number '1' qualifies."""
        assert starts_one_ends(1) == 1

    def test_n_2(self):
        """n=2: 18 two-digit numbers start or end with 1."""
        assert starts_one_ends(2) == 18

    def test_n_3(self):
        """n=3: 180 three-digit numbers start or end with 1."""
        assert starts_one_ends(3) == 180

    def test_n_4(self):
        """n=4: 1800 four-digit numbers start or end with 1."""
        assert starts_one_ends(4) == 1800

    def test_n_5(self):
        """n=5: 18000 five-digit numbers start or end with 1."""
        assert starts_one_ends(5) == 18000

    # --- Larger / Edge Cases ---

    def test_n_10(self):
        """n=10: large value to verify exponential growth."""
        assert starts_one_ends(10) == 18 * 10 ** 8

    def test_n_15(self):
        """n=15: very large value."""
        assert starts_one_ends(15) == 18 * 10 ** 13

    # --- Input Validation ---

    def test_n_zero_returns_non_positive(self):
        """n=0 is not a valid positive integer; result should not be a valid count."""
        result = starts_one_ends(0)
        assert result <= 0 or not isinstance(result, int)

    def test_n_negative_returns_non_positive(self):
        """Negative n is invalid; result should not be a valid count."""
        result = starts_one_ends(-1)
        assert result <= 0 or not isinstance(result, int)

    def test_n_non_integer_returns_float(self):
        """Non-integer input produces a float result, not an integer count."""
        result = starts_one_ends(2.5)
        assert isinstance(result, float)

    def test_n_string_raises(self):
        """String input should raise an error."""
        with pytest.raises(Exception):
            starts_one_ends("5")

    # --- Type Checks ---

    def test_returns_int_for_valid_input(self):
        """Result should be an integer for valid positive integer n."""
        result = starts_one_ends(3)
        assert isinstance(result, int)

    def test_positive_result(self):
        """Result should always be positive for valid n."""
        for n in range(1, 10):
            assert starts_one_ends(n) > 0

    # --- Monotonicity ---

    def test_increasing_with_n(self):
        """Count should increase as n increases."""
        prev = None
        for n in range(1, 10):
            val = starts_one_ends(n)
            if prev is not None:
                assert val > prev
            prev = val
