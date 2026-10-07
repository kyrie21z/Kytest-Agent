"""Unit tests for solution.prime_fib."""

import pytest
from solution import prime_fib


# ---------------------------------------------------------------------------
# Normal / typical cases – taken directly from the docstring
# ---------------------------------------------------------------------------

class TestDocstringExamples:
    """Cases explicitly given in the function's docstring."""

    def test_prime_fib_1(self):
        assert prime_fib(1) == 2

    def test_prime_fib_2(self):
        assert prime_fib(2) == 3

    def test_prime_fib_3(self):
        assert prime_fib(3) == 5

    def test_prime_fib_4(self):
        assert prime_fib(4) == 13

    def test_prime_fib_5(self):
        assert prime_fib(5) == 89


# ---------------------------------------------------------------------------
# Extended normal cases – manually verified next prime Fibonacci numbers
# ---------------------------------------------------------------------------
# Fibonacci primes (in order): 2, 3, 5, 13, 89, 233, 1597, 28657, 514229, 433494437, …

class TestExtendedNormalCases:
    """Additional correct indices beyond the docstring examples."""

    def test_prime_fib_6(self):
        # 6th prime Fibonacci number is 233
        assert prime_fib(6) == 233

    def test_prime_fib_7(self):
        # 7th prime Fibonacci number is 1597
        assert prime_fib(7) == 1597

    def test_prime_fib_8(self):
        # 8th prime Fibonacci number is 28657
        assert prime_fib(8) == 28657

    def test_prime_fib_9(self):
        # 9th prime Fibonacci number is 514229
        assert prime_fib(9) == 514229

    def test_prime_fib_10(self):
        # 10th prime Fibonacci number is 433494437
        assert prime_fib(10) == 433494437


# ---------------------------------------------------------------------------
# Boundary cases – edges of the valid input range
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Inputs at or near the boundaries of expected usage."""

    def test_smallest_valid_input(self):
        # n=1 is the smallest documented valid input
        assert prime_fib(1) == 2


# ---------------------------------------------------------------------------
# Invalid / edge-case inputs – zero, negative, etc.
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Inputs outside the documented contract (n must be ≥ 1)."""

    def test_zero_input(self):
        # n=0: the while-loop never executes; returns initial b=1
        assert prime_fib(0) == 1

    def test_negative_input(self):
        # n=-1: same behaviour as n=0 – loop doesn't run, returns b=1
        assert prime_fib(-1) == 1


# ---------------------------------------------------------------------------
# Property-based sanity checks
# ---------------------------------------------------------------------------

class TestProperties:
    """General properties that every result must satisfy."""

    def _is_fibonacci(self, x):
        """Check whether x is a Fibonacci number."""
        if x < 0:
            return False
        # A number is Fibonacci iff 5*x^2+4 or 5*x^2-4 is a perfect square.
        def is_square(n):
            if n < 0:
                return False
            s = int(n ** 0.5)
            return s * s == n
        return is_square(5 * x * x + 4) or is_square(5 * x * x - 4)

    def _is_prime(self, x):
        """Deterministic primality check for small integers."""
        if x < 2:
            return False
        if x < 4:
            return True
        if x % 2 == 0 or x % 3 == 0:
            return False
        i = 5
        while i * i <= x:
            if x % i == 0 or x % (i + 2) == 0:
                return False
            i += 6
        return True

    @pytest.mark.parametrize("n", range(1, 11))
    def test_result_is_fibonacci_and_prime(self, n):
        """Every returned value must be both a Fibonacci number and prime."""
        result = prime_fib(n)
        assert self._is_fibonacci(result), f"{result} is not a Fibonacci number"
        assert self._is_prime(result), f"{result} is not prime"

    def test_strictly_increasing(self):
        """The sequence of prime Fibonacci numbers is strictly increasing."""
        prev = None
        for n in range(1, 11):
            val = prime_fib(n)
            if prev is not None:
                assert val > prev, f"prime_fib({n})={val} not > prime_fib({n-1})={prev}"
            prev = val
