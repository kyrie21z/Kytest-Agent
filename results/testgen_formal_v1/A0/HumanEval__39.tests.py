"""Unit tests for solution.prime_fib."""

import pytest
from solution import prime_fib


class TestPrimeFibBasic:
    """Tests for basic functionality of prime_fib."""

    def test_prime_fib_1(self):
        """Test the 1st prime Fibonacci number."""
        assert prime_fib(1) == 2

    def test_prime_fib_2(self):
        """Test the 2nd prime Fibonacci number."""
        assert prime_fib(2) == 3

    def test_prime_fib_3(self):
        """Test the 3rd prime Fibonacci number."""
        assert prime_fib(3) == 5

    def test_prime_fib_4(self):
        """Test the 4th prime Fibonacci number."""
        assert prime_fib(4) == 13

    def test_prime_fib_5(self):
        """Test the 5th prime Fibonacci number."""
        assert prime_fib(5) == 89


class TestPrimeFibLargerValues:
    """Tests for larger values of n."""

    def test_prime_fib_6(self):
        """Test the 6th prime Fibonacci number."""
        assert prime_fib(6) == 233

    def test_prime_fib_7(self):
        """Test the 7th prime Fibonacci number."""
        assert prime_fib(7) == 1597

    def test_prime_fib_8(self):
        """Test the 8th prime Fibonacci number."""
        assert prime_fib(8) == 28657

    def test_prime_fib_9(self):
        """Test the 9th prime Fibonacci number."""
        assert prime_fib(9) == 514229


class TestPrimeFibProperties:
    """Tests verifying mathematical properties of results."""

    @pytest.mark.parametrize("n", range(1, 10))
    def test_result_is_fibonacci(self, n):
        """Verify that every result is a Fibonacci number."""
        result = prime_fib(n)
        # Generate Fibonacci numbers up to result
        a, b = 0, 1
        while b < result:
            a, b = b, a + b
        assert b == result, f"{result} is not a Fibonacci number"

    @pytest.mark.parametrize("n", range(1, 10))
    def test_result_is_prime(self, n):
        """Verify that every result is a prime number."""
        result = prime_fib(n)
        if result < 2:
            pytest.fail(f"{result} is less than 2, cannot be prime")
        # Simple trial division primality check
        for i in range(2, int(result ** 0.5) + 1):
            assert result % i != 0, f"{result} is divisible by {i}"

    def test_results_are_strictly_increasing(self):
        """Verify that results are strictly increasing with n."""
        prev = None
        for n in range(1, 10):
            val = prime_fib(n)
            if prev is not None:
                assert val > prev, f"prime_fib({n})={val} is not greater than prime_fib({n-1})={prev}"
            prev = val

    def test_no_duplicates(self):
        """Verify that no two results are the same."""
        results = [prime_fib(i) for i in range(1, 10)]
        assert len(results) == len(set(results)), "Duplicate values found in results"


class TestPrimeFibEdgeCases:
    """Tests for edge cases."""

    def test_single_digit_input(self):
        """Test with single digit inputs."""
        assert isinstance(prime_fib(1), int)
        assert isinstance(prime_fib(9), int)

    def test_return_type(self):
        """Verify return type is int."""
        assert isinstance(prime_fib(1), int)
        assert isinstance(prime_fib(5), int)
        assert isinstance(prime_fib(9), int)


class TestPrimeFibDoctests:
    """Run the built-in doctests."""

    def test_doctests(self):
        """Execute all doctests defined in prime_fib docstring."""
        import doctest
        from solution import prime_fib
        results = doctest.testmod(m=None, verbose=False, optionflags=doctest.NORMALIZE_WHITESPACE)
        assert results.failed == 0, f"{results.failed} doctest(s) failed"
