"""Unit tests for solution.largest_prime_factor."""

import pytest
from solution import largest_prime_factor


class TestNormalCases:
    """Tests with typical valid inputs as documented in the docstring."""

    def test_docstring_example_1(self):
        """largest_prime_factor(13195) == 29 per docstring."""
        # 13195 = 5 * 7 * 13 * 29
        assert largest_prime_factor(13195) == 29

    def test_docstring_example_2(self):
        """largest_prime_factor(2048) == 2 per docstring."""
        # 2048 = 2^11, only prime factor is 2
        assert largest_prime_factor(2048) == 2

    def test_small_composite(self):
        """6 = 2 * 3, largest prime factor is 3."""
        assert largest_prime_factor(6) == 3

    def test_another_small_composite(self):
        """10 = 2 * 5, largest prime factor is 5."""
        assert largest_prime_factor(10) == 5

    def test_product_of_two_primes(self):
        """15 = 3 * 5, largest prime factor is 5."""
        assert largest_prime_factor(15) == 5

    def test_power_of_a_prime(self):
        """8 = 2^3, largest prime factor is 2."""
        assert largest_prime_factor(8) == 2

    def test_larger_composite(self):
        """30 = 2 * 3 * 5, largest prime factor is 5."""
        assert largest_prime_factor(30) == 5

    def test_even_number_with_large_prime(self):
        """22 = 2 * 11, largest prime factor is 11."""
        assert largest_prime_factor(22) == 11

    def test_odd_composite(self):
        """21 = 3 * 7, largest prime factor is 7."""
        assert largest_prime_factor(21) == 7

    def test_square_of_prime(self):
        """49 = 7^2, largest prime factor is 7."""
        assert largest_prime_factor(49) == 7

    def test_cube_of_prime(self):
        """27 = 3^3, largest prime factor is 3."""
        assert largest_prime_factor(27) == 3

    def test_multiple_distinct_primes(self):
        """2 * 3 * 7 = 42, largest prime factor is 7."""
        assert largest_prime_factor(42) == 7

    def test_larger_example(self):
        """100 = 2^2 * 5^2, largest prime factor is 5."""
        assert largest_prime_factor(100) == 5

    def test_very_large_input(self):
        """999999940 = 2^2 * 5 * 49999997, largest prime factor is 49999997."""
        assert largest_prime_factor(999999940) == 49999997


class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_min_valid_n_per_docstring(self):
        """Smallest composite number: 4 = 2^2, largest prime factor is 2."""
        assert largest_prime_factor(4) == 2

    def test_n_equals_9(self):
        """9 = 3^2, largest prime factor is 3."""
        assert largest_prime_factor(9) == 3

    def test_n_equals_12(self):
        """12 = 2^2 * 3, largest prime factor is 3."""
        assert largest_prime_factor(12) == 3

    def test_n_equals_14(self):
        """14 = 2 * 7, largest prime factor is 7."""
        assert largest_prime_factor(14) == 7

    def test_n_equals_16(self):
        """16 = 2^4, largest prime factor is 2."""
        assert largest_prime_factor(16) == 2

    def test_n_equals_18(self):
        """18 = 2 * 3^2, largest prime factor is 3."""
        assert largest_prime_factor(18) == 3

    def test_n_equals_25(self):
        """25 = 5^2, largest prime factor is 5."""
        assert largest_prime_factor(25) == 5

    def test_n_equals_1000(self):
        """1000 = 2^3 * 5^3, largest prime factor is 5."""
        assert largest_prime_factor(1000) == 5

    def test_n_equals_10000(self):
        """10000 = 2^4 * 5^4, largest prime factor is 5."""
        assert largest_prime_factor(10000) == 5


class TestEmptyNullZeroSizeInputs:
    """Tests for edge cases with zero, one, or invalid sizes."""

    def test_n_equals_1(self):
        """n=1: no prime factors exist; function has no explicit return path."""
        # The sieve creates [True]*2, loops find nothing, falls off end -> None
        assert largest_prime_factor(1) is None

    def test_n_equals_0(self):
        """n=0: sieve size 1, no primes found, returns None."""
        assert largest_prime_factor(0) is None

    def test_negative_n(self):
        """Negative n: sieve creation with negative index causes error."""
        # Creating [True] * (-5 + 1) = [True] * -4 raises ValueError
        with pytest.raises(ValueError):
            largest_prime_factor(-5)


class TestInvalidInputs:
    """Tests for inputs outside the documented constraints."""

    def test_non_integer_string(self):
        """Passing a string instead of int should raise TypeError."""
        with pytest.raises(TypeError):
            largest_prime_factor("10")

    def test_none_input(self):
        """Passing None should raise TypeError."""
        with pytest.raises(TypeError):
            largest_prime_factor(None)

    def test_float_input(self):
        """Passing a float should raise TypeError."""
        with pytest.raises(TypeError):
            largest_prime_factor(10.5)


class TestPrimeInputs:
    """Tests where n itself is prime (violates docstring assumption)."""

    def test_prime_2(self):
        """n=2 is prime. No prime < 2 divides 2, so returns None."""
        assert largest_prime_factor(2) is None

    def test_prime_3(self):
        """n=3 is prime. Returns None."""
        assert largest_prime_factor(3) is None

    def test_prime_7(self):
        """n=7 is prime. Returns None."""
        assert largest_prime_factor(7) is None

    def test_prime_13(self):
        """n=13 is prime. Returns None."""
        assert largest_prime_factor(13) is None

    def test_prime_97(self):
        """n=97 is prime. Returns None."""
        assert largest_prime_factor(97) is None


class TestReturnValueType:
    """Verify return type is always int when a result exists."""

    def test_return_type_int(self):
        """Result should be an int."""
        result = largest_prime_factor(13195)
        assert isinstance(result, int)

    def test_return_type_int_for_all_cases(self):
        """All non-None results should be ints."""
        for n in [4, 6, 8, 10, 15, 21, 22, 25, 27, 30, 42, 49, 100]:
            result = largest_prime_factor(n)
            assert isinstance(result, int), f"Expected int for n={n}, got {type(result)}"
