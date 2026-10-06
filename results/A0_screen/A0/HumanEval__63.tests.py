"""Unit tests for fibfib function in solution.py."""

import pytest
from solution import fibfib


class TestFibFib:
    """Tests for the fibfib function."""

    def test_base_case_zero(self):
        """fibfib(0) should return 0."""
        assert fibfib(0) == 0

    def test_base_case_one(self):
        """fibfib(1) should return 0."""
        assert fibfib(1) == 0

    def test_base_case_two(self):
        """fibfib(2) should return 1."""
        assert fibfib(2) == 1

    def test_example_three(self):
        """fibfib(3) = fibfib(2) + fibfib(1) + fibfib(0) = 1 + 0 + 0 = 1."""
        assert fibfib(3) == 1

    def test_example_four(self):
        """fibfib(4) = fibfib(3) + fibfib(2) + fibfib(1) = 1 + 1 + 0 = 2."""
        assert fibfib(4) == 2

    def test_example_five(self):
        """fibfib(5) = fibfib(4) + fibfib(3) + fibfib(2) = 2 + 1 + 1 = 4."""
        assert fibfib(5) == 4

    def test_example_eight(self):
        """fibfib(8) should return 24 (from docstring)."""
        assert fibfib(8) == 24

    def test_negative_input(self):
        """Negative inputs should not raise an error unexpectedly."""
        result = fibfib(-1)
        assert isinstance(result, int)

    def test_return_type(self):
        """fibfib should always return an int."""
        for n in range(10):
            assert isinstance(fibfib(n), int)

    def test_monotonic_growth(self):
        """For n >= 2, fibfib should be non-decreasing."""
        for n in range(2, 20):
            if n > 2:
                assert fibfib(n) >= fibfib(n - 1)

    def test_larger_values(self):
        """Test some larger values to ensure correctness."""
        # Computed manually: fibfib(9)=44, fibfib(10)=81, fibfib(11)=149, etc.
        assert fibfib(9) == 44
        assert fibfib(10) == 81
        assert fibfib(15) == 1705
        assert fibfib(20) == 35890

    def test_docstring_examples(self):
        """Verify all examples from the docstring."""
        assert fibfib(1) == 0
        assert fibfib(5) == 4
        assert fibfib(8) == 24
