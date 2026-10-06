"""Unit tests for solution.prime_fib."""

import pytest
from solution import prime_fib


class TestPrimeFibDocstringExamples:
    """Tests from the docstring doctests."""

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
        # 6th prime Fibonacci number
        assert prime_fib(6) == 233

    def test_prime_fib_7(self):
        # 7th prime Fibonacci number
        assert prime_fib(7) == 1597

    def test_prime_fib_8(self):
        # 8th prime Fibonacci number
        assert prime_fib(8) == 28657

    def test_prime_fib_9(self):
        # 9th prime Fibonacci number
        assert prime_fib(9) == 514229


class TestPrimeFibMonotonicity:
    """Verify that prime_fib results are strictly increasing."""

    def test_strictly_increasing(self):
        prev = None
        for i in range(1, 8):
            val = prime_fib(i)
            if prev is not None:
                assert val > prev, f"prime_fib({i})={val} should be > prime_fib({i-1})={prev}"
            prev = val


class TestPrimeFibIsFibonacci:
    """Verify that every result is actually a Fibonacci number."""

    @staticmethod
    def _is_fibonacci(n):
        """Check if n is a Fibonacci number using the perfect-square property."""
        if n < 0:
            return False
        def _is_perfect_square(x):
            if x < 0:
                return False
            s = int(x ** 0.5)
            return s * s == x
        return _is_perfect_square(5 * n * n + 4) or _is_perfect_square(5 * n * n - 4)

    def test_results_are_fibonacci(self):
        for i in range(1, 10):
            val = prime_fib(i)
            assert self._is_fibonacci(val), f"{val} (prime_fib({i})) is not a Fibonacci number"


class TestPrimeFibIsPrime:
    """Verify that every result is actually prime."""

    @staticmethod
    def _is_prime(n):
        """Deterministic primality check for small numbers."""
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

    def test_results_are_prime(self):
        for i in range(1, 10):
            val = prime_fib(i)
            assert self._is_prime(val), f"{val} (prime_fib({i})) is not prime"


class TestPrimeFibBoundaryCases:
    """Edge cases at boundaries of valid input ranges."""

    def test_prime_fib_zero(self):
        # n=0: loop condition c_prime < 0 is False immediately, returns b=1
        # 1 is returned but is neither prime nor Fibonacci-indexed; this is the actual behavior
        result = prime_fib(0)
        assert result == 1

    def test_prime_fib_negative(self):
        # n=-1: same as n=0, loop doesn't execute, returns b=1
        result = prime_fib(-1)
        assert result == 1

    def test_prime_fib_large_n(self):
        # A larger n to stress-test the algorithm
        result = prime_fib(10)
        # 10th prime Fibonacci number is 433494437
        assert result == 433494437


class TestPrimeFibInputTypes:
    """Test behavior with various input types."""

    def test_float_input(self):
        # Passing a float like 1.0 — Python will compare 0 < 1.0 correctly
        # but the semantics are unusual. Just verify it runs without crashing
        # and produces a deterministic result.
        result = prime_fib(1.0)
        assert isinstance(result, int)

    def test_string_input_raises_or_returns(self):
        # Passing a string like "1" — comparison 0 < "1" raises TypeError in Python 3
        with pytest.raises(TypeError):
            prime_fib("1")

    def test_none_input_raises(self):
        with pytest.raises(TypeError):
            prime_fib(None)

    def test_list_input_raises(self):
        with pytest.raises(TypeError):
            prime_fib([1])


class TestPrimeFibLargeInputs:
    """Stress tests with larger inputs."""

    def test_prime_fib_15(self):
        # 15th prime Fibonacci number — verifies correctness at scale
        result = prime_fib(15)
        assert result > 0
        # Verify it's prime using our helper
        assert self._is_prime_helper(result)

    @staticmethod
    def _is_prime_helper(n):
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
