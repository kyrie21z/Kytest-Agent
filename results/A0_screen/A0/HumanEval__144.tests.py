import pytest
from solution import simplify


class TestSimplifyBasicCases:
    """Test cases from the docstring examples."""

    def test_example_1(self):
        # 1/5 * 5/1 = 5/5 = 1 -> whole number
        assert simplify("1/5", "5/1") is True

    def test_example_2(self):
        # 1/6 * 2/1 = 2/6 = 1/3 -> not a whole number
        assert simplify("1/6", "2/1") is False

    def test_example_3(self):
        # 7/10 * 10/2 = 70/20 = 7/2 = 3.5 -> not a whole number
        assert simplify("7/10", "10/2") is False


class TestSimplifyWholeNumberResults:
    """Tests where the product results in a whole number."""

    def test_identity_multiplication(self):
        # Any fraction * 1/1 = itself; only whole when numerator divides denominator
        assert simplify("2/1", "1/1") is True

    def test_reciprocal_fractions(self):
        # 3/4 * 4/3 = 12/12 = 1 -> whole number
        assert simplify("3/4", "4/3") is True

    def test_integer_multiplication(self):
        # 2/1 * 3/1 = 6/1 = 6 -> whole number
        assert simplify("2/1", "3/1") is True

    def test_same_fraction_squared(self):
        # 2/3 * 2/3 = 4/9 -> not whole
        assert simplify("2/3", "2/3") is False

    def test_fraction_times_itself_can_be_whole(self):
        # 3/2 * 3/2 = 9/4 -> not whole
        assert simplify("3/2", "3/2") is False

    def test_product_equals_one(self):
        # 5/7 * 7/5 = 35/35 = 1 -> whole number
        assert simplify("5/7", "7/5") is True

    def test_large_numbers_whole(self):
        # 100/1 * 1/1 = 100 -> whole number
        assert simplify("100/1", "1/1") is True

    def test_multiple_of_denominator(self):
        # 3/4 * 8/3 = 24/12 = 2 -> whole number
        assert simplify("3/4", "8/3") is True

    def test_another_whole_result(self):
        # 5/2 * 4/5 = 20/10 = 2 -> whole number
        assert simplify("5/2", "4/5") is True

    def test_numerator_divides_evenly(self):
        # 6/3 * 3/2 = 18/6 = 3 -> whole number
        assert simplify("6/3", "3/2") is True


class TestSimplifyNonWholeNumberResults:
    """Tests where the product does NOT result in a whole number."""

    def test_simple_non_whole(self):
        # 1/3 * 1/3 = 1/9 -> not whole
        assert simplify("1/3", "1/3") is False

    def test_prime_denominators(self):
        # 1/2 * 1/3 = 1/6 -> not whole
        assert simplify("1/2", "1/3") is False

    def test_irreducible_result(self):
        # 2/5 * 3/7 = 6/35 -> not whole
        assert simplify("2/5", "3/7") is False

    def test_larger_non_whole(self):
        # 7/8 * 5/6 = 35/48 -> not whole
        assert simplify("7/8", "5/6") is False

    def test_unit_fraction_times_integer(self):
        # 1/4 * 3/1 = 3/4 -> not whole
        assert simplify("1/4", "3/1") is False

    def test_mixed_whole_and_fraction(self):
        # 3/1 * 1/4 = 3/4 -> not whole
        assert simplify("3/1", "1/4") is False


class TestSimplifyEdgeCases:
    """Edge case tests."""

    def test_smallest_fraction(self):
        # 1/1 * 1/1 = 1 -> whole number
        assert simplify("1/1", "1/1") is True

    def test_very_large_numerator(self):
        # 1000/1 * 1/1 = 1000 -> whole number
        assert simplify("1000/1", "1/1") is True

    def test_very_large_denominator(self):
        # 1/1000 * 1000/1 = 1000/1000 = 1 -> whole number
        assert simplify("1/1000", "1000/1") is True

    def test_equal_fractions_product(self):
        # 1/2 * 1/2 = 1/4 -> not whole
        assert simplify("1/2", "1/2") is False

    def test_one_over_one_times_any(self):
        # 1/1 * 5/3 = 5/3 -> not whole
        assert simplify("1/1", "5/3") is False

    def test_any_times_one_over_one(self):
        # 5/3 * 1/1 = 5/3 -> not whole
        assert simplify("5/3", "1/1") is False

    def test_cross_cancellation_whole(self):
        # 4/9 * 9/4 = 36/36 = 1 -> whole number
        assert simplify("4/9", "9/4") is True

    def test_partial_cancellation_not_whole(self):
        # 4/6 * 3/2 = 12/12 = 1 -> whole number
        assert simplify("4/6", "3/2") is True

    def test_no_cancellation(self):
        # 2/3 * 5/7 = 10/21 -> not whole
        assert simplify("2/3", "5/7") is False


class TestSimplifyInputFormat:
    """Tests related to input string format."""

    def test_valid_positive_integers(self):
        # All inputs are positive integers as per spec
        assert simplify("1/1", "1/1") is True

    def test_single_digit_numerators_and_denominators(self):
        assert simplify("3/4", "4/3") is True

    def test_multi_digit_numerators_and_denominators(self):
        assert simplify("12/5", "5/12") is True

    def test_different_length_inputs(self):
        # 1/100 * 100/1 = 100/100 = 1 -> whole number
        assert simplify("1/100", "100/1") is True
