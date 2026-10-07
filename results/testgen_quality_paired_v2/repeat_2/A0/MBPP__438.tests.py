import pytest
from solution import count_bidirectional


class TestCountBidirectional:
    """Tests for the count_bidirectional function."""

    def test_empty_list(self):
        """Empty input should return 0."""
        assert count_bidirectional([]) == 0

    def test_single_tuple(self):
        """A single tuple cannot form a pair."""
        assert count_bidirectional([(1, 2)]) == 0

    def test_no_bidirectional_pairs(self):
        """No matching reverse pairs should return 0."""
        result = count_bidirectional([(1, 2), (3, 4), (5, 6)])
        assert result == 0

    def test_one_bidirectional_pair(self):
        """One pair where tuple2[0] == tuple1[1] should return 1."""
        result = count_bidirectional([(1, 2), (2, 1)])
        assert result == 1

    def test_multiple_bidirectional_pairs(self):
        """Multiple distinct pairs satisfying the condition."""
        result = count_bidirectional([
            (1, 2), (2, 1),
            (3, 4), (4, 3),
            (5, 6), (6, 5)
        ])
        assert result == 3

    def test_duplicate_tuples(self):
        """Duplicate tuples should each be counted as separate entries."""
        # [(1,2), (2,1), (2,1)] -> two pairs: (idx0,idx1) and (idx0,idx2)
        result = count_bidirectional([(1, 2), (2, 1), (2, 1)])
        assert result == 2

    def test_self_reverse_tuples(self):
        """Tuples where a == b still match when paired with identical tuples."""
        # (1,1) & (1,1): 1==1 -> yes
        result = count_bidirectional([(1, 1), (1, 1)])
        assert result == 1

    def test_mixed_valid_and_invalid(self):
        """Mix of valid pairs and non-pairs."""
        result = count_bidirectional([
            (1, 2), (2, 1),   # valid pair: 2==2
            (3, 4),           # no reverse
            (5, 6), (6, 5),   # valid pair: 6==6
        ])
        assert result == 2

    def test_larger_values(self):
        """Test with larger integer values."""
        result = count_bidirectional([
            (100, 200), (200, 100),
            (-1, 1), (1, -1),
        ])
        assert result == 2

    def test_negative_numbers(self):
        """Test with negative numbers."""
        result = count_bidirectional([(-3, -5), (-5, -3)])
        assert result == 1

    def test_zero_values(self):
        """Test with zero: (0,0) & (0,0) -> 0==0 -> yes."""
        result = count_bidirectional([(0, 0), (0, 0)])
        assert result == 1

    def test_string_tuples(self):
        """Test with string elements."""
        result = count_bidirectional([('a', 'b'), ('b', 'a')])
        assert result == 1

    def test_mixed_type_tuples(self):
        """Test with mixed types inside tuples."""
        result = count_bidirectional([(1, 'a'), ('a', 1)])
        assert result == 1

    def test_unordered_input(self):
        """Same set of tuples in different orders should yield same result."""
        result1 = count_bidirectional([(1, 2), (2, 1), (3, 4), (4, 3)])
        result2 = count_bidirectional([(2, 1), (4, 3), (1, 2), (3, 4)])
        assert result1 == result2 == 2

    def test_many_duplicates_of_same_pair(self):
        """Many duplicates of the same bidirectional pair."""
        pairs = [(1, 2)] * 5 + [(2, 1)] * 5
        # Each (1,2) at indices 0-4 pairs with each (2,1) at indices 5-9
        # That's 5 * 5 = 25 pairs
        result = count_bidirectional(pairs)
        assert result == 25

    def test_partial_overlap(self):
        """Some tuples have reverses, others don't."""
        # [(1,2),(2,1),(2,3),(3,4),(4,3)]
        # (1,2)&(2,1): 2==2 ✓
        # (1,2)&(2,3): 2==2 ✓
        # (1,2)&(3,4): 3==2 ✗
        # (1,2)&(4,3): 4==2 ✗
        # (2,1)&(2,3): 2==1 ✗
        # (2,1)&(3,4): 3==1 ✗
        # (2,1)&(4,3): 4==1 ✗
        # (2,3)&(3,4): 3==3 ✓
        # (2,3)&(4,3): 4==3 ✗
        # (3,4)&(4,3): 4==4 ✓
        result = count_bidirectional([
            (1, 2), (2, 1),
            (2, 3),
            (3, 4), (4, 3),
        ])
        assert result == 4

    def test_all_same_element_pairs(self):
        """All tuples are (x, x); every pair matches since x==x."""
        # (1,1)&(1,1): 1==1 ✓, (1,1)&(1,1): 1==1 ✓, (1,1)&(1,1): 1==1 ✓
        result = count_bidirectional([(1, 1), (1, 1), (1, 1)])
        assert result == 3
