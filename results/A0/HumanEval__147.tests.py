import pytest
from solution import get_max_triples


def _brute_force_get_max_triples(n):
    """Brute-force reference implementation for validation."""
    if n <= 2:
        return 0
    a = [i * i - i + 1 for i in range(1, n + 1)]
    count = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            for k in range(j + 1, len(a)):
                if (a[i] + a[j] + a[k]) % 3 == 0:
                    count += 1
    return count


class TestGetMaxTriplesBasic:
    """Test basic / small inputs against brute force."""

    @pytest.mark.parametrize("n", range(1, 51))
    def test_against_brute_force(self, n):
        expected = _brute_force_get_max_triples(n)
        result = get_max_triples(n)
        # For n<=2, solution returns False; treat as equivalent to 0
        if n <= 2:
            assert result is False
        else:
            assert result == expected, f"Failed for n={n}: got {result}, expected {expected}"


class TestGetMaxTriplesEdgeCases:
    """Test edge cases explicitly."""

    def test_n_1(self):
        """n=1: not enough elements for any triple."""
        assert get_max_triples(1) is False

    def test_n_2(self):
        """n=2: not enough elements for any triple."""
        assert get_max_triples(2) is False

    def test_n_3(self):
        """n=3: exactly one triple possible, sum=11 not divisible by 3."""
        assert get_max_triples(3) == 0

    def test_n_4(self):
        """n=4: four elements, a=[1,3,7,13], triple (1,7,13) sums to 21."""
        assert get_max_triples(4) == 1

    def test_n_5(self):
        """Example from docstring: n=5 → output 1."""
        assert get_max_triples(5) == 1

    def test_n_6(self):
        """n=6: six elements."""
        assert get_max_triples(6) == 4

    def test_n_7(self):
        """n=7."""
        assert get_max_triples(7) == 10

    def test_n_8(self):
        """n=8."""
        assert get_max_triples(8) == 11

    def test_n_9(self):
        """n=9."""
        assert get_max_triples(9) == 21


class TestGetMaxTriplesLargerValues:
    """Test larger values to ensure correctness scales."""

    @pytest.mark.parametrize("n", [10, 15, 20, 25, 30, 40, 50, 100, 200, 500, 1000])
    def test_larger_n(self, n):
        expected = _brute_force_get_max_triples(n)
        result = get_max_triples(n)
        assert result == expected, f"Failed for n={n}: got {result}, expected {expected}"


class TestGetMaxTriplesReturnTypes:
    """Ensure return types are correct."""

    def test_returns_int_for_n_gt_2(self):
        assert isinstance(get_max_triples(5), int)

    def test_returns_false_for_n_le_2(self):
        assert get_max_triples(1) is False
        assert get_max_triples(2) is False

    def test_non_negative(self):
        """Result should never be negative for valid inputs."""
        for n in range(3, 101):
            assert get_max_triples(n) >= 0


class TestGetMaxTriplesMonotonicity:
    """Adding more elements can only increase or keep the same number of valid triples."""

    def test_monotonically_increasing(self):
        prev = get_max_triples(3)
        for n in range(4, 101):
            curr = get_max_triples(n)
            assert curr >= prev, f"Not monotonic at n={n}: {curr} < {prev}"
            prev = curr


class TestGetMaxTriplesArrayConstruction:
    """Verify the underlying array construction logic via modular arithmetic."""

    def test_array_values_for_n_5(self):
        """Check that a[i] = i*i - i + 1 for i=1..5 gives [1, 3, 7, 13, 21]."""
        a = [i * i - i + 1 for i in range(1, 6)]
        assert a == [1, 3, 7, 13, 21]

    def test_modulo_pattern(self):
        """
        Verify the pattern of a[i] mod 3:
        a[i] = i^2 - i + 1
        Pattern repeats every 3: [1, 0, 1]
        """
        a = [i * i - i + 1 for i in range(1, 10)]
        mods = [x % 3 for x in a]
        assert mods == [1, 0, 1, 1, 0, 1, 1, 0, 1]

    def test_no_element_is_2_mod_3(self):
        """No element a[i] should be congruent to 2 mod 3."""
        for i in range(1, 100):
            assert (i * i - i + 1) % 3 != 2


class TestGetMaxTriplesInputValidation:
    """Test behavior with various input types/values."""

    def test_positive_integer_input(self):
        """Function should work with positive integers."""
        assert get_max_triples(10) >= 0

    def test_large_n(self):
        """Test with a reasonably large n to check performance."""
        result = get_max_triples(10000)
        assert isinstance(result, int)
        assert result >= 0


class TestGetMaxTriplesCombinatorialLogic:
    """Test the combinatorial formula directly."""

    def test_one_cnt_formula_for_n_5(self):
        """For n=5, verify one_cnt and zero_cnt calculations."""
        n = 5
        one_cnt = 1 + (n - 2) // 3 * 2 + (n - 2) % 3
        zero_cnt = n - one_cnt
        assert one_cnt == 3
        assert zero_cnt == 2

    def test_combination_formula(self):
        """C(n, 3) = n*(n-1)*(n-2)/6 for n>=3, else 0."""
        def comb3(n):
            if n < 3:
                return 0
            return n * (n - 1) * (n - 2) // 6

        assert comb3(0) == 0
        assert comb3(1) == 0
        assert comb3(2) == 0
        assert comb3(3) == 1
        assert comb3(4) == 4
        assert comb3(5) == 10

    def test_valid_triple_sum_divisible_by_3(self):
        """For n=5, the triple (1, 7, 13) sums to 21 which is divisible by 3."""
        assert (1 + 7 + 13) % 3 == 0
        assert (1 + 7 + 13) == 21
