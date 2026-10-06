import pytest
from solution import greatest_common_divisor


# ---------------------------------------------------------------------------
# 1. Normal / typical inputs
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Typical positive integer pairs."""

    def test_coprime_3_5(self):
        assert greatest_common_divisor(3, 5) == 1

    def test_coprime_7_13(self):
        assert greatest_common_divisor(7, 13) == 1

    def test_shared_factor_25_15(self):
        assert greatest_common_divisor(25, 15) == 5

    def test_shared_factor_12_8(self):
        assert greatest_common_divisor(12, 8) == 4

    def test_larger_numbers_100_75(self):
        assert greatest_common_divisor(100, 75) == 25

    def test_one_divides_other_6_18(self):
        assert greatest_common_divisor(6, 18) == 6

    def test_reversed_order_15_25(self):
        # GCD is commutative
        assert greatest_common_divisor(15, 25) == 5

    def test_prime_with_multiple_7_21(self):
        assert greatest_common_divisor(7, 21) == 7

    def test_two_primes_11_17(self):
        assert greatest_common_divisor(11, 17) == 1

    def test_same_number_42_42(self):
        assert greatest_common_divisor(42, 42) == 42


# ---------------------------------------------------------------------------
# 2. Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Inputs at the boundaries of meaningful ranges."""

    def test_one_and_any_1_100(self):
        assert greatest_common_divisor(1, 100) == 1

    def test_any_and_one_100_1(self):
        assert greatest_common_divisor(100, 1) == 1

    def test_equal_large_numbers_999999_999999(self):
        assert greatest_common_divisor(999999, 999999) == 999999

    def test_small_positive_2_3(self):
        assert greatest_common_divisor(2, 3) == 1

    def test_smallest_nontrivial_2_2(self):
        assert greatest_common_divisor(2, 2) == 2


# ---------------------------------------------------------------------------
# 3. Zero-related inputs
# ---------------------------------------------------------------------------

class TestZeroInputs:
    """Edge cases involving zero."""

    def test_zero_first_arg(self):
        assert greatest_common_divisor(0, 5) == 5

    def test_zero_second_arg(self):
        assert greatest_common_divisor(5, 0) == 5

    def test_both_zeros(self):
        assert greatest_common_divisor(0, 0) == 0

    def test_zero_with_negative(self):
        assert greatest_common_divisor(0, -7) == -7

    def test_negative_with_zero(self):
        assert greatest_common_divisor(-7, 0) == -7


# ---------------------------------------------------------------------------
# 4. Negative inputs
# ---------------------------------------------------------------------------

class TestNegativeInputs:
    """Pairs where one or both arguments are negative."""

    def test_first_negative(self):
        # gcd(-10, 5) via Euclidean: (-10, 5) -> (5, -10%5=0) -> 5
        assert greatest_common_divisor(-10, 5) == 5

    def test_second_negative(self):
        # gcd(10, -5) via Euclidean: (10, -5) -> (-5, 10%-5=0) -> -5
        assert greatest_common_divisor(10, -5) == -5

    def test_both_negative(self):
        # gcd(-10, -5) via Euclidean: (-10, -5) -> (-5, -10%-5=0) -> -5
        assert greatest_common_divisor(-10, -5) == -5

    def test_negative_coprime(self):
        # gcd(-3, 7) via Euclidean: (-3, 7) -> (7, -3%7=4) -> (4, 7%4=3)
        # -> (3, 4%3=1) -> (1, 3%1=0) -> 1
        assert greatest_common_divisor(-3, 7) == 1


# ---------------------------------------------------------------------------
# 5. Invalid inputs – should raise TypeError
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Non-integer types that cannot produce a valid GCD."""

    @pytest.mark.parametrize("a, b", [
        ("hello", 5),
        (5, "world"),
        ("abc", "def"),
        (None, 5),
        (5, None),
        (None, None),
        ([3], [5]),
        ({}, {}),
    ])
    def test_raises_type_error(self, a, b):
        with pytest.raises(TypeError):
            greatest_common_divisor(a, b)


# ---------------------------------------------------------------------------
# 6. Docstring doctest examples (sanity check)
# ---------------------------------------------------------------------------

class TestDocstringExamples:
    """Verify the examples from the docstring still hold."""

    def test_doc_example_1(self):
        assert greatest_common_divisor(3, 5) == 1

    def test_doc_example_2(self):
        assert greatest_common_divisor(25, 15) == 5
