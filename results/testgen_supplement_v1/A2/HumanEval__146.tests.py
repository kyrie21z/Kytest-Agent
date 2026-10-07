import pytest
from solution import specialFilter


# ──────────────────────────────────────────────
# 1. Normal / typical inputs
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with typical, non-edge-case inputs."""

    def test_example_1(self):
        # [15, -73, 14, -15] => only 15 qualifies (>10, first='1', last='5')
        assert specialFilter([15, -73, 14, -15]) == 1

    def test_example_2(self):
        # [33, -2, -3, 45, 21, 109] => 33 and 109 qualify
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2

    def test_all_qualify(self):
        # All numbers are > 10 with odd first & last digits
        assert specialFilter([11, 33, 55, 77, 99]) == 5

    def test_none_qualify(self):
        # No number satisfies all conditions
        assert specialFilter([1, 2, 3, 4, 5]) == 0

    def test_mixed_positive_and_negative(self):
        # Positive qualifying + negative numbers (negatives never qualify)
        assert specialFilter([11, -11, 33, -33, 55, -55]) == 3

    def test_even_first_digit(self):
        # First digit is even → does not qualify
        assert specialFilter([21, 23, 25, 27, 29]) == 0

    def test_even_last_digit(self):
        # Last digit is even → does not qualify
        assert specialFilter([12, 32, 52, 72, 92]) == 0

    def test_large_numbers(self):
        # Multi-digit numbers with odd first/last
        assert specialFilter([111, 333, 555, 777, 999]) == 5

    def test_single_qualifier_in_large_list(self):
        assert specialFilter([1, 2, 3, 11, 5, 6, 7]) == 1


# ──────────────────────────────────────────────
# 2. Boundary cases
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_number_exactly_10(self):
        # 10 is NOT > 10, so it does not qualify
        assert specialFilter([10]) == 0

    def test_number_exactly_11(self):
        # 11 > 10, first='1', last='1' → qualifies
        assert specialFilter([11]) == 1

    def test_number_exactly_9(self):
        # 9 is NOT > 10
        assert specialFilter([9]) == 0

    def test_two_digit_boundary_odd_odd(self):
        # Smallest two-digit number with odd first & last
        assert specialFilter([11]) == 1

    def test_two_digit_boundary_even_even(self):
        # Largest two-digit number with even first & last
        assert specialFilter([88]) == 0

    def test_three_digit_smallest(self):
        # 101: > 10, first='1', last='1' → qualifies
        assert specialFilter([101]) == 1

    def test_three_digit_largest(self):
        # 999: > 10, first='9', last='9' → qualifies
        assert specialFilter([999]) == 1

    def test_number_with_zero_middle(self):
        # 101 has zero in middle but still qualifies
        assert specialFilter([101, 303, 505]) == 3

    def test_number_with_zero_last(self):
        # 10: last digit is '0' (even), doesn't qualify
        assert specialFilter([10]) == 0

    def test_number_with_zero_first_impossible(self):
        # No positive integer has '0' as first digit in normal repr
        assert specialFilter([0]) == 0


# ──────────────────────────────────────────────
# 3. Empty, null, or zero-size inputs
# ──────────────────────────────────────────────

class TestEmptyAndZeroInputs:
    """Tests for empty lists, single-element lists, etc."""

    def test_empty_list(self):
        assert specialFilter([]) == 0

    def test_single_element_qualifies(self):
        assert specialFilter([11]) == 1

    def test_single_element_does_not_qualify(self):
        assert specialFilter([5]) == 0

    def test_single_negative(self):
        assert specialFilter([-11]) == 0

    def test_single_zero(self):
        assert specialFilter([0]) == 0

    def test_single_ten(self):
        assert specialFilter([10]) == 0

    def test_single_eleven(self):
        assert specialFilter([11]) == 1


# ──────────────────────────────────────────────
# 4. Invalid / unusual inputs
# ──────────────────────────────────────────────

class TestUnusualInputs:
    """Tests with values that might seem unusual but are valid."""

    def test_all_zeros(self):
        assert specialFilter([0, 0, 0]) == 0

    def test_all_same_value(self):
        assert specialFilter([11, 11, 11]) == 3

    def test_all_same_non_qualifying(self):
        assert specialFilter([22, 22, 22]) == 0

    def test_negative_qualifying_digits(self):
        # -11: str("-11")[0] = '-', not in odd set → doesn't qualify
        assert specialFilter([-11, -33, -55]) == 0

    def test_mixed_signs_with_qualifiers(self):
        # Only positive ones can qualify
        assert specialFilter([11, -11, 33, -33]) == 2

    def test_duplicate_values(self):
        assert specialFilter([11, 11, 33, 33, 33]) == 5

    def test_alternating_qualify_skip(self):
        assert specialFilter([11, 12, 13, 14, 15]) == 3  # 11, 13, 15


# ──────────────────────────────────────────────
# 5. Exception cases
# ──────────────────────────────────────────────

class TestExceptionCases:
    """Tests that the function handles or raises on invalid types."""

    def test_none_input_raises(self):
        with pytest.raises(TypeError):
            specialFilter(None)

    def test_string_input_raises(self):
        with pytest.raises(TypeError):
            specialFilter("hello")

    def test_integer_input_raises(self):
        with pytest.raises(TypeError):
            specialFilter(42)

    def test_nested_list_raises(self):
        with pytest.raises(TypeError):
            specialFilter([[11]])

    def test_tuple_input_works(self):
        # Tuples are iterable; str() works on each element
        assert specialFilter((11, 33)) == 2

    def test_generator_input_works(self):
        assert specialFilter(x for x in [11, 33, 55]) == 3

    def test_float_input(self):
        # Floats: str(11.5) = "11.5", first='1', last='5' → qualifies
        # But 11.5 > 10 → yes
        assert specialFilter([11.5]) == 1

    def test_float_no_decimal(self):
        # str(11.0) = "11.0", last='0' (even) → doesn't qualify
        assert specialFilter([11.0]) == 0

    def test_dict_iterates_over_keys(self):
        # Iterating over a dict yields keys. {1: 2} → key 1, which is <= 10
        assert specialFilter({1: 2}) == 0
