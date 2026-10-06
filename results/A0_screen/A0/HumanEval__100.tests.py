import pytest
from solution import make_a_pile


class TestMakeAPile:
    """Tests for the make_a_pile function."""

    # --- Examples from docstring ---

    def test_example_n_equals_3(self):
        """Test case from the docstring: make_a_pile(3) == [3, 5, 7]."""
        assert make_a_pile(3) == [3, 5, 7]

    # --- Small inputs ---

    def test_n_equals_1(self):
        """A single-level pile should return a list with just n."""
        assert make_a_pile(1) == [1]

    def test_n_equals_2(self):
        """Even n=2: starts at 2, next even is 4."""
        assert make_a_pile(2) == [2, 4]

    def test_n_equals_4(self):
        """Even n=4: [4, 6, 8, 10]."""
        assert make_a_pile(4) == [4, 6, 8, 10]

    def test_n_equals_5(self):
        """Odd n=5: [5, 7, 9, 11, 13]."""
        assert make_a_pile(5) == [5, 7, 9, 11, 13]

    # --- Larger inputs ---

    def test_n_equals_6(self):
        """Even n=6: [6, 8, 10, 12, 14, 16]."""
        assert make_a_pile(6) == [6, 8, 10, 12, 14, 16]

    def test_n_equals_10(self):
        """Even n=10: starts at 10, increments by 2, 10 elements."""
        expected = [10 + 2 * i for i in range(10)]
        assert make_a_pile(10) == expected

    def test_n_equals_7(self):
        """Odd n=7: starts at 7, increments by 2, 7 elements."""
        expected = [7 + 2 * i for i in range(7)]
        assert make_a_pile(7) == expected

    # --- Return type and structure checks ---

    def test_returns_list(self):
        """The function should always return a list."""
        assert isinstance(make_a_pile(3), list)

    def test_length_equals_n(self):
        """The returned list must have exactly n elements."""
        for n in range(1, 11):
            result = make_a_pile(n)
            assert len(result) == n

    def test_all_elements_are_integers(self):
        """Every element in the result must be an integer."""
        result = make_a_pile(8)
        assert all(isinstance(x, int) for x in result)

    # --- Arithmetic progression property ---

    def test_arithmetic_step_is_2(self):
        """Each consecutive pair should differ by exactly 2."""
        for n in range(2, 11):
            result = make_a_pile(n)
            for i in range(len(result) - 1):
                assert result[i + 1] - result[i] == 2

    def test_first_element_equals_n(self):
        """The first element of the list must equal n."""
        for n in range(1, 11):
            assert make_a_pile(n)[0] == n

    # --- Parity preservation ---

    def test_odd_start_preserves_odd_parity(self):
        """When n is odd, every element should be odd."""
        for n in range(1, 11, 2):
            result = make_a_pile(n)
            assert all(x % 2 != 0 for x in result)

    def test_even_start_preserves_even_parity(self):
        """When n is even, every element should be even."""
        for n in range(2, 11, 2):
            result = make_a_pile(n)
            assert all(x % 2 == 0 for x in result)

    # --- Edge / boundary cases ---

    def test_large_n(self):
        """Test with a larger value to ensure no overflow or index issues."""
        n = 100
        result = make_a_pile(n)
        assert len(result) == n
        assert result[0] == n
        assert result[-1] == n + 2 * (n - 1)

    def test_zero_returns_empty_list(self):
        """n=0 should return an empty list since range(0) produces nothing."""
        assert make_a_pile(0) == []

    def test_negative_returns_empty_list(self):
        """Negative n should return an empty list since range(negative) produces nothing."""
        assert make_a_pile(-3) == []

    def test_non_integer_raises_error(self):
        """Non-integer input should raise an error."""
        with pytest.raises(Exception):
            make_a_pile(3.5)

    def test_string_raises_error(self):
        """String input should raise an error."""
        with pytest.raises(Exception):
            make_a_pile("three")
