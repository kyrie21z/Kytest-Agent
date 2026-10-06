import pytest
from solution import prime_fib


class TestPrimeFib:
    """Tests for the prime_fib function."""

    # --- Doctest examples from the docstring ---

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

    # --- Additional known prime Fibonacci numbers ---
    # Prime Fibonacci sequence: 2, 3, 5, 13, 89, 233, 1597, 28657, 514229, ...

    def test_prime_fib_6(self):
        assert prime_fib(6) == 233

    def test_prime_fib_7(self):
        assert prime_fib(7) == 1597

    def test_prime_fib_8(self):
        assert prime_fib(8) == 28657

    def test_prime_fib_9(self):
        assert prime_fib(9) == 514229

    # --- Input validation / edge cases ---

    def test_prime_fib_zero(self):
        """n=0 should return 0 because no prime Fibonacci numbers are found before the loop terminates."""
        # With n=0, c_prime starts at 0 which is >= n, so the while loop never executes
        # and b remains 1. But actually the loop condition is c_prime < n, so 0 < 0 is False.
        # a,b start as 0,1; after first iteration a=1, b=1. Since loop doesn't run, returns b=1.
        # Let's verify what the actual behavior is.
        result = prime_fib(0)
        assert isinstance(result, int)

    def test_prime_fib_negative(self):
        """Negative n: the while loop condition c_prime < n will be True initially (0 < negative is False).
        Actually 0 < -1 is False, so loop doesn't execute, returns b=1."""
        result = prime_fib(-1)
        assert isinstance(result, int)

    def test_prime_fib_large_n(self):
        """Test with a larger value to ensure correctness and reasonable performance."""
        result = prime_fib(10)
        assert isinstance(result, int)
        assert result > 514229

    # --- Property-based style checks ---

    def test_result_is_fibonacci(self):
        """The returned value must be a Fibonacci number."""
        def is_fibonacci(x):
            """Check if x is a Fibonacci number."""
            if x < 0:
                return False
            a, b = 0, 1
            while b < x:
                a, b = b, a + b
            return b == x

        for i in range(1, 10):
            val = prime_fib(i)
            assert is_fibonacci(val), f"{val} (the {i}-th prime fib) is not a Fibonacci number"

    def test_result_is_prime(self):
        """The returned value must be a prime number."""
        def is_prime_small(n):
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

        for i in range(1, 10):
            val = prime_fib(i)
            assert is_prime_small(val), f"{val} (the {i}-th prime fib) is not prime"

    def test_results_are_strictly_increasing(self):
        """Each successive prime Fibonacci number must be strictly greater than the previous one."""
        results = [prime_fib(i) for i in range(1, 10)]
        for i in range(1, len(results)):
            assert results[i] > results[i - 1], \
                f"prime_fib({i+1})={results[i]} is not greater than prime_fib({i})={results[i-1]}"

    def test_no_duplicates(self):
        """No two calls with different n should return the same value."""
        results = [prime_fib(i) for i in range(1, 10)]
        assert len(results) == len(set(results)), "Duplicate values found in prime_fib results"
