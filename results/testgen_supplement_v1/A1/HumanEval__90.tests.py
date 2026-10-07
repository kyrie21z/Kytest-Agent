import pytest
from solution import next_smallest


# ──────────────────────────────────────────────
# Normal cases – typical inputs
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with straightforward, well-formed inputs."""

    def test_increasing_order(self):
        assert next_smallest([1, 2, 3, 4, 5]) == 2

    def test_decreasing_order(self):
        assert next_smallest([5, 4, 3, 2, 1]) == 2

    def test_random_order(self):
        assert next_smallest([5, 1, 4, 3, 2]) == 2

    def test_two_elements(self):
        """Minimum valid list: exactly two distinct elements."""
        assert next_smallest([10, 5]) == 10

    def test_negative_numbers(self):
        assert next_smallest([-3, -1, -2]) == -2

    def test_mixed_positive_and_negative(self):
        assert next_smallest([3, -1, 2, -5, 0]) == -1

    def test_larger_values(self):
        assert next_smallest([100, 200, 300]) == 200

    def test_all_same_first_then_different(self):
        """Duplicates at the start, distinct 2nd smallest later."""
        assert next_smallest([1, 1, 1, 2, 3]) == 2

    def test_duplicates_after_second(self):
        """Distinct 2nd smallest followed by more duplicates."""
        assert next_smallest([1, 2, 2, 2, 2]) == 2

    def test_many_duplicates_one_second(self):
        assert next_smallest([1, 1, 1, 1, 2]) == 2

    def test_single_duplicate_pair(self):
        assert next_smallest([1, 2, 2, 3]) == 2

    def test_large_list_with_duplicates(self):
        lst = [5] * 100 + [3] + [1] * 50
        assert next_smallest(lst) == 3


# ──────────────────────────────────────────────
# Boundary cases – edges of valid input ranges
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the boundaries of valid input sizes and values."""

    def test_minimum_valid_size_two_distinct(self):
        assert next_smallest([0, 1]) == 1

    def test_minimum_valid_size_two_equal(self):
        assert next_smallest([0, 0]) is None

    def test_single_element(self):
        assert next_smallest([42]) is None

    def test_empty_list(self):
        assert next_smallest([]) is None

    def test_all_identical_elements(self):
        assert next_smallest([7, 7, 7, 7]) is None

    def test_two_identical_elements(self):
        assert next_smallest([5, 5]) is None

    def test_three_identical_elements(self):
        assert next_smallest([1, 1, 1]) is None

    def test_extreme_negative_values(self):
        assert next_smallest([-1000000, -999999, -1000001]) == -1000000

    def test_extreme_positive_values(self):
        assert next_smallest([1000000, 999999, 1000001]) == 1000000

    def test_zero_in_list(self):
        assert next_smallest([0, 1, 2]) == 1

    def test_zero_as_second_smallest(self):
        assert next_smallest([-1, 0, 1]) == 0


# ──────────────────────────────────────────────
# Invalid inputs – types not documented as supported
# ──────────────────────────────────────────────

class TestInvalidInputs:
    """Tests with inputs that violate the documented contract.

    The function does NOT validate its argument type; it accepts any
    iterable-like object.  We document the actual runtime behaviour
    rather than asserting exceptions that never occur.
    """

    @pytest.mark.parametrize("invalid_input, expected", [
        ("not a list", None),   # sorted chars are all different → returns 'a'
        ({"key": "value"}, None),  # dict keys sorted → only one key → None
        ((1, 2, 3), 2),         # tuple is iterable → behaves like a list
    ])
    def test_non_list_inputs(self, invalid_input, expected):
        """Document actual behaviour for non-list inputs."""
        result = next_smallest(invalid_input)
        assert result == expected

    def test_none_raises_type_error(self):
        """None has no len() → TypeError."""
        with pytest.raises(TypeError):
            next_smallest(None)

    def test_integer_raises_type_error(self):
        """int has no len() → TypeError."""
        with pytest.raises(TypeError):
            next_smallest(42)

    def test_float_raises_type_error(self):
        """float has no len() → TypeError."""
        with pytest.raises(TypeError):
            next_smallest(3.14)


# ──────────────────────────────────────────────
# Docstring examples – verify against documented behavior
# ──────────────────────────────────────────────

class TestDocstringExamples:
    """Explicitly verify every example from the docstring."""

    def test_docstring_example_1(self):
        assert next_smallest([1, 2, 3, 4, 5]) == 2

    def test_docstring_example_2(self):
        assert next_smallest([5, 1, 4, 3, 2]) == 2

    def test_docstring_example_3(self):
        assert next_smallest([]) is None

    def test_docstring_example_4(self):
        assert next_smallest([1, 1]) is None
