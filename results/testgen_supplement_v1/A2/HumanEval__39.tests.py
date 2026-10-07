"""Unit tests for solution.prime_fib."""

import pytest
from solution import prime_fib


class TestPrimeFibDocstringExamples:
    """Tests from the docstring examples."""

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


class TestPrimeFibNormalCases:
    """Additional normal cases beyond the docstring examples."""

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


class TestPrimeFibBoundaryCases:
    """Boundary cases at the edges of valid input ranges."""

    def test_minimum_valid_input(self):
        # Smallest valid positive integer input
        assert prime_fib(1) == 2

    def test_larger_input(self):
        # A moderately larger input to exercise more iterations
        assert prime_fib(10) == 433494437


class TestPrimeFibZeroAndNegativeInputs:
    """Tests for zero and negative inputs (edge of valid range)."""

    def test_zero_input(self):
        # When n=0, the while loop condition c_prime < 0 is immediately False,
        # so the loop body never runs and b remains its initial value 1.
        # Note: 1 is returned but is neither prime nor Fibonacci in the expected sense.
        # This documents the actual runtime behavior.
        assert prime_fib(0) == 1

    def test_negative_input(self):
        # When n<0, same as n=0: loop never executes, returns initial b=1.
        assert prime_fib(-1) == 1

    def test_negative_input_large(self):
        assert prime_fib(-100) == 1


class TestPrimeFibOutputProperties:
    """Verify that outputs are indeed both Fibonacci and prime numbers."""

    def _is_fibonacci(self, x):
        """Check if x is a Fibonacci number."""
        if x < 0:
            return False
        # A number is Fibonacci iff 5*x^2 + 4 or 5*x^2 - 4 is a perfect square
        def is_perfect_square(n):
            if n < 0:
                return False
            s = int(n ** 0.5)
            return s * s == n
        return is_perfect_square(5 * x * x + 4) or is_perfect_square(5 * x * x - 4)

    def _is_prime(self, n):
        """Deterministic primality test for small numbers."""
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    @pytest.mark.parametrize("n,expected", [
        (1, 2),
        (2, 3),
        (3, 5),
        (4, 13),
        (5, 89),
        (6, 233),
        (7, 1597),
        (8, 28657),
    ])
    def test_output_is_fibonacci_and_prime(self, n, expected):
        result = prime_fib(n)
        assert self._is_fibonacci(result), f"{result} is not a Fibonacci number"
        assert self._is_prime(result), f"{result} is not a prime number"
        assert result == expected

    def test_strictly_increasing(self):
        """Each successive call should return a strictly larger value."""
        prev = None
        for n in range(1, 9):
            val = prime_fib(n)
            if prev is not None:
                assert val > prev, f"prime_fib({n})={val} is not greater than prime_fib({n-1})={prev}"
            prev = val


class TestPrimeFibLargeInput:
    """Test with a larger input to exercise many iterations."""

    def test_prime_fib_10(self):
        # 10th prime Fibonacci number
        assert prime_fib(10) == 433494437
