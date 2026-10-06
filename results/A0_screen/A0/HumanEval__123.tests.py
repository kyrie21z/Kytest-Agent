import pytest
from solution import get_odd_collatz


class TestGetOddCollatz:
    """Tests for the get_odd_collatz function."""

    def test_n_equals_one(self):
        """Collatz(1) should return [1]."""
        assert get_odd_collatz(1) == [1]

    def test_example_from_docstring(self):
        """Example from the docstring: get_odd_collatz(5) returns [1, 5]."""
        assert get_odd_collatz(5) == [1, 5]

    def test_n_equals_two(self):
        """Collatz sequence for 2: [2, 1]. Odd numbers: [1]."""
        assert get_odd_collatz(2) == [1]

    def test_n_equals_three(self):
        """Collatz sequence for 3: [3, 10, 5, 16, 8, 4, 2, 1].
        Odd numbers: [3, 5, 1]. Sorted: [1, 3, 5]."""
        assert get_odd_collatz(3) == [1, 3, 5]

    def test_n_equals_four(self):
        """Collatz sequence for 4: [4, 2, 1]. Odd numbers: [1]."""
        assert get_odd_collatz(4) == [1]

    def test_n_equals_six(self):
        """Collatz sequence for 6: [6, 3, 10, 5, 16, 8, 4, 2, 1].
        Odd numbers: [3, 5, 1]. Sorted: [1, 3, 5]."""
        assert get_odd_collatz(6) == [1, 3, 5]

    def test_n_equals_seven(self):
        """Collatz sequence for 7: [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1].
        Odd numbers: [7, 11, 17, 13, 5, 1]. Sorted: [1, 5, 7, 11, 13, 17]."""
        assert get_odd_collatz(7) == [1, 5, 7, 11, 13, 17]

    def test_n_equals_eight(self):
        """Collatz sequence for 8: [8, 4, 2, 1]. Odd numbers: [1]."""
        assert get_odd_collatz(8) == [1]

    def test_n_equals_twelve(self):
        """Collatz sequence for 12: [12, 6, 3, 10, 5, 16, 8, 4, 2, 1].
        Odd numbers: [3, 5, 1]. Sorted: [1, 3, 5]."""
        assert get_odd_collatz(12) == [1, 3, 5]

    def test_result_is_sorted(self):
        """Result should always be sorted in increasing order."""
        result = get_odd_collatz(27)
        assert result == sorted(result)

    def test_result_contains_only_odd_numbers(self):
        """All elements in the result must be odd."""
        result = get_odd_collatz(27)
        assert all(x % 2 == 1 for x in result)

    def test_result_always_includes_one(self):
        """The Collatz sequence always reaches 1, so 1 must be in the result."""
        for n in range(1, 101):
            assert 1 in get_odd_collatz(n)

    def test_larger_number(self):
        """Test with a larger input number."""
        result = get_odd_collatz(27)
        # Verify it's a non-empty list of odd integers
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(x, int) for x in result)
        assert all(x % 2 == 1 for x in result)

    def test_input_is_positive_integer(self):
        """Function should work correctly for various positive integers."""
        # Test a range of inputs
        for n in [1, 2, 3, 5, 7, 10, 15, 20, 50, 100]:
            result = get_odd_collatz(n)
            assert isinstance(result, list)
            assert len(result) >= 1
            assert all(x % 2 == 1 for x in result)
            assert result == sorted(result)

    def test_return_type(self):
        """Return value should be a list."""
        result = get_odd_collatz(5)
        assert isinstance(result, list)

    def test_elements_are_integers(self):
        """All elements in the returned list should be integers."""
        result = get_odd_collatz(27)
        assert all(isinstance(x, int) for x in result)

    def test_no_duplicates(self):
        """The result list should not contain duplicate values."""
        for n in range(1, 50):
            result = get_odd_collatz(n)
            assert len(result) == len(set(result))
