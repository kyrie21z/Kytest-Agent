import pytest
from solution import count_bidirectional


class TestCountBidirectional:
    """Tests for the count_bidirectional function."""

    # --- Edge cases ---

    def test_empty_list(self):
        """An empty list should return 0."""
        assert count_bidirectional([]) == 0

    def test_single_tuple(self):
        """A list with only one tuple has no pairs, so result is 0."""
        assert count_bidirectional([(1, 2)]) == 0

    def test_two_tuples_no_match(self):
        """Two tuples where neither satisfies the condition."""
        assert count_bidirectional([(1, 2), (3, 4)]) == 0

    # --- Basic matching cases ---

    def test_one_matching_pair(self):
        """One pair where tuple2[0] == tuple1[1]."""
        # (1, 2) and (2, 3): tuple(1)[0]=2 == tuple(0)[1]=2 → match
        assert count_bidirectional([(1, 2), (2, 3)]) == 1

    def test_reverse_order_no_match(self):
        """When the matching direction is reversed, it still counts."""
        # (2, 3) and (1, 2): tuple(1)[0]=1 != tuple(0)[1]=3 → no match
        assert count_bidirectional([(2, 3), (1, 2)]) == 0

    def test_self_matching_tuple(self):
        """Tuple (a, a) can match with another tuple starting with a."""
        # (1, 1) and (1, 2): tuple(1)[0]=1 == tuple(0)[1]=1 → match
        assert count_bidirectional([(1, 1), (1, 2)]) == 1

    def test_identical_tuples(self):
        """Identical tuples: (a,b) and (a,b) → tuple2[0]==tuple1[1]?"""
        # (1, 2) and (1, 2): tuple(1)[0]=1 != tuple(0)[1]=2 → no match
        assert count_bidirectional([(1, 2), (1, 2)]) == 0

    def test_same_element_tuples(self):
        """Tuples with same elements: (1,1) and (1,1) → tuple2[0]=1 == tuple1[1]=1 → match."""
        assert count_bidirectional([(1, 1), (1, 1)]) == 1

    # --- Multiple pairs ---

    def test_multiple_matching_pairs(self):
        """Multiple pairs satisfy the condition."""
        # Pairs:
        #   (0,1)-(1,2): 1==1 ✓
        #   (0,1)-(2,3): 2!=1 ✗
        #   (0,1)-(3,4): 3!=1 ✗
        #   (1,2)-(2,3): 2==2 ✓
        #   (1,2)-(3,4): 3!=2 ✗
        #   (2,3)-(3,4): 3==3 ✓
        assert count_bidirectional([(0, 1), (1, 2), (2, 3), (3, 4)]) == 3

    def test_no_matches_in_longer_list(self):
        """No pairs match in a longer list."""
        assert count_bidirectional([(1, 2), (3, 4), (5, 6)]) == 0

    def test_all_pairs_match(self):
        """Every pair satisfies the condition when all tuples are identical (a,a)."""
        # All tuples are (1,1), so every pair has tuple2[0]=1 == tuple1[1]=1 → match.
        # With n tuples, there are n*(n-1)/2 pairs.
        result = count_bidirectional([(1, 1), (1, 1), (1, 1)])
        assert result == 3  # C(3,2) = 3

    def test_all_pairs_match_five_tuples(self):
        """Five identical (a,a) tuples: C(5,2) = 10 pairs, all match."""
        assert count_bidirectional([(7, 7)] * 5) == 10

    # --- Mixed scenarios ---

    def test_mixed_matches_and_non_matches(self):
        """Some pairs match, some don't."""
        # (1,2)-(2,3): tuple2[0]=2 == tuple1[1]=2 → ✓
        # (1,2)-(4,5): 4!=2 ✗
        # (1,2)-(6,7): 6!=2 ✗
        # (2,3)-(4,5): 4!=3 ✗
        # (2,3)-(6,7): 6!=3 ✗
        # (4,5)-(6,7): 6!=5 ✗
        assert count_bidirectional([(1, 2), (2, 3), (4, 5), (6, 7)]) == 1

    def test_duplicate_values_across_tuples(self):
        """Duplicate values across different tuples."""
        # (1,2)-(2,1): 2==2 ✓
        # (1,2)-(3,4): 3!=2 ✗
        # (1,2)-(4,5): 4!=2 ✗
        # (2,1)-(3,4): 3!=1 ✗
        # (2,1)-(4,5): 4!=1 ✗
        # (3,4)-(4,5): 4==4 ✓
        assert count_bidirectional([(1, 2), (2, 1), (3, 4), (4, 5)]) == 2

    # --- Larger lists ---

    def test_large_list_with_known_result(self):
        """Test with a larger list where we can manually verify."""
        # Chain: (1,2),(2,3),(3,4),(4,5),(5,6)
        # Adjacent pairs form chains: (1,2)-(2,3), (2,3)-(3,4), etc.
        # Non-adjacent: (1,2)-(3,4): 3!=2 ✗, etc.
        result = count_bidirectional([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])
        assert result == 4  # 4 adjacent chain links

    def test_list_with_many_duplicates(self):
        """List with many identical tuples."""
        # 5 copies of (1,1): C(5,2) = 10 pairs, all match since 1==1
        assert count_bidirectional([(1, 1)] * 5) == 10

    # --- Type and boundary considerations ---

    def test_negative_numbers(self):
        """Function works with negative numbers."""
        assert count_bidirectional([(-1, -2), (-2, -3)]) == 1

    def test_zero_elements(self):
        """Function works with zero values."""
        assert count_bidirectional([(0, 0), (0, 0)]) == 1

    def test_string_tuples(self):
        """Function works with string elements."""
        assert count_bidirectional([('a', 'b'), ('b', 'c')]) == 1

    def test_mixed_types(self):
        """Function works with mixed numeric types."""
        assert count_bidirectional([(1, 2), (2.0, 3)]) == 1

    def test_three_tuples_chained(self):
        """Three tuples forming a chain."""
        # (1,2)-(2,3): 2==2 ✓
        # (1,2)-(3,4): 3!=2 ✗
        # (2,3)-(3,4): 3==3 ✓
        assert count_bidirectional([(1, 2), (2, 3), (3, 4)]) == 2

    def test_four_tuples_complex(self):
        """Four tuples with complex matching pattern."""
        # (1,2),(2,3),(3,4),(4,5)
        # (1,2)-(2,3): 2==2 ✓
        # (1,2)-(3,4): 3!=2 ✗
        # (1,2)-(4,5): 4!=2 ✗
        # (2,3)-(3,4): 3==3 ✓
        # (2,3)-(4,5): 4!=3 ✗
        # (3,4)-(4,5): 4==4 ✓
        assert count_bidirectional([(1, 2), (2, 3), (3, 4), (4, 5)]) == 3
