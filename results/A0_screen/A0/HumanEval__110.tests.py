import pytest
from solution import exchange


class TestExchangeBasic:
    """Test basic functionality of the exchange function."""

    def test_example_1(self):
        """Both lists have equal evens; exchange is possible."""
        assert exchange([1, 2, 3, 4], [1, 2, 3, 4]) == "YES"

    def test_example_2(self):
        """Not enough evens in lst2 to cover odds in lst1."""
        assert exchange([1, 2, 3, 4], [1, 5, 3, 4]) == "NO"

    def test_all_even_lst1(self):
        """lst1 already has all even numbers — always YES."""
        assert exchange([2, 4, 6], [1, 3, 5]) == "YES"

    def test_all_odd_lst1_no_evens_in_lst2(self):
        """lst1 has all odds but lst2 has no evens — NO."""
        assert exchange([1, 3, 5], [7, 9, 11]) == "NO"

    def test_exact_match(self):
        """Number of odds in lst1 equals number of evens in lst2 — YES."""
        # lst1 has 2 odds, lst2 has 2 evens
        assert exchange([1, 3, 2], [4, 6, 5]) == "YES"


class TestExchangeSingleElement:
    """Test with single-element lists."""

    def test_single_even_in_lst1(self):
        assert exchange([2], [1]) == "YES"

    def test_single_odd_in_lst1_with_even_in_lst2(self):
        assert exchange([1], [2]) == "YES"

    def test_single_odd_in_lst1_with_odd_in_lst2(self):
        assert exchange([1], [3]) == "NO"

    def test_single_even_in_lst1_with_odd_in_lst2(self):
        assert exchange([2], [3]) == "YES"


class TestExchangeEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_zero_is_even(self):
        """Zero should be treated as even."""
        assert exchange([0, 1, 3], [2, 4, 5]) == "YES"

    def test_negative_numbers(self):
        """Negative odd/even numbers should be handled correctly."""
        # lst1: [-1, 2] -> 1 odd; lst2: [-2, 3] -> 1 even => YES
        assert exchange([-1, 2], [-2, 3]) == "YES"

    def test_negative_numbers_not_enough(self):
        """Negative numbers where exchange is not possible."""
        # lst1: [-1, -3, 2] -> 2 odds; lst2: [-5, 3] -> 0 evens => NO
        assert exchange([-1, -3, 2], [-5, 3]) == "NO"

    def test_large_list_possible(self):
        """Large list where exchange is possible."""
        lst1 = [1, 3, 5, 7, 9, 2, 4, 6]  # 5 odds
        lst2 = [2, 4, 6, 8, 10, 1, 3, 5]  # 5 evens
        assert exchange(lst1, lst2) == "YES"

    def test_large_list_not_possible(self):
        """Large list where exchange is not possible."""
        lst1 = [1, 3, 5, 7, 9, 11, 13]  # 7 odds
        lst2 = [2, 4, 6, 1, 3, 5, 7]     # 3 evens
        assert exchange(lst1, lst2) == "NO"

    def test_lst1_empty_assumption(self):
        """Lists are assumed non-empty per docstring, but test anyway."""
        # This shouldn't happen per spec, but let's verify behavior
        assert exchange([], [2, 4, 6]) == "YES"

    def test_lst2_empty_assumption(self):
        """lst2 empty — no evens available."""
        assert exchange([1, 3, 5], []) == "NO"


class TestExchangeMoreScenarios:
    """Additional scenarios for thorough coverage."""

    def test_one_odd_one_even(self):
        assert exchange([1], [2]) == "YES"

    def test_two_odds_two_evens(self):
        assert exchange([1, 3], [2, 4]) == "YES"

    def test_three_odds_two_evens(self):
        assert exchange([1, 3, 5], [2, 4]) == "NO"

    def test_mixed_with_duplicates(self):
        """Lists with duplicate values."""
        # lst1: [1, 1, 2, 2] -> 2 odds; lst2: [2, 2, 4, 4] -> 4 evens => YES
        assert exchange([1, 1, 2, 2], [2, 2, 4, 4]) == "YES"

    def test_all_same_values(self):
        """All elements are the same value."""
        assert exchange([2, 2, 2], [2, 2, 2]) == "YES"

    def test_alternating_pattern(self):
        """Alternating odd/even pattern in lst1."""
        # lst1: [1, 2, 1, 2, 1] -> 3 odds; lst2: [2, 4, 6, 8, 10] -> 5 evens => YES
        assert exchange([1, 2, 1, 2, 1], [2, 4, 6, 8, 10]) == "YES"

    def test_boundary_equal_count(self):
        """Odds in lst1 exactly equals evens in lst2 — boundary case."""
        # lst1: [1, 3, 2] -> 2 odds; lst2: [4, 6, 5] -> 2 evens => YES
        assert exchange([1, 3, 2], [4, 6, 5]) == "YES"

    def test_off_by_one(self):
        """One more odd than available evens — NO."""
        # lst1: [1, 3, 5, 2] -> 3 odds; lst2: [4, 6, 7] -> 2 evens => NO
        assert exchange([1, 3, 5, 2], [4, 6, 7]) == "NO"

    def test_return_type_string(self):
        """Ensure return value is a string."""
        result_yes = exchange([2], [1])
        result_no = exchange([1], [3])
        assert isinstance(result_yes, str)
        assert isinstance(result_no, str)
        assert result_yes == "YES"
        assert result_no == "NO"
