"""Unit tests for solution.count_bidirectional."""

import pytest
from solution import count_bidirectional


class TestCountBidirectionalEmptyAndSingle:
    """Tests for empty lists and single-element lists."""

    def test_empty_list(self):
        assert count_bidirectional([]) == 0

    def test_single_tuple(self):
        assert count_bidirectional([(1, 2)]) == 0


class TestCountBidirectionalBasicPairs:
    """Tests for basic bidirectional pair detection."""

    def test_one_matching_pair(self):
        """Two tuples where second[0] == first[1]."""
        result = count_bidirectional([(1, 2), (2, 3)])
        assert result == 1

    def test_no_matching_pair(self):
        """Two tuples where no match exists."""
        result = count_bidirectional([(1, 2), (3, 4)])
        assert result == 0

    def test_two_identical_tuples(self):
        """Identical tuples: (1,2) and (1,2) -> second[0]=1 != first[1]=2."""
        result = count_bidirectional([(1, 2), (1, 2)])
        assert result == 0

    def test_reverse_pair(self):
        """Classic bidirectional: (1,2) and (2,1) -> second[0]=2 == first[1]=2."""
        result = count_bidirectional([(1, 2), (2, 1)])
        assert result == 1


class TestCountBidirectionalMultiplePairs:
    """Tests with multiple tuples and various combinations."""

    def test_multiple_matching_pairs(self):
        """Three tuples forming two matching pairs."""
        # (1,2),(2,3) -> match (2==2)
        # (1,2),(3,4) -> no match (3!=2)
        # (2,3),(3,4) -> match (3==3)
        result = count_bidirectional([(1, 2), (2, 3), (3, 4)])
        assert result == 2

    def test_chain_of_tuples(self):
        """A chain where each tuple's second element matches the next's first."""
        # Pairs: (1,2)-(2,3)✓, (1,2)-(3,4)✗, (1,2)-(4,5)✗,
        #        (2,3)-(3,4)✓, (2,3)-(4,5)✗, (3,4)-(4,5)✓
        result = count_bidirectional([(1, 2), (2, 3), (3, 4), (4, 5)])
        assert result == 3

    def test_no_matches_in_long_list(self):
        """Long list with no matching pairs."""
        result = count_bidirectional([(1, 2), (3, 4), (5, 6), (7, 8)])
        assert result == 0


class TestCountBidirectionalEdgeCases:
    """Tests for edge cases and special values."""

    def test_zero_values(self):
        """Tuples containing zero: (0,0) and (0,0) -> second[0]=0 == first[1]=0 ✓"""
        result = count_bidirectional([(0, 0), (0, 0)])
        assert result == 1

    def test_negative_numbers(self):
        """Tuples with negative numbers."""
        result = count_bidirectional([(-1, -2), (-2, -3)])
        assert result == 1

    def test_mixed_positive_negative(self):
        """Mix of positive and negative numbers."""
        result = count_bidirectional([(1, -1), (-1, 1)])
        assert result == 1

    def test_large_numbers(self):
        """Tuples with large integer values."""
        result = count_bidirectional([(10**9, 10**9 + 1), (10**9 + 1, 10**9 + 2)])
        assert result == 1

    def test_string_tuples(self):
        """Tuples containing strings."""
        result = count_bidirectional([('a', 'b'), ('b', 'c')])
        assert result == 1

    def test_mixed_type_tuples(self):
        """Tuples with mixed types (int and str)."""
        result = count_bidirectional([(1, 'a'), ('a', 2)])
        assert result == 1

    def test_boolean_values(self):
        """Tuples with boolean values."""
        result = count_bidirectional([(True, False), (False, True)])
        assert result == 1

    def test_none_values(self):
        """Tuples containing None."""
        result = count_bidirectional([(None, 'x'), ('x', None)])
        assert result == 1


class TestCountBidirectionalDuplicates:
    """Tests involving duplicate tuples in the list."""

    def test_duplicate_matching_tuples(self):
        """Duplicate identical tuples that don't form matching pairs."""
        result = count_bidirectional([(1, 2), (1, 2), (1, 2)])
        assert result == 0

    def test_duplicate_bidirectional_pairs(self):
        """Multiple copies of bidirectional pairs."""
        # Tuples: (1,2), (2,1), (1,2), (2,1)
        # All cross-pairs between {first,(1,2)} and {(2,1)} match, etc.
        result = count_bidirectional([(1, 2), (2, 1), (1, 2), (2, 1)])
        assert result == 4

    def test_triplicate_same_tuple(self):
        """Three identical self-loop tuples."""
        result = count_bidirectional([(5, 5), (5, 5), (5, 5)])
        # Each pair: second[0]=5, first[1]=5 -> 5==5 ✓
        # C(3,2) = 3 pairs, all match
        assert result == 3


class TestCountBidirectionalComplexScenarios:
    """More complex real-world scenarios."""

    def test_graph_edges(self):
        """Simulating directed graph edges; count pairs where edge B starts
        where edge A ends (i.e., potential path continuations)."""
        edges = [(1, 2), (2, 3), (3, 1), (4, 5)]
        result = count_bidirectional(edges)
        assert result == 2

    def test_self_loops(self):
        """Tuples where first == second (self-loops)."""
        result = count_bidirectional([(1, 1), (1, 1)])
        assert result == 1

    def test_three_way_chain(self):
        """A three-way chain of connections."""
        result = count_bidirectional([(1, 2), (2, 3), (3, 4)])
        assert result == 2

    def test_cyclic_pattern(self):
        """Cyclic pattern: (1,2),(2,3),(3,1)."""
        result = count_bidirectional([(1, 2), (2, 3), (3, 1)])
        assert result == 2

    def test_wide_list_no_matches(self):
        """Wide list with many tuples but no matches."""
        tuples = [(i, i + 10) for i in range(1, 11)]
        result = count_bidirectional(tuples)
        assert result == 0

    def test_wide_list_some_matches(self):
        """Wide list with some matches (chain of 10 tuples)."""
        tuples = [(i, i + 1) for i in range(1, 11)]
        result = count_bidirectional(tuples)
        assert result == 9


class TestCountBidirectionalReturnTypes:
    """Tests verifying return type correctness."""

    def test_returns_integer(self):
        result = count_bidirectional([(1, 2)])
        assert isinstance(result, int)

    def test_returns_non_negative(self):
        """Result should never be negative."""
        result = count_bidirectional([(1, 2), (3, 4), (5, 6)])
        assert result >= 0

    def test_result_within_bounds(self):
        """Result should be <= C(n,2) for n tuples."""
        n = 5
        tuples = [(i, i + 1) for i in range(n)]
        max_possible = n * (n - 1) // 2
        result = count_bidirectional(tuples)
        assert result <= max_possible
