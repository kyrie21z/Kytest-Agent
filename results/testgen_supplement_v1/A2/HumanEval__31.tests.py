"""Unit tests for is_prime() in solution.py."""

import pytest
from solution import is_prime


# ---------------------------------------------------------------------------
# Normal / typical inputs – positive integers that are clearly prime or composite
# ---------------------------------------------------------------------------

class TestIsPrimeNormalCases:
    """Tests with well-known prime and composite numbers."""

    # --- Primes ----------------------------------------------------------
    def test_prime_2(self):
        assert is_prime(2) is True

    def test_prime_3(self):
        assert is_prime(3) is True

    def test_prime_5(self):
        assert is_prime(5) is True

    def test_prime_7(self):
        assert is_prime(7) is True

    def test_prime_11(self):
        assert is_prime(11) is True

    def test_prime_61(self):
        assert is_prime(61) is True

    def test_prime_101(self):
        assert is_prime(101) is True

    def test_prime_13441(self):
        assert is_prime(13441) is True

    def test_large_prime_999983(self):
        assert is_prime(999983) is True

    def test_large_prime_1000000007(self):
        assert is_prime(1000000007) is True

    # --- Composites ------------------------------------------------------
    def test_composite_4(self):
        assert is_prime(4) is False

    def test_composite_6(self):
        assert is_prime(6) is False

    def test_composite_9(self):
        assert is_prime(9) is False

    def test_composite_10(self):
        assert is_prime(10) is False

    def test_composite_100(self):
        assert is_prime(100) is False

    def test_composite_even_large(self):
        assert is_prime(1000) is False

    def test_composite_odd_large(self):
        assert is_prime(999999) is False

    def test_square_of_prime(self):
        assert is_prime(49) is False   # 7^2

    def test_product_of_two_primes(self):
        assert is_prime(15) is False   # 3 * 5


# ---------------------------------------------------------------------------
# Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------

class TestIsPrimeBoundaryCases:
    """Tests at the boundaries of the input domain."""

    def test_zero(self):
        assert is_prime(0) is False

    def test_one(self):
        assert is_prime(1) is False

    def test_two_smallest_prime(self):
        assert is_prime(2) is True

    def test_three_smallest_odd_prime(self):
        assert is_prime(3) is True

    def test_negative_one(self):
        assert is_prime(-1) is False

    def test_negative_five(self):
        assert is_prime(-5) is False

    def test_negative_large(self):
        assert is_prime(-100) is False


# ---------------------------------------------------------------------------
# Edge cases – powers of two, perfect squares, twin primes, etc.
# ---------------------------------------------------------------------------

class TestIsPrimeEdgeCases:
    """Additional edge-case scenarios."""

    def test_power_of_two_4(self):
        assert is_prime(4) is False

    def test_power_of_two_8(self):
        assert is_prime(8) is False

    def test_power_of_two_16(self):
        assert is_prime(16) is False

    def test_twin_prime_pair_11_and_13(self):
        assert is_prime(11) is True
        assert is_prime(13) is True

    def test_perfect_cube_27(self):
        assert is_prime(27) is False

    def test_perfect_cube_8(self):
        assert is_prime(8) is False

    def test_fermat_prime_17(self):
        assert is_prime(17) is True

    def test_mersenne_prime_127(self):
        assert is_prime(127) is True

    def test_palindrome_prime_11(self):
        assert is_prime(11) is True

    def test_palindrome_composite_22(self):
        assert is_prime(22) is False


# ---------------------------------------------------------------------------
# Invalid / unexpected input types – the function does not guard against
# non-numeric types, so we verify what actually happens.
# ---------------------------------------------------------------------------

class TestIsPrimeInvalidInputs:
    """Tests with inputs outside the documented integer domain."""

    def test_none_raises(self):
        with pytest.raises(TypeError):
            is_prime(None)

    def test_string_raises(self):
        with pytest.raises(TypeError):
            is_prime("6")

    def test_list_raises(self):
        with pytest.raises(TypeError):
            is_prime([2])

    def test_empty_string_raises(self):
        with pytest.raises(TypeError):
            is_prime("")

    def test_dict_raises(self):
        with pytest.raises(TypeError):
            is_prime({})

    def test_tuple_raises(self):
        with pytest.raises(TypeError):
            is_prime((2,))

    def test_float_whole_number_returns_false_for_6(self):
        # Floats like 6.0 work via Python's numeric coercion; 6.0 is composite.
        assert is_prime(6.0) is False

    def test_float_whole_number_returns_true_for_7(self):
        # 7.0 is prime.
        assert is_prime(7.0) is True


# ---------------------------------------------------------------------------
# Docstring doctest examples (re-asserted here for completeness)
# ---------------------------------------------------------------------------

class TestIsPrimeDocstringExamples:
    """Re-check every example from the docstring."""

    def test_docstring_6(self):
        assert is_prime(6) is False

    def test_docstring_101(self):
        assert is_prime(101) is True

    def test_docstring_11(self):
        assert is_prime(11) is True

    def test_docstring_13441(self):
        assert is_prime(13441) is True

    def test_docstring_61(self):
        assert is_prime(61) is True

    def test_docstring_4(self):
        assert is_prime(4) is False

    def test_docstring_1(self):
        assert is_prime(1) is False
