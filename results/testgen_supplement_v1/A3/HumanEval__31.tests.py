"""Unit tests for solution.is_prime."""

import pytest
from solution import is_prime


# ---------------------------------------------------------------------------
# Docstring examples (the canonical set from the doctest block)
# ---------------------------------------------------------------------------
class TestDocstringExamples:
    def test_is_prime_6(self):
        assert is_prime(6) is False

    def test_is_prime_101(self):
        assert is_prime(101) is True

    def test_is_prime_11(self):
        assert is_prime(11) is True

    def test_is_prime_13441(self):
        assert is_prime(13441) is True

    def test_is_prime_61(self):
        assert is_prime(61) is True

    def test_is_prime_4(self):
        assert is_prime(4) is False

    def test_is_prime_1(self):
        assert is_prime(1) is False


# ---------------------------------------------------------------------------
# Small primes (boundary at the bottom of the prime range)
# ---------------------------------------------------------------------------
class TestSmallPrimes:
    def test_two(self):
        """2 is the smallest and only even prime."""
        assert is_prime(2) is True

    def test_three(self):
        assert is_prime(3) is True

    def test_five(self):
        assert is_prime(5) is True

    def test_seven(self):
        assert is_prime(7) is True

    def test_thirteen(self):
        assert is_prime(13) is True

    def test_seventeen(self):
        assert is_prime(17) is True


# ---------------------------------------------------------------------------
# Small composites
# ---------------------------------------------------------------------------
class TestSmallComposites:
    def test_zero(self):
        assert is_prime(0) is False

    def test_eight(self):
        assert is_prime(8) is False

    def test_nine(self):
        assert is_prime(9) is False

    def test_ten(self):
        assert is_prime(10) is False

    def test_twelve(self):
        assert is_prime(12) is False

    def test_fifteen(self):
        assert is_prime(15) is False

    def test_twenty_five(self):
        assert is_prime(25) is False

    def test_one_hundred(self):
        assert is_prime(100) is False


# ---------------------------------------------------------------------------
# Boundary: numbers <= 1 (should all be non-prime)
# ---------------------------------------------------------------------------
class TestBoundaryNonPositive:
    @pytest.mark.parametrize("n", [0, -1, -2, -10, -100])
    def test_non_positive(self, n):
        assert is_prime(n) is False


# ---------------------------------------------------------------------------
# Larger primes
# ---------------------------------------------------------------------------
class TestLargerPrimes:
    def test_97(self):
        assert is_prime(97) is True

    def test_1009(self):
        assert is_prime(1009) is True

    def test_104729(self):
        # 104729 is the 10000th prime number
        assert is_prime(104729) is True

    def test_999983(self):
        # Largest 6-digit prime
        assert is_prime(999983) is True


# ---------------------------------------------------------------------------
# Larger composites
# ---------------------------------------------------------------------------
class TestLargerComposites:
    def test_1000(self):
        assert is_prime(1000) is False

    def test_999999(self):
        assert is_prime(999999) is False

    def test_square_of_prime(self):
        """A square of a prime is composite."""
        assert is_prime(49) is False   # 7^2
        assert is_prime(121) is False  # 11^2
        assert is_prime(289) is False  # 17^2

    def test_even_greater_than_2(self):
        """All even numbers > 2 are composite."""
        for n in range(4, 20, 2):
            assert is_prime(n) is False


# ---------------------------------------------------------------------------
# Invalid / unexpected input types
# ---------------------------------------------------------------------------
class TestInvalidInputs:
    @pytest.mark.parametrize("value", [None, "hello", [1, 2], {"a": 1}])
    def test_non_integer_raises(self, value):
        """Non-integer types should raise TypeError or similar."""
        with pytest.raises((TypeError, AttributeError)):
            is_prime(value)

    def test_float_input(self):
        """Floats may raise TypeError; some implementations accept them."""
        # We allow either an exception or correct boolean result
        try:
            result = is_prime(3.0)
            # If no exception, the result should still be meaningful
            assert isinstance(result, bool)
        except (TypeError, ValueError):
            pass  # acceptable

    def test_negative_float(self):
        """Negative floats are <= 1, so is_prime returns False (no exception)."""
        assert is_prime(-3.5) is False
