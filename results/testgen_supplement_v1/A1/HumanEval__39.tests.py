"""Unit tests for prime_fib from solution.py.

The function prime_fib(n) returns the n-th number that is both a Fibonacci
number and a prime number.

Docstring examples:
    prime_fib(1) -> 2
    prime_fib(2) -> 3
    prime_fib(3) -> 5
    prime_fib(4) -> 13
    prime_fib(5) -> 89

Additional verified values:
    prime_fib(6) -> 233
    prime_fib(7) -> 1597
    prime_fib(8) -> 28657
    prime_fib(9) -> 514229
    prime_fib(10) -> 433494437

Edge / boundary behaviour observed:
    prime_fib(0) -> 1   (loop never enters; returns initial b=1)
    prime_fib(-1) -> 1  (same reason)

Invalid inputs raise TypeError:
    str, None, etc.
"""

import pytest
from solution import prime_fib


# ---------------------------------------------------------------------------
# 1. Normal cases – docstring examples
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests against the documented examples in the docstring."""

    def test_n_equals_1(self):
        assert prime_fib(1) == 2

    def test_n_equals_2(self):
        assert prime_fib(2) == 3

    def test_n_equals_3(self):
        assert prime_fib(3) == 5

    def test_n_equals_4(self):
        assert prime_fib(4) == 13

    def test_n_equals_5(self):
        assert prime_fib(5) == 89


# ---------------------------------------------------------------------------
# 2. Boundary cases – edges of valid input range
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries of the valid positive-integer range."""

    def test_n_equals_6(self):
        assert prime_fib(6) == 233

    def test_n_equals_7(self):
        assert prime_fib(7) == 1597

    def test_n_equals_8(self):
        assert prime_fib(8) == 28657

    def test_n_equals_9(self):
        assert prime_fib(9) == 514229

    def test_n_equals_10(self):
        assert prime_fib(10) == 433494437

    # Larger values to exercise bigger Fibonacci numbers
    def test_n_equals_15(self):
        assert prime_fib(15) == 475420437734698220747368027166749382927701417016557193662268716376935476241

    def test_n_equals_20(self):
        assert prime_fib(20) == 36684474316080978061473613646275630451100586901195229815270242868417768061193560857904335017879540515228143777781065869


# ---------------------------------------------------------------------------
# 3. Empty / zero-size / null-like inputs
# ---------------------------------------------------------------------------

class TestZeroAndNegativeInputs:
    """Tests for n <= 0, where the while-loop body never executes."""

    def test_n_equals_0(self):
        """n=0: c_prime starts at 0, condition 0 < 0 is False → returns b=1."""
        assert prime_fib(0) == 1

    def test_n_equals_negative_one(self):
        """n=-1: same as above, loop never runs."""
        assert prime_fib(-1) == 1

    def test_n_equals_negative_ten(self):
        """n=-10: same behaviour."""
        assert prime_fib(-10) == 1


# ---------------------------------------------------------------------------
# 4. Invalid inputs – should raise TypeError
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests that non-integer types raise TypeError."""

    @pytest.mark.parametrize("invalid_input", [
        "abc",       # string
        None,        # NoneType
        [],          # list
        {},          # dict
        set(),       # set
    ])
    def test_invalid_type_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError):
            prime_fib(invalid_input)

    def test_float_input(self):
        """float is accepted by Python's comparison operators; 1.5 behaves like 1."""
        assert prime_fib(1.5) == 2


# ---------------------------------------------------------------------------
# 5. Exception cases – verify no unexpected exceptions for valid inputs
# ---------------------------------------------------------------------------

class TestNoUnexpectedExceptions:
    """Ensure that all reasonable positive integers execute without error."""

    @pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_no_exception_for_small_n(self, n):
        result = prime_fib(n)
        assert isinstance(result, int)
        assert result > 0

    def test_result_is_always_positive(self):
        """Every returned value must be a positive integer."""
        for n in range(1, 11):
            val = prime_fib(n)
            assert isinstance(val, int), f"Expected int for n={n}, got {type(val)}"
            assert val > 0, f"Expected positive for n={n}, got {val}"


# ---------------------------------------------------------------------------
# 6. Property-based sanity checks
# ---------------------------------------------------------------------------

class TestProperties:
    """Higher-level properties about the output."""

    def test_strictly_increasing(self):
        """prime_fib(n) should be strictly increasing with n."""
        prev = None
        for n in range(1, 11):
            val = prime_fib(n)
            if prev is not None:
                assert val > prev, f"Not strictly increasing at n={n}: {prev} >= {val}"
            prev = val

    def test_all_results_are_integers(self):
        """All results must be Python ints."""
        for n in range(1, 11):
            assert isinstance(prime_fib(n), int)
