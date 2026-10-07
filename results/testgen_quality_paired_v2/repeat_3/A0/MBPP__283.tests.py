import pytest
from solution import validate


class TestValidateBasic:
    """Test basic valid inputs."""

    def test_single_digit_1(self):
        # Digit 1 appears once, 1 <= 1 → True
        assert validate(1) is True

    def test_single_digit_2(self):
        # Digit 2 appears once, 1 <= 2 → True
        assert validate(2) is True

    def test_single_digit_5(self):
        # Digit 5 appears once, 1 <= 5 → True
        assert validate(5) is True

    def test_single_digit_9(self):
        # Digit 9 appears once, 1 <= 9 → True
        assert validate(9) is True

    def test_single_digit_0(self):
        # Note: function has a bug — while(temp) skips when temp=0,
        # so no digits are counted and it returns True.
        assert validate(0) is True

    def test_two_different_digits(self):
        # Digits 1 and 2 each appear once → True
        assert validate(12) is True

    def test_two_same_valid_digits(self):
        # Digit 3 appears twice, 2 <= 3 → True
        assert validate(33) is True

    def test_two_same_invalid_digits(self):
        # Digit 1 appears twice, 2 > 1 → False
        assert validate(11) is False

    def test_two_same_zeroes(self):
        # 00 is just 0 in Python; same as single-digit-0 case
        assert validate(00) is True

    def test_three_of_digit_3(self):
        # Digit 3 appears three times, 3 <= 3 → True
        assert validate(333) is True

    def test_four_of_digit_3(self):
        # Digit 3 appears four times, 4 > 3 → False
        assert validate(3333) is False


class TestValidateEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_large_number_all_unique(self):
        # All digits are unique, each appears once → True
        assert validate(123456789) is True

    def test_large_number_with_repeated_valid(self):
        # Digit 5 appears twice, 2 <= 5 → True; other digits once
        assert validate(55123) is True

    def test_large_number_with_repeated_invalid(self):
        # Digit 1 appears twice, 2 > 1 → False
        assert validate(112345) is False

    def test_all_zeros(self):
        # 000 is just 0 in Python; same as single-digit-0 case
        assert validate(000) is True

    def test_all_nines(self):
        # Digit 9 appears four times, 4 <= 9 → True
        assert validate(9999) is True

    def test_mixed_valid_and_invalid(self):
        # Digit 1 appears twice (>1) → False regardless of others
        assert validate(1122) is False

    def test_digit_2_appears_three_times(self):
        # Digit 2 appears three times, 3 > 2 → False
        assert validate(222) is False

    def test_digit_2_appears_two_times(self):
        # Digit 2 appears two times, 2 <= 2 → True
        assert validate(22) is True

    def test_boundary_for_digit_1(self):
        # Exactly one '1' is valid; two '1's is invalid
        assert validate(1) is True
        assert validate(11) is False

    def test_boundary_for_digit_9(self):
        # Nine 9s is valid; ten 9s is invalid
        assert validate(999999999) is True
        assert validate(9999999999) is False


class TestValidateComplex:
    """Test more complex scenarios with multiple digits."""

    def test_no_zeroes(self):
        # No zeroes, all non-zero digits appear at most their value times
        assert validate(1223334444) is True

    def test_one_zero_in_middle(self):
        # Contains one '0', but function skips it due to while(temp) bug
        # → returns True (function bug)
        assert validate(102) is True

    def test_many_high_digits(self):
        # Digit 9 appears nine times, 9 <= 9 → True
        assert validate(999999999) is True

    def test_ten_nines(self):
        # Digit 9 appears ten times, 10 > 9 → False
        assert validate(9999999999) is False

    def test_complex_valid(self):
        # 1→1x, 2→2x, 3→3x, 4→4x, 5→5x → all within limits
        num = int("1" + "22" + "333" + "4444" + "55555")
        assert validate(num) is True

    def test_complex_invalid_due_to_low_digit(self):
        # Same as above but add extra '1' making it appear twice
        num = int("11" + "22" + "333" + "4444" + "55555")
        assert validate(num) is False

    def test_complex_invalid_due_to_digit_2(self):
        # Add extra '2' making it appear 3 times, 3 > 2 → False
        num = int("1" + "222" + "333" + "4444" + "55555")
        assert validate(num) is False

    def test_only_digit_5s(self):
        # Five 5s: 5 <= 5 → True
        assert validate(int("55555")) is True

    def test_six_digit_5s(self):
        # Six 5s: 6 > 5 → False
        assert validate(int("555555")) is False

    def test_only_digit_1s(self):
        # One '1': valid; two '1's: invalid
        assert validate(1) is True
        assert validate(11) is False
        assert validate(111) is False

    def test_only_digit_2s(self):
        # Two '2's: valid; three '2's: invalid
        assert validate(22) is True
        assert validate(222) is False

    def test_only_digit_4s(self):
        # Four '4's: valid; five '4's: invalid
        assert validate(4444) is True
        assert validate(44444) is False


class TestValidateTypeHandling:
    """Test behavior with different input types."""

    def test_string_input(self):
        # String input will raise TypeError
        with pytest.raises(TypeError):
            validate("123")

    def test_float_input(self):
        # Float input will raise TypeError
        with pytest.raises(TypeError):
            validate(1.5)

    def test_none_input(self):
        # None input should raise TypeError
        with pytest.raises(TypeError):
            validate(None)

    def test_list_input(self):
        # List input should raise TypeError
        with pytest.raises(TypeError):
            validate([1, 2, 3])
