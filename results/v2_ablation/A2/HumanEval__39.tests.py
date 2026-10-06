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
    """Additional normal cases with typical positive integer inputs."""

    def test_prime_fib_6(self):
        # 6th prime Fibonacci number: 233
        assert prime_fib(6) == 233

    def test_prime_fib_7(self):
        # 7th prime Fibonacci number: 1597
        assert prime_fib(7) == 1597

    def test_prime_fib_8(self):
        # 8th prime Fibonacci number: 28657
        assert prime_fib(8) == 28657

    def test_prime_fib_9(self):
        # 9th prime Fibonacci number: 514229
        assert prime_fib(9) == 514229


class TestPrimeFibBoundaryCases:
    """Boundary cases at the edges of valid input ranges."""

    def test_prime_fib_smallest_valid_input(self):
        # Smallest valid positive input
        assert prime_fib(1) == 2

    def test_prime_fib_larger_input(self):
        # A moderately larger input to check correctness scales
        assert prime_fib(10) == 433494437


class TestPrimeFibZeroAndNegativeInputs:
    """Tests for zero and negative inputs — edge of valid range."""

    def test_prime_fib_zero(self):
        # When n=0, the while loop condition c_prime < 0 is False immediately,
        # so the function returns b=1 without entering the loop.
        assert prime_fib(0) == 1

    def test_prime_fib_negative_one(self):
        # Same as zero: loop never executes, returns initial b=1.
        assert prime_fib(-1) == 1

    def test_prime_fib_negative_large(self):
        assert prime_fib(-100) == 1


class TestPrimeFibInputType:
    """Tests verifying the function handles different input types."""

    def test_prime_fib_returns_int(self):
        result = prime_fib(5)
        assert isinstance(result, int)

    def test_prime_fib_positive_returns_positive(self):
        for n in [1, 2, 3, 4, 5, 6, 7]:
            assert prime_fib(n) > 0


class TestPrimeFibProperties:
    """Tests based on mathematical properties of the output."""

    def test_output_is_fibonacci(self):
        """Verify each returned value is actually a Fibonacci number."""
        fibs = set()
        a, b = 0, 1
        for _ in range(1000):
            fibs.add(b)
            a, b = b, a + b
            if b > 10**15:
                break
        for n in range(1, 10):
            assert prime_fib(n) in fibs

    def test_output_is_prime(self):
        """Verify each returned value is prime using simple trial division."""
        def is_prime(num):
            if num < 2:
                return False
            if num < 4:
                return True
            if num % 2 == 0 or num % 3 == 0:
                return False
            i = 5
            while i * i <= num:
                if num % i == 0 or num % (i + 2) == 0:
                    return False
                i += 6
            return True

        for n in range(1, 10):
            assert is_prime(prime_fib(n)), f"prime_fib({n})={prime_fib(n)} is not prime"

    def test_strictly_increasing(self):
        """Prime Fibonacci numbers should be strictly increasing."""
        prev = None
        for n in range(1, 10):
            val = prime_fib(n)
            if prev is not None:
                assert val > prev
            prev = val
