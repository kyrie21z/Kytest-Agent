import pytest
from solution import is_multiply_prime


class TestIsMultiplyPrime:
    """Tests for the is_multiply_prime function."""

    # --- Edge cases and boundary values ---

    def test_zero(self):
        assert is_multiply_prime(0) is False

    def test_one(self):
        assert is_multiply_prime(1) is False

    def test_negative_numbers(self):
        assert is_multiply_prime(-1) is False
        assert is_multiply_prime(-10) is False

    # --- Single prime numbers (should be False — only 1 prime factor) ---

    def test_prime_two(self):
        assert is_multiply_prime(2) is False

    def test_prime_three(self):
        assert is_multiply_prime(3) is False

    def test_prime_five(self):
        assert is_multiply_prime(5) is False

    def test_prime_seven(self):
        assert is_multiply_prime(7) is False

    def test_prime_eleven(self):
        assert is_multiply_prime(11) is False

    # --- Product of two primes (should be False) ---

    def test_two_times_two(self):
        assert is_multiply_prime(4) is False  # 2 * 2

    def test_two_times_three(self):
        assert is_multiply_prime(6) is False  # 2 * 3

    def test_three_times_five(self):
        assert is_multiply_prime(15) is False  # 3 * 5

    def test_two_times_seventeen(self):
        assert is_multiply_prime(34) is False  # 2 * 17

    def test_two_times_thirteen(self):
        assert is_multiply_prime(26) is False  # 2 * 13

    def test_three_times_seventeen(self):
        assert is_multiply_prime(51) is False  # 3 * 17

    def test_five_times_seventeen(self):
        assert is_multiply_prime(85) is False  # 5 * 17

    def test_three_times_thirtyone(self):
        assert is_multiply_prime(93) is False  # 3 * 31

    def test_two_times_fortynine(self):
        assert is_multiply_prime(94) is False  # 2 * 47

    def test_five_times_nineteen(self):
        assert is_multiply_prime(95) is False  # 5 * 19

    def test_seven_times_thirteen(self):
        assert is_multiply_prime(91) is False  # 7 * 13

    def test_two_times_thirtyseven(self):
        assert is_multiply_prime(74) is False  # 2 * 37

    def test_two_times_fortyone(self):
        assert is_multiply_prime(82) is False  # 2 * 41

    def test_three_times_twentythree(self):
        assert is_multiply_prime(69) is False  # 3 * 23

    def test_five_times_thirteen(self):
        assert is_multiply_prime(65) is False  # 5 * 13

    def test_two_times_eleven(self):
        assert is_multiply_prime(22) is False  # 2 * 11

    def test_three_times_seven(self):
        assert is_multiply_prime(21) is False  # 3 * 7

    def test_two_times_seven(self):
        assert is_multiply_prime(14) is False  # 2 * 7

    def test_two_times_five(self):
        assert is_multiply_prime(10) is False  # 2 * 5

    def test_three_times_three(self):
        assert is_multiply_prime(9) is False  # 3 * 3

    def test_five_times_five(self):
        assert is_multiply_prime(25) is False  # 5 * 5

    def test_seven_times_seven(self):
        assert is_multiply_prime(49) is False  # 7 * 7

    # --- Product of three primes (should be True) ---

    def test_example_30(self):
        assert is_multiply_prime(30) is True  # 2 * 3 * 5

    def test_eight(self):
        assert is_multiply_prime(8) is True  # 2 * 2 * 2

    def test_twelve(self):
        assert is_multiply_prime(12) is True  # 2 * 2 * 3

    def test_fortytwo(self):
        assert is_multiply_prime(42) is True  # 2 * 3 * 7

    def test_onehundredfive(self):
        assert is_multiply_prime(105) is True  # 3 * 5 * 7

    def test_two_times_two_times_three(self):
        assert is_multiply_prime(12) is True  # 2 * 2 * 3

    def test_two_times_two_times_five(self):
        assert is_multiply_prime(20) is True  # 2 * 2 * 5

    def test_two_times_two_times_seven(self):
        assert is_multiply_prime(28) is True  # 2 * 2 * 7

    def test_two_times_three_times_three(self):
        assert is_multiply_prime(18) is True  # 2 * 3 * 3

    def test_three_times_three_times_three(self):
        assert is_multiply_prime(27) is True  # 3 * 3 * 3

    def test_two_times_three_times_five(self):
        assert is_multiply_prime(30) is True  # 2 * 3 * 5

    def test_two_times_three_times_seven(self):
        assert is_multiply_prime(42) is True  # 2 * 3 * 7

    def test_two_times_three_times_eleven(self):
        assert is_multiply_prime(66) is True  # 2 * 3 * 11

    def test_two_times_three_times_thirteen(self):
        assert is_multiply_prime(78) is True  # 2 * 3 * 13

    def test_two_times_five_times_seven(self):
        assert is_multiply_prime(70) is True  # 2 * 5 * 7

    def test_three_times_five_times_seven(self):
        assert is_multiply_prime(105) is True  # 3 * 5 * 7

    def test_two_times_two_times_thirteen(self):
        assert is_multiply_prime(52) is True  # 2 * 2 * 13

    def test_two_times_two_times_nineteen(self):
        assert is_multiply_prime(76) is True  # 2 * 2 * 19

    def test_two_times_two_times_twentythree(self):
        assert is_multiply_prime(92) is True  # 2 * 2 * 23

    def test_three_times_three_times_three(self):
        assert is_multiply_prime(27) is True  # 3 * 3 * 3

    def test_three_times_three_times_five(self):
        assert is_multiply_prime(45) is True  # 3 * 3 * 5

    def test_three_times_three_times_seven(self):
        assert is_multiply_prime(63) is True  # 3 * 3 * 7

    def test_three_times_three_times_eleven(self):
        assert is_multiply_prime(99) is True  # 3 * 3 * 11

    def test_two_times_five_times_five(self):
        assert is_multiply_prime(50) is True  # 2 * 5 * 5

    def test_three_times_five_times_five(self):
        assert is_multiply_prime(75) is True  # 3 * 5 * 5

    def test_two_times_seven_times_seven(self):
        assert is_multiply_prime(98) is True  # 2 * 7 * 7

    # --- Product of four or more primes (should be False) ---

    def test_four_primes_two_times_two_times_two_times_two(self):
        assert is_multiply_prime(16) is False  # 2 * 2 * 2 * 2

    def test_four_primes_two_times_two_times_two_times_three(self):
        assert is_multiply_prime(24) is False  # 2 * 2 * 2 * 3

    def test_four_primes_two_times_two_times_three_times_three(self):
        assert is_multiply_prime(36) is False  # 2 * 2 * 3 * 3

    def test_four_primes_two_times_two_times_two_times_five(self):
        assert is_multiply_prime(40) is False  # 2 * 2 * 2 * 5

    def test_four_primes_two_times_two_times_three_times_five(self):
        assert is_multiply_prime(60) is False  # 2 * 2 * 3 * 5

    def test_four_primes_two_times_three_times_five_times_seven(self):
        assert is_multiply_prime(210) is False  # 2 * 3 * 5 * 7

    def test_six_primes_two_to_the_sixth(self):
        assert is_multiply_prime(64) is False  # 2^6

    def test_five_primes_two_times_two_times_two_times_two_times_three(self):
        assert is_multiply_prime(48) is False  # 2 * 2 * 2 * 2 * 3

    def test_five_primes_two_times_two_times_two_times_three_times_three(self):
        assert is_multiply_prime(72) is False  # 2 * 2 * 2 * 3 * 3

    def test_four_primes_two_times_three_times_three_times_three(self):
        assert is_multiply_prime(54) is False  # 2 * 3 * 3 * 3

    def test_four_primes_two_times_two_times_two_times_two_times_two(self):
        assert is_multiply_prime(32) is False  # 2^5

    def test_four_primes_two_times_two_times_three_times_seven(self):
        assert is_multiply_prime(84) is False  # 2 * 2 * 3 * 7

    def test_four_primes_two_times_two_times_two_times_eleven(self):
        assert is_multiply_prime(88) is False  # 2 * 2 * 2 * 11

    def test_four_primes_three_times_three_times_three_times_three(self):
        assert is_multiply_prime(81) is False  # 3^4

    def test_four_primes_two_times_three_times_three_times_five(self):
        assert is_multiply_prime(90) is False  # 2 * 3 * 3 * 5

    def test_four_primes_two_times_two_times_two_times_two_times_three(self):
        assert is_multiply_prime(96) is False  # 2^5 * 3

    # --- Boundary at max value (a < 100 per docstring) ---

    def test_boundary_values_comprehensive(self):
        """Test every number from 2 to 99 systematically."""
        for a in range(2, 100):
            result = is_multiply_prime(a)
            # Count prime factors with multiplicity
            n = a
            count = 0
            d = 2
            while d * d <= n:
                while n % d == 0:
                    count += 1
                    n //= d
                d += 1
            if n > 1:
                count += 1
            expected = count == 3
            assert result == expected, f"is_multiply_prime({a}) returned {result}, expected {expected} ({count} prime factors)"
