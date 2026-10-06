"""Unit tests for solution.prime_fib."""

import pytest
from solution import prime_fib


# ---------------------------------------------------------------------------
# 1. Normal / typical inputs – exact expected outputs derived from the
#    documented doctests and manual verification.
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests against the documented examples and known prime Fibonacci numbers."""

    def test_n1(self):
        # 1st prime Fibonacci number
        assert prime_fib(1) == 2

    def test_n2(self):
        # 2nd prime Fibonacci number
        assert prime_fib(2) == 3

    def test_n3(self):
        # 3rd prime Fibonacci number
        assert prime_fib(3) == 5

    def test_n4(self):
        # 4th prime Fibonacci number
        assert prime_fib(4) == 13

    def test_n5(self):
        # 5th prime Fibonacci number
        assert prime_fib(5) == 89

    def test_n6(self):
        # 6th prime Fibonacci number
        assert prime_fib(6) == 233

    def test_n7(self):
        # 7th prime Fibonacci number
        assert prime_fib(7) == 1597

    def test_n8(self):
        # 8th prime Fibonacci number
        assert prime_fib(8) == 28657

    def test_n9(self):
        # 9th prime Fibonacci number
        assert prime_fib(9) == 514229


# ---------------------------------------------------------------------------
# 2. Boundary cases – edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries of the valid positive-integer range."""

    def test_n0(self):
        # n=0: while-loop condition (0 < 0) is False immediately,
        # so the function returns the initial value of b (= 1).
        assert prime_fib(0) == 1

    def test_large_n(self):
        # A moderately large n to ensure correctness beyond small values.
        # prime_fib(10) should be 433494437
        assert prime_fib(10) == 433494437


# ---------------------------------------------------------------------------
# 3. Empty / null / zero-size inputs
# ---------------------------------------------------------------------------

class TestZeroAndNullInputs:
    """Tests for zero and null-like inputs."""

    def test_zero(self):
        # Already covered in boundary, but restated here for clarity.
        assert prime_fib(0) == 1

    def test_none_input(self):
        # Passing None should raise TypeError because `None < int` fails.
        with pytest.raises(TypeError):
            prime_fib(None)


# ---------------------------------------------------------------------------
# 4. Invalid inputs – types or values outside the implied contract
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests for inputs that violate the function's implicit constraints."""

    @pytest.mark.parametrize("bad_value", [-1, -5, -100])
    def test_negative_integers(self, bad_value):
        # Negative n: while-loop condition (0 < negative) is False,
        # so the function returns the initial b (= 1).
        assert prime_fib(bad_value) == 1

    @pytest.mark.parametrize("bad_value", [0.5, 1.0, 2.7])
    def test_float_inputs(self, bad_value):
        # Floats are technically comparable with ints in Python,
        # but they are not valid "n-th" indices. The function will
        # attempt to iterate; e.g. 1.0 < 1 evaluates to False,
        # so prime_fib(1.0) returns 1 instead of 2.
        # We document this behaviour rather than asserting an error.
        result = prime_fib(bad_value)
        assert isinstance(result, int)

    def test_string_input(self):
        # String cannot be compared with int via `<`, raises TypeError.
        with pytest.raises(TypeError):
            prime_fib("abc")

    def test_list_input(self):
        # List cannot be compared with int via `<`, raises TypeError.
        with pytest.raises(TypeError):
            prime_fib([1, 2])

    def test_dict_input(self):
        with pytest.raises(TypeError):
            prime_fib({"n": 5})


# ---------------------------------------------------------------------------
# 5. Exception cases – verify the function can raise under certain inputs
# ---------------------------------------------------------------------------

class TestExceptionCases:
    """Tests where the function is expected to raise exceptions."""

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError):
            prime_fib(None)

    def test_string_raises_type_error(self):
        with pytest.raises(TypeError):
            prime_fib("hello")

    def test_tuple_raises_type_error(self):
        with pytest.raises(TypeError):
            prime_fib((1, 2))

    def test_set_raises_type_error(self):
        with pytest.raises(TypeError):
            prime_fib({1, 2})


# ---------------------------------------------------------------------------
# 6. Property-based sanity checks
# ---------------------------------------------------------------------------

class TestProperties:
    """Additional sanity checks on the mathematical properties of results."""

    def test_results_are_positive(self):
        for n in range(1, 11):
            assert prime_fib(n) > 0

    def test_results_are_strictly_increasing(self):
        prev = None
        for n in range(1, 11):
            val = prime_fib(n)
            if prev is not None:
                assert val > prev
            prev = val

    def test_result_is_integer(self):
        for n in range(1, 11):
            assert isinstance(prime_fib(n), int)
