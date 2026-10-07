"""Unit tests for count_up_to in solution.py."""

import pytest
from solution import count_up_to


class TestCountUpToNormalCases:
    """Test normal/typical inputs as documented in the docstring."""

    def test_n_equals_5(self):
        assert count_up_to(5) == [2, 3]

    def test_n_equals_11(self):
        assert count_up_to(11) == [2, 3, 5, 7]

    def test_n_equals_20(self):
        assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_n_equals_18(self):
        assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]


class TestCountUpToBoundaryCases:
    """Test boundary values at the edges of valid input ranges."""

    def test_n_equals_0(self):
        """No primes less than 0."""
        assert count_up_to(0) == []

    def test_n_equals_1(self):
        """No primes less than 1."""
        assert count_up_to(1) == []

    def test_n_equals_2(self):
        """No primes strictly less than 2 (smallest prime is 2 itself)."""
        assert count_up_to(2) == []

    def test_n_equals_3(self):
        """Only prime strictly less than 3 is 2."""
        assert count_up_to(3) == [2]

    def test_n_equals_4(self):
        """Primes less than 4 are 2 and 3."""
        assert count_up_to(4) == [2, 3]

    def test_n_equals_10(self):
        """Primes less than 10: 2, 3, 5, 7."""
        assert count_up_to(10) == [2, 3, 5, 7]

    def test_n_equals_100(self):
        """Primes less than 100."""
        expected = [
            2, 3, 5, 7, 11, 13, 17, 19,
            23, 29, 31, 37, 41, 43, 47,
            53, 59, 61, 67, 71, 73, 79,
            83, 89, 97,
        ]
        assert count_up_to(100) == expected


class TestCountUpToEmptyAndZeroInputs:
    """Test edge cases with zero-size or effectively empty results."""

    def test_zero_returns_empty_list(self):
        assert count_up_to(0) == []

    def test_one_returns_empty_list(self):
        assert count_up_to(1) == []

    def test_two_returns_empty_list(self):
        assert count_up_to(2) == []


class TestCountUpToLargeInputs:
    """Test larger inputs to verify correctness on bigger ranges."""

    def test_n_equals_50(self):
        expected = [
            2, 3, 5, 7, 11, 13, 17, 19,
            23, 29, 31, 37, 41, 43, 47,
        ]
        assert count_up_to(50) == expected

    def test_n_equals_1000(self):
        result = count_up_to(1000)
        # Verify all returned values are actually prime and less than 1000
        for p in result:
            assert p < 1000
            # Check primality by trial division
            if p < 2:
                continue
            for d in range(2, int(p ** 0.5) + 1):
                assert p % d != 0, f"{p} is not prime"
        # Verify no primes were missed: every prime < 1000 should be in result
        def is_prime(x):
            if x < 2:
                return False
            for d in range(2, int(x ** 0.5) + 1):
                if x % d == 0:
                    return False
            return True
        expected_primes = [x for x in range(1000) if is_prime(x)]
        assert result == expected_primes


class TestCountUpToInvalidInputs:
    """Test invalid inputs that violate the documented constraints."""

    @pytest.mark.parametrize("invalid_input", [
        -1,
        -10,
        -100,
    ])
    def test_negative_integer(self, invalid_input):
        """Negative integers are outside the documented 'non-negative' constraint.
        The current implementation silently returns [] for negative n because
        [True] * (n+1) produces an empty list and range(2, n) is empty.
        We document this actual behavior."""
        assert count_up_to(invalid_input) == []

    @pytest.mark.parametrize("invalid_input", [
        None,
        "abc",
        3.14,
        [2, 3],
        {"n": 5},
    ])
    def test_non_integer_types(self, invalid_input):
        """Non-integer types are invalid per the documented signature."""
        with pytest.raises((TypeError, ValueError)):
            count_up_to(invalid_input)


class TestCountUpToOutputProperties:
    """Test structural properties of the output regardless of specific values."""

    def test_output_is_always_a_list(self):
        for n in [0, 1, 2, 5, 10, 100]:
            result = count_up_to(n)
            assert isinstance(result, list)

    def test_output_is_sorted(self):
        for n in [5, 10, 20, 50, 100, 1000]:
            result = count_up_to(n)
            assert result == sorted(result)

    def test_no_duplicates(self):
        for n in [5, 10, 20, 50, 100]:
            result = count_up_to(n)
            assert len(result) == len(set(result))

    def test_all_elements_are_integers(self):
        for n in [5, 10, 20, 100]:
            result = count_up_to(n)
            for elem in result:
                assert isinstance(elem, int)

    def test_all_elements_are_strictly_less_than_n(self):
        for n in [5, 10, 20, 50, 100]:
            result = count_up_to(n)
            for elem in result:
                assert elem < n

    def test_all_elements_are_prime(self):
        def is_prime(x):
            if x < 2:
                return False
            for d in range(2, int(x ** 0.5) + 1):
                if x % d == 0:
                    return False
            return True

        for n in [5, 10, 20, 50, 100, 500]:
            result = count_up_to(n)
            for elem in result:
                assert is_prime(elem), f"{elem} is not prime"
