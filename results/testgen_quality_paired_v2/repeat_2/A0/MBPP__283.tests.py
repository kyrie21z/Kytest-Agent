import pytest
from solution import validate


# ---------------------------------------------------------------------------
# Positive cases – every digit's frequency is <= the digit itself
# ---------------------------------------------------------------------------

class TestPositiveCases:
    """Inputs where validate() should return True."""

    def test_empty_like_zero(self):
        # Edge case: n == 0; the while-loop body never executes,
        # so no digit is counted and the function returns True.
        assert validate(0) is True

    def test_single_digit_one(self):
        # Digit 1 appears once → 1 <= 1 ✓
        assert validate(1) is True

    def test_single_digit_two(self):
        # Digit 2 appears once → 1 <= 2 ✓
        assert validate(2) is True

    def test_single_digit_nine(self):
        # Digit 9 appears once → 1 <= 9 ✓
        assert validate(9) is True

    def test_two_twos_ok(self):
        # Digit 2 appears twice → 2 <= 2 ✓
        assert validate(22) is True

    def test_three_threes_ok(self):
        # Digit 3 appears three times → 3 <= 3 ✓
        assert validate(333) is True

    def test_four_fours_ok(self):
        # Digit 4 appears four times → 4 <= 4 ✓
        assert validate(4444) is True

    def test_five_fives_ok(self):
        # Digit 5 appears five times → 5 <= 5 ✓
        assert validate(55555) is True

    def test_six_sixes_ok(self):
        # Digit 6 appears six times → 6 <= 6 ✓
        assert validate(666666) is True

    def test_seven_sevens_ok(self):
        # Digit 7 appears seven times → 7 <= 7 ✓
        assert validate(7777777) is True

    def test_eight_eights_ok(self):
        # Digit 8 appears eight times → 8 <= 8 ✓
        assert validate(88888888) is True

    def test_nine_nines_ok(self):
        # Digit 9 appears nine times → 9 <= 9 ✓
        assert validate(999999999) is True

    def test_mixed_digits_valid(self):
        # 1 appears 1 time, 2 appears 2 times, 3 appears 1 time
        # 1<=1, 2<=2, 3<=1 → all OK
        assert validate(1223) is True

    def test_another_mixed_valid(self):
        # 1×1, 2×1, 3×1, 4×1 → all frequencies <= digit
        assert validate(1234) is True

    def test_large_valid_number(self):
        # 1×1, 2×2, 3×3, 4×4, 5×5, 6×6, 7×7, 8×8, 9×9
        num = int("1" + "22" + "333" + "4444" + "55555" + "666666" +
                  "7777777" + "88888888" + "999999999")
        assert validate(num) is True

    def test_single_large_digit(self):
        # Just digit 9 repeated 9 times
        assert validate(int("9" * 9)) is True


# ---------------------------------------------------------------------------
# Negative cases – some digit's frequency exceeds the digit itself
# ---------------------------------------------------------------------------

class TestNegativeCases:
    """Inputs where validate() should return False."""

    def test_digit_zero_present(self):
        # Digit 0 appears → frequency 1 > 0 → False
        assert validate(10) is False

    def test_digit_zero_in_middle(self):
        assert validate(101) is False

    def test_digit_zero_at_end(self):
        assert validate(120) is False

    def test_digit_one_appears_twice(self):
        # Digit 1 appears twice → 2 > 1 → False
        assert validate(11) is False

    def test_digit_one_appears_many_times(self):
        assert validate(11111) is False

    def test_digit_two_appears_thrice(self):
        # Digit 2 appears 3 times → 3 > 2 → False
        assert validate(222) is False

    def test_digit_three_appears_four_times(self):
        # Digit 3 appears 4 times → 4 > 3 → False
        assert validate(3333) is False

    def test_digit_four_appears_five_times(self):
        assert validate(44444) is False

    def test_digit_five_appears_six_times(self):
        assert validate(555555) is False

    def test_digit_six_appears_seven_times(self):
        assert validate(6666666) is False

    def test_digit_seven_appears_eight_times(self):
        assert validate(77777777) is False

    def test_digit_eight_appears_nine_times(self):
        assert validate(888888888) is False

    def test_digit_nine_appears_ten_times(self):
        assert validate(int("9" * 10)) is False

    def test_multiple_violations(self):
        # Digit 1 appears 3 times AND digit 2 appears 3 times
        assert validate(111222) is False

    def test_zero_and_one_both_violate(self):
        assert validate(1010) is False


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Boundary and unusual inputs."""

    def test_single_digit_boundary(self):
        # Each single digit from 0-9
        for d in range(10):
            assert validate(d) is True

    def test_alternating_digits(self):
        # 121212 → digit 1 appears 3 times (3 > 1 → False)
        assert validate(121212) is False

    def test_all_same_digit_small(self):
        # 55555 → digit 5 appears 5 times → 5 <= 5 → True
        assert validate(55555) is True

    def test_all_same_digit_over(self):
        # 555555 → digit 5 appears 6 times → 6 > 5 → False
        assert validate(555555) is False

    def test_max_length_input(self):
        # A very large number with valid frequencies
        # 9 repeated 9 times is valid
        assert validate(int("9" * 9)) is True

    def test_min_nonzero_input(self):
        assert validate(1) is True


# ---------------------------------------------------------------------------
# Property-based style checks
# ---------------------------------------------------------------------------

class TestProperties:
    """Higher-level behavioural properties."""

    def test_no_zero_digit_always_true_if_no_zero(self):
        """Any positive integer without digit 0 and with all other
        digit frequencies within bounds should return True."""
        # Build a number that has exactly d copies of digit d for d=1..9
        digits = []
        for d in range(1, 10):
            digits.extend([str(d)] * d)
        num = int("".join(digits))
        assert validate(num) is True

    def test_any_number_with_zero_returns_false(self):
        """If the integer contains digit 0, validate must return False
        because frequency of 0 (>=1) > 0."""
        for i in range(1, 1000):
            s = str(i)
            if '0' in s:
                assert validate(i) is False, f"Expected False for {i}"

    def test_single_digit_repeated_exactly_digit_plus_one_times(self):
        """Digit d repeated (d+1) times should always return False."""
        for d in range(1, 10):
            num = int(str(d) * (d + 1))
            assert validate(num) is False, f"Expected False for {num}"

    def test_single_digit_repeated_exactly_digit_times(self):
        """Digit d repeated d times should always return True."""
        for d in range(1, 10):
            num = int(str(d) * d)
            assert validate(num) is True, f"Expected True for {num}"
