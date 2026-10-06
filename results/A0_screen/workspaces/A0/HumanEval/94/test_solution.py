import pytest
from solution import skjkasdkd


class TestSkjkasdkdBasicExamples:
    """Tests using the examples from the docstring."""

    def test_example_1(self):
        lst = [0, 3, 2, 1, 3, 5, 7, 4, 5, 5, 5, 2, 181, 32, 4, 32, 3, 2, 32, 324, 4, 3]
        assert skjkasdkd(lst) == 10  # largest prime is 181, sum of digits = 1+8+1 = 10

    def test_example_2(self):
        lst = [1, 0, 1, 8, 2, 4597, 2, 1, 3, 40, 1, 2, 1, 2, 4, 2, 5, 1]
        assert skjkasdkd(lst) == 25  # largest prime is 4597, sum of digits = 4+5+9+7 = 25

    def test_example_3(self):
        lst = [1, 3, 1, 32, 5107, 34, 83278, 109, 163, 23, 2323, 32, 30, 1, 9, 3]
        assert skjkasdkd(lst) == 13  # largest prime is 5107, sum of digits = 5+1+0+7 = 13

    def test_example_4(self):
        lst = [0, 724, 32, 71, 99, 32, 6, 0, 5, 91, 83, 0, 5, 6]
        assert skjkasdkd(lst) == 11  # largest prime is 83, sum of digits = 8+3 = 11

    def test_example_5(self):
        lst = [0, 81, 12, 3, 1, 21]
        assert skjkasdkd(lst) == 3  # largest prime is 3, sum of digits = 3

    def test_example_6(self):
        lst = [0, 8, 1, 2, 1, 7]
        assert skjkasdkd(lst) == 7  # largest prime is 7, sum of digits = 7


class TestSkjkasdkdEdgeCases:
    """Tests for edge cases."""

    def test_empty_list(self):
        assert skjkasdkd([]) is None

    def test_no_primes(self):
        lst = [0, 1, 4, 6, 8, 9, 10, 15]
        assert skjkasdkd(lst) is None

    def test_single_element_prime(self):
        assert skjkasdkd([7]) == 7

    def test_single_element_not_prime(self):
        assert skjkasdkd([4]) is None

    def test_all_same_prime(self):
        lst = [5, 5, 5, 5]
        assert skjkasdkd(lst) == 5

    def test_negative_numbers(self):
        lst = [-5, -3, -2, -7]
        assert skjkasdkd(lst) is None

    def test_mixed_negative_and_positive(self):
        lst = [-5, 3, -2, 7]
        assert skjkasdkd(lst) == 7


class TestSkjkasdkdPrimeIdentification:
    """Tests focusing on correct prime identification."""

    def test_smallest_prime(self):
        lst = [0, 1, 2, 4]
        assert skjkasdkd(lst) == 2  # 2 is the smallest prime

    def test_two_digit_prime(self):
        lst = [11]
        assert skjkasdkd(lst) == 2  # 11 -> 1 + 1 = 2

    def test_three_digit_prime(self):
        lst = [101]
        assert skjkasdkd(lst) == 2  # 101 -> 1 + 0 + 1 = 2

    def test_larger_prime(self):
        lst = [997]
        assert skjkasdkd(lst) == 25  # 997 -> 9 + 9 + 7 = 25

    def test_non_prime_large_number(self):
        lst = [100, 101, 102]
        assert skjkasdkd(lst) == 2  # 101 is prime, 100 and 102 are not

    def test_duplicate_largest_prime(self):
        lst = [13, 13, 7, 3]
        assert skjkasdkd(lst) == 4  # 13 is largest prime, 1 + 3 = 4


class TestSkjkasdkdDigitSum:
    """Tests focusing on digit sum calculation."""

    def test_prime_with_zero(self):
        lst = [101]
        assert skjkasdkd(lst) == 2  # 1 + 0 + 1 = 2

    def test_prime_with_many_digits(self):
        lst = [10007]
        assert skjkasdkd(lst) == 8  # 10007 is prime, 1 + 0 + 0 + 0 + 7 = 8

    def test_prime_sum_equals_ten(self):
        lst = [181]
        assert skjkasdkd(lst) == 10  # 1 + 8 + 1 = 10


class TestSkjkasdkdLargestSelection:
    """Tests ensuring the largest prime is selected."""

    def test_multiple_primes_selects_largest(self):
        lst = [2, 3, 5, 7, 11, 13]
        assert skjkasdkd(lst) == 4  # 13 is largest, 1 + 3 = 4

    def test_small_prime_larger_than_big_non_prime(self):
        lst = [2, 100, 1000]
        assert skjkasdkd(lst) == 2  # 2 is the only prime

    def test_medium_prime_vs_small_prime(self):
        lst = [3, 11, 7]
        assert skjkasdkd(lst) == 2  # 11 is largest, 1 + 1 = 2

    def test_largest_is_in_middle_of_list(self):
        lst = [3, 2, 181, 5, 7]
        assert skjkasdkd(lst) == 10  # 181 is largest prime

    def test_largest_at_end(self):
        lst = [3, 2, 5, 7, 181]
        assert skjkasdkd(lst) == 10  # 181 is largest prime

    def test_largest_at_start(self):
        lst = [181, 7, 5, 3, 2]
        assert skjkasdkd(lst) == 10  # 181 is largest prime


class TestSkjkasdkdSpecialPrimes:
    """Tests for special prime values."""

    def test_prime_2(self):
        lst = [2]
        assert skjkasdkd(lst) == 2

    def test_prime_3(self):
        lst = [3]
        assert skjkasdkd(lst) == 3

    def test_prime_11(self):
        lst = [11]
        assert skjkasdkd(lst) == 2

    def test_prime_101(self):
        lst = [101]
        assert skjkasdkd(lst) == 2

    def test_prime_997(self):
        lst = [997]
        assert skjkasdkd(lst) == 25
