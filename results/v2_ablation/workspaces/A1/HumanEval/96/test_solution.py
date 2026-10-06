"""Unit tests for count_up_to in solution.py."""

import pytest
from solution import count_up_to


class TestCountUpToNormalCases:
    """Tests with typical, documented inputs."""

    def test_n_equals_5(self):
        assert count_up_to(5) == [2, 3]

    def test_n_equals_11(self):
        assert count_up_to(11) == [2, 3, 5, 7]

    def test_n_equals_20(self):
        assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_n_equals_18(self):
        assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]

    def test_n_equals_10(self):
        assert count_up_to(10) == [2, 3, 5, 7]

    def test_n_equals_30(self):
        assert count_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


class TestCountUpToBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_n_equals_2(self):
        # No primes strictly less than 2
        assert count_up_to(2) == []

    def test_n_equals_3(self):
        # Only 2 is prime and less than 3
        assert count_up_to(3) == [2]

    def test_n_equals_4(self):
        assert count_up_to(4) == [2, 3]

    def test_n_equals_6(self):
        assert count_up_to(6) == [2, 3, 5]

    def test_n_equals_100(self):
        expected = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97
        ]
        assert count_up_to(100) == expected


class TestCountUpToEmptyAndZeroInputs:
    """Tests for zero and empty-like inputs."""

    def test_n_equals_0(self):
        # No primes less than 0
        assert count_up_to(0) == []

    def test_n_equals_1(self):
        # No primes less than 1
        assert count_up_to(1) == []


class TestCountUpToInvalidInputs:
    """Tests for invalid inputs that should raise exceptions."""

    @pytest.mark.parametrize("invalid_input", [
        -1,
        -10,
        -100,
    ])
    def test_negative_integer(self, invalid_input):
        """Negative integers are outside the documented 'non-negative' constraint.
        The function may or may not raise; we document the behavior."""
        # The function does NOT raise for negative n because:
        #   [True] * 0 = [] when n=-1, range(2, -1) is empty.
        # However, per the docstring, n must be non-negative.
        # We test that it returns [] for n < 0 as a practical observation.
        result = count_up_to(invalid_input)
        assert result == []

    def test_none_input(self):
        """Passing None should raise TypeError."""
        with pytest.raises(TypeError):
            count_up_to(None)

    def test_string_input(self):
        """Passing a string should raise TypeError."""
        with pytest.raises(TypeError):
            count_up_to("5")

    def test_float_input(self):
        """Passing a float should raise TypeError."""
        with pytest.raises(TypeError):
            count_up_to(5.0)

    def test_list_input(self):
        """Passing a list should raise TypeError."""
        with pytest.raises(TypeError):
            count_up_to([5])

    def test_dict_input(self):
        """Passing a dict should raise TypeError."""
        with pytest.raises(TypeError):
            count_up_to({})


class TestCountUpToLargerValues:
    """Tests with larger inputs to verify correctness at scale."""

    def test_n_equals_50(self):
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        assert count_up_to(50) == expected

    def test_n_equals_1000(self):
        # Generate expected primes less than 1000 using a simple method
        def simple_primes(limit):
            primes = []
            for num in range(2, limit):
                is_prime = True
                for p in range(2, int(num ** 0.5) + 1):
                    if num % p == 0:
                        is_prime = False
                        break
                if is_prime:
                    primes.append(num)
            return primes

        assert count_up_to(1000) == simple_primes(1000)

    def test_result_is_sorted(self):
        """Primes should always be returned in ascending order."""
        result = count_up_to(100)
        assert result == sorted(result)

    def test_all_elements_are_prime(self):
        """Every element in the result must be a prime number."""
        result = count_up_to(200)
        for num in result:
            if num < 2:
                continue
            for i in range(2, int(num ** 0.5) + 1):
                assert num % i != 0, f"{num} is not prime"

    def test_no_composite_numbers(self):
        """No composite numbers should appear in the result."""
        composites = {4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 25}
        result = count_up_to(30)
        for c in composites:
            assert c not in result, f"{c} should not be in the result"

    def test_result_length_for_n_100(self):
        """There are exactly 25 primes less than 100."""
        assert len(count_up_to(100)) == 25

    def test_result_length_for_n_50(self):
        """There are exactly 15 primes less than 50."""
        assert len(count_up_to(50)) == 15
