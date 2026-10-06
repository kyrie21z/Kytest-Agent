import pytest
from solution import valid_date


class TestValidDateBasicFormat:
    """Tests for basic date format validation (mm-dd-yyyy)."""

    def test_valid_standard_date(self):
        assert valid_date('03-11-2000') is True

    def test_valid_another_date(self):
        assert valid_date('06-04-2020') is True

    def test_invalid_wrong_separator_slash(self):
        assert valid_date('06/04/2020') is False

    def test_invalid_wrong_separator_dash_in_year(self):
        assert valid_date('06-04-20-20') is False

    def test_invalid_no_separator(self):
        assert valid_date('06042020') is False

    def test_invalid_mixed_separators(self):
        assert valid_date('06-04/2020') is False

    def test_invalid_wrong_length_short(self):
        assert valid_date('1-1-2000') is False

    def test_invalid_wrong_length_long(self):
        assert valid_date('001-01-2000') is False

    def test_empty_string(self):
        assert valid_date('') is False

    def test_only_whitespace(self):
        assert valid_date('   ') is False

    def test_none_input_raises_error(self):
        with pytest.raises(TypeError):
            valid_date(None)


class TestValidDateMonthRange:
    """Tests for month range validation (1-12)."""

    def test_valid_month_one(self):
        assert valid_date('01-15-2020') is True

    def test_valid_month_twelve(self):
        assert valid_date('12-31-2020') is True

    def test_invalid_month_zero(self):
        assert valid_date('00-15-2020') is False

    def test_invalid_month_thirteen(self):
        assert valid_date('13-15-2020') is False

    def test_invalid_month_negative_as_string(self):
        assert valid_date('-1-15-2020') is False

    def test_invalid_month_too_large(self):
        assert valid_date('99-15-2020') is False


class TestValidDateDayRange:
    """Tests for day range validation based on month."""

    # Months with 31 days: 1, 3, 5, 7, 8, 10, 12
    def test_january_31_days(self):
        assert valid_date('01-31-2020') is True

    def test_january_32_days_invalid(self):
        assert valid_date('01-32-2020') is False

    def test_march_31_days(self):
        assert valid_date('03-31-2020') is True

    def test_may_31_days(self):
        assert valid_date('05-31-2020') is True

    def test_july_31_days(self):
        assert valid_date('07-31-2020') is True

    def test_august_31_days(self):
        assert valid_date('08-31-2020') is True

    def test_october_31_days(self):
        assert valid_date('10-31-2020') is True

    def test_december_31_days(self):
        assert valid_date('12-31-2020') is True

    # Months with 30 days: 4, 6, 9, 11
    def test_april_30_days(self):
        assert valid_date('04-30-2020') is True

    def test_april_31_days_invalid(self):
        assert valid_date('04-31-2020') is False

    def test_june_30_days(self):
        assert valid_date('06-30-2020') is True

    def test_june_31_days_invalid(self):
        assert valid_date('06-31-2020') is False

    def test_september_30_days(self):
        assert valid_date('09-30-2020') is True

    def test_september_31_days_invalid(self):
        assert valid_date('09-31-2020') is False

    def test_november_30_days(self):
        assert valid_date('11-30-2020') is True

    def test_november_31_days_invalid(self):
        assert valid_date('11-31-2020') is False

    # February: max 29 days
    def test_february_29_days(self):
        assert valid_date('02-29-2020') is True

    def test_february_28_days(self):
        assert valid_date('02-28-2020') is True

    def test_february_30_days_invalid(self):
        assert valid_date('02-30-2020') is False

    def test_february_31_days_invalid(self):
        assert valid_date('02-31-2020') is False


class TestValidDateDayMinimum:
    """Tests for minimum day validation (day >= 1)."""

    def test_day_zero_invalid(self):
        assert valid_date('04-0-2040') is False

    def test_day_negative_invalid(self):
        assert valid_date('04--1-2040') is False

    def test_first_day_valid(self):
        assert valid_date('01-01-2020') is True


class TestValidDateYear:
    """Tests for year field handling."""

    def test_leap_year_feb_29(self):
        assert valid_date('02-29-2020') is True

    def test_non_leap_year_feb_29_still_valid(self):
        # The function allows up to 29 days for Feb regardless of leap year
        assert valid_date('02-29-2019') is True

    def test_valid_year_four_digits(self):
        assert valid_date('01-01-1999') is True

    def test_valid_year_two_digits(self):
        assert valid_date('01-01-99') is False

    def test_valid_year_zero(self):
        assert valid_date('01-01-0000') is True


class TestValidDateNonDigitCharacters:
    """Tests for non-digit character rejection."""

    def test_alpha_in_month(self):
        assert valid_date('ab-01-2020') is False

    def test_alpha_in_day(self):
        assert valid_date('01-ab-2020') is False

    def test_alpha_in_year(self):
        assert valid_date('01-01-abcd') is False

    def test_special_chars(self):
        assert valid_date('01-01-20!0') is False

    def test_spaces_in_date(self):
        assert valid_date('01 01 2020') is False


class TestValidDateEdgeCases:
    """Edge case and boundary tests."""

    def test_single_digit_month_with_leading_zero(self):
        assert valid_date('01-15-2020') is True

    def test_single_digit_day_with_leading_zero(self):
        assert valid_date('01-01-2020') is True

    def test_max_valid_date(self):
        assert valid_date('12-31-9999') is True

    def test_min_valid_date(self):
        assert valid_date('01-01-0000') is True

    def test_example_from_docstring_1(self):
        assert valid_date('03-11-2000') is True

    def test_example_from_docstring_2(self):
        assert valid_date('15-01-2012') is False

    def test_example_from_docstring_3(self):
        assert valid_date('04-0-2040') is False

    def test_example_from_docstring_4(self):
        assert valid_date('06-04-2020') is True

    def test_example_from_docstring_5(self):
        assert valid_date('06/04/2020') is False
