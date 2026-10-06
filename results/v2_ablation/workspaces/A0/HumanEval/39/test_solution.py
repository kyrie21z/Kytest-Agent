"""Unit tests for solution.prime_fib using pytest."""

import pytest
from solution import prime_fib


def _is_fibonacci(num):
    """Check if a number is a Fibonacci number."""
    if num < 0:
        return False
    a, b = 0, 1
    while b < num:
        a, b = b, a + b
    return b == num


def _is_prime(num):
    """Check if a number is prime (deterministic)."""
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    i = 3
    while i * i <= num:
        if num % i == 0:
            return False
        i += 2
    return True


class TestPrimeFibDocstringExamples:
    """Tests based on the docstring examples."""

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


class TestPrimeFibSmallValues:
    """Tests for small input values."""

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


class TestPrimeFibLargerValues:
    """Tests for larger input values."""

    def test_prime_fib_10(self):
        # 10th prime Fibonacci number is 433494437
        assert prime_fib(10) == 433494437

    def test_prime_fib_11(self):
        # 11th prime Fibonacci number is 2971215073
        assert prime_fib(11) == 2971215073


class TestPrimeFibProperties:
    """Tests verifying mathematical properties of the results."""

    def test_result_is_always_prime(self):
        """Every result from prime_fib must be a prime number."""
        for n in range(1, 11):
            result = prime_fib(n)
            assert _is_prime(result), f"prime_fib({n})={result} is not prime"

    def test_result_is_always_fibonacci(self):
        """Every result from prime_fib must be a Fibonacci number."""
        for n in range(1, 11):
            result = prime_fib(n)
            assert _is_fibonacci(result), f"prime_fib({n})={result} is not Fibonacci"

    def test_results_are_strictly_increasing(self):
        """Results should be strictly increasing with n."""
        prev = None
        for n in range(1, 11):
            result = prime_fib(n)
            if prev is not None:
                assert result > prev, f"prime_fib({n})={result} is not greater than prime_fib({n-1})={prev}"
            prev = result

    def test_no_duplicate_results(self):
        """Each call with different n should return a different value."""
        results = [prime_fib(n) for n in range(1, 11)]
        assert len(results) == len(set(results)), "Duplicate results found"


class TestPrimeFibEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_minimum_input(self):
        """Test with the smallest valid input n=1."""
        result = prime_fib(1)
        assert result == 2
        assert _is_prime(result)
        assert _is_fibonacci(result)

    def test_first_three_prime_fibs_are_consecutive_primes(self):
        """The first three prime Fibonacci numbers (2, 3, 5) are consecutive primes."""
        assert prime_fib(1) == 2
        assert prime_fib(2) == 3
        assert prime_fib(3) == 5


class TestPrimeFibTypeAndValue:
    """Tests for return type and value constraints."""

    def test_returns_integer(self):
        """prime_fib should return an int."""
        for n in range(1, 6):
            result = prime_fib(n)
            assert isinstance(result, int), f"prime_fib({n}) returned {type(result)} instead of int"

    def test_positive_results(self):
        """All results should be positive integers."""
        for n in range(1, 11):
            result = prime_fib(n)
            assert result > 0, f"prime_fib({n})={result} is not positive"


class TestPrimeFibConsistency:
    """Tests for deterministic behavior."""

    def test_same_input_same_output(self):
        """Calling prime_fib with the same input multiple times should give the same result."""
        for n in range(1, 11):
            results = [prime_fib(n) for _ in range(5)]
            assert all(r == results[0] for r in results), f"Non-deterministic results for n={n}"
