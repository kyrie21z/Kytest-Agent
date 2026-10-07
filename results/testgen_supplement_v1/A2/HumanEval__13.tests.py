"""Unit tests for solution.greatest_common_divisor."""

import pytest
from solution import greatest_common_divisor


# ---------------------------------------------------------------------------
# 1. Normal / typical inputs
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with typical positive integer inputs."""

    def test_coprime_numbers(self):
        """Two coprime numbers have GCD 1."""
        assert greatest_common_divisor(3, 5) == 1

    def test_non_trivial_gcd(self):
        """GCD(25, 15) = 5."""
        assert greatest_common_divisor(25, 15) == 5

    def test_another_non_trivial(self):
        """GCD(12, 8) = 4."""
        assert greatest_common_divisor(12, 8) == 4

    def test_larger_example(self):
        """GCD(100, 75) = 25."""
        assert greatest_common_divisor(100, 75) == 25

    def test_prime_with_multiple(self):
        """GCD(7, 21) = 7 (prime divides composite)."""
        assert greatest_common_divisor(7, 21) == 7

    def test_two_primes_different(self):
        """GCD(3, 7) = 1 (two distinct primes are coprime)."""
        assert greatest_common_divisor(3, 7) == 1


# ---------------------------------------------------------------------------
# 2. Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries of valid integer inputs."""

    def test_one_is_zero_first(self):
        """GCD(0, n) = n."""
        assert greatest_common_divisor(0, 5) == 5

    def test_one_is_zero_second(self):
        """GCD(n, 0) = n."""
        assert greatest_common_divisor(5, 0) == 5

    def test_both_zero(self):
        """GCD(0, 0) = 0 (algorithm returns a when b==0, and a=0)."""
        assert greatest_common_divisor(0, 0) == 0

    def test_equal_positive_numbers(self):
        """GCD(n, n) = n."""
        assert greatest_common_divisor(7, 7) == 7

    def test_equal_one(self):
        """GCD(1, 1) = 1."""
        assert greatest_common_divisor(1, 1) == 1

    def test_one_divides_other(self):
        """GCD(10, 2) = 2 (smaller divides larger)."""
        assert greatest_common_divisor(10, 2) == 2

    def test_one_divides_other_reversed(self):
        """GCD(2, 10) = 2."""
        assert greatest_common_divisor(2, 10) == 2

    def test_one_as_argument(self):
        """GCD(1, 100) = 1 (1 divides everything)."""
        assert greatest_common_divisor(1, 100) == 1

    def test_large_numbers(self):
        """GCD(1_000_000, 500_000) = 500_000."""
        assert greatest_common_divisor(1_000_000, 500_000) == 500_000

    def test_large_coprime(self):
        """GCD of two large coprime numbers is 1."""
        assert greatest_common_divisor(999_999, 999_997) == 1


# ---------------------------------------------------------------------------
# 3. Negative inputs
# ---------------------------------------------------------------------------

class TestNegativeInputs:
    """Tests with negative integer arguments."""

    def test_negative_first(self):
        """GCD(-6, 4) — algorithm may return negative result."""
        result = greatest_common_divisor(-6, 4)
        # The Euclidean implementation returns -2; absolute value is 2.
        assert abs(result) == 2

    def test_negative_second(self):
        """GCD(6, -4) — algorithm may return negative result."""
        result = greatest_common_divisor(6, -4)
        assert abs(result) == 2

    def test_both_negative(self):
        """GCD(-6, -4) — algorithm may return negative result."""
        result = greatest_common_divisor(-6, -4)
        assert abs(result) == 2

    def test_negative_coprime(self):
        """GCD(-3, 5) should be 1 in magnitude."""
        result = greatest_common_divisor(-3, 5)
        assert abs(result) == 1


# ---------------------------------------------------------------------------
# 4. Invalid inputs (non-integer types)
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests that demonstrate behaviour with invalid (non-int) inputs."""

    @pytest.mark.parametrize("a, b", [
        ("hello", 5),
        (5, "world"),
        (None, 5),
        ([5], 5),
        ({}, 5),
    ])
    def test_non_integer_raises_type_error(self, a, b):
        """Passing non-integer types should raise TypeError."""
        with pytest.raises(TypeError):
            greatest_common_divisor(a, b)

    def test_float_inputs_return_float(self):
        """Floats do not raise TypeError; the algorithm runs on floats."""
        # query_gcd(3.5, 7) -> query_gcd(7, 3.5) -> query_gcd(3.5, 0.0) -> 3.5
        assert greatest_common_divisor(3.5, 7) == 3.5

    def test_float_inputs_reversed(self):
        """query_gcd(7, 3.5) -> query_gcd(3.5, 0.0) -> 3.5"""
        assert greatest_common_divisor(7, 3.5) == 3.5


# ---------------------------------------------------------------------------
# 5. Exception cases & edge properties
# ---------------------------------------------------------------------------

class TestEdgeProperties:
    """Tests leveraging mathematical properties of GCD."""

    def test_commutativity(self):
        """GCD(a, b) == GCD(b, a)."""
        for a, b in [(12, 8), (25, 15), (100, 75), (3, 5)]:
            assert greatest_common_divisor(a, b) == greatest_common_divisor(b, a)

    def test_self_identity(self):
        """GCD(n, n) == n for various n."""
        for n in [0, 1, 7, 42, 1000]:
            assert greatest_common_divisor(n, n) == n

    def test_result_divides_both(self):
        """The GCD must divide both input numbers."""
        for a, b in [(25, 15), (100, 75), (12, 8), (1_000_000, 500_000)]:
            g = greatest_common_divisor(a, b)
            if g != 0:
                assert a % g == 0
                assert b % g == 0

    def test_result_is_positive_for_nonzero_inputs(self):
        """For nonzero inputs, the GCD should be positive."""
        for a, b in [(25, 15), (12, 8), (100, 75)]:
            assert greatest_common_divisor(a, b) > 0
