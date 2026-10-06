import pytest
from solution import intersection


class TestIntersectionBasicSamples:
    """Tests from the docstring samples."""

    def test_sample_1(self):
        # intersection of (1,2) and (2,3) is (2,2), length 0, not prime
        assert intersection((1, 2), (2, 3)) == "NO"

    def test_sample_2(self):
        # intersection of (-1,1) and (0,4) is (0,1), length 1, not prime
        assert intersection((-1, 1), (0, 4)) == "NO"

    def test_sample_3(self):
        # intersection of (-3,-1) and (-5,5) is (-3,-1), length 2, prime
        assert intersection((-3, -1), (-5, 5)) == "YES"


class TestNoIntersection:
    """When intervals do not overlap, should return 'NO'."""

    def test_disjoint_positive(self):
        assert intersection((1, 2), (3, 4)) == "NO"

    def test_disjoint_negative(self):
        assert intersection((-5, -4), (-3, -2)) == "NO"

    def test_disjoint_across_zero(self):
        assert intersection((-2, -1), (1, 2)) == "NO"

    def test_adjacent_no_overlap(self):
        # (1,2) and (3,4) are adjacent but don't overlap
        assert intersection((1, 2), (3, 4)) == "NO"

    def test_one_point_touch(self):
        # (1,2) and (2,3) touch at point 2, intersection is (2,2), length 0
        assert intersection((1, 2), (2, 3)) == "NO"


class TestPrimeLengthIntersections:
    """When the intersection length is a prime number, return 'YES'."""

    def test_length_2_prime(self):
        # interval1=(1,5), interval2=(2,6) -> intersect=(2,5), len=3, prime
        assert intersection((1, 5), (2, 6)) == "YES"

    def test_length_3_prime(self):
        # interval1=(1,5), interval2=(2,6) -> intersect=(2,5), len=3, prime
        assert intersection((1, 5), (2, 6)) == "YES"

    def test_length_5_prime(self):
        # interval1=(0,7), interval2=(2,9) -> intersect=(2,7), len=5, prime
        assert intersection((0, 7), (2, 9)) == "YES"

    def test_length_7_prime(self):
        # interval1=(0,10), interval2=(3,13) -> intersect=(3,10), len=7, prime
        assert intersection((0, 10), (3, 13)) == "YES"

    def test_length_11_prime(self):
        # interval1=(0,15), interval2=(4,20) -> intersect=(4,15), len=11, prime
        assert intersection((0, 15), (4, 20)) == "YES"

    def test_length_13_prime(self):
        # interval1=(0,20), interval2=(7,25) -> intersect=(7,20), len=13, prime
        assert intersection((0, 20), (7, 25)) == "YES"


class TestNonPrimeLengthIntersections:
    """When the intersection length is not a prime number, return 'NO'."""

    def test_length_0(self):
        # identical touching points, length 0
        assert intersection((1, 2), (2, 3)) == "NO"

    def test_length_1(self):
        # intersection length = 1, not prime
        assert intersection((1, 3), (2, 4)) == "NO"

    def test_length_4(self):
        # intersection length = 4, not prime
        assert intersection((0, 6), (2, 8)) == "NO"  # intersect=(2,6), len=4

    def test_length_6(self):
        # intersection length = 6, not prime
        assert intersection((0, 8), (2, 10)) == "NO"  # intersect=(2,8), len=6

    def test_length_8(self):
        # intersection length = 8, not prime
        assert intersection((0, 10), (2, 12)) == "NO"  # intersect=(2,10), len=8

    def test_length_9(self):
        # intersection length = 9, not prime
        assert intersection((0, 12), (3, 15)) == "NO"  # intersect=(3,12), len=9

    def test_length_10(self):
        # intersection length = 10, not prime
        assert intersection((0, 14), (4, 18)) == "NO"  # intersect=(4,14), len=10


class TestIdenticalIntervals:
    """When both intervals are the same."""

    def test_same_interval_length_5(self):
        # intersect = same interval, length = 5, prime
        assert intersection((0, 5), (0, 5)) == "YES"

    def test_same_interval_length_4(self):
        # intersect = same interval, length = 4, not prime
        assert intersection((0, 4), (0, 4)) == "NO"

    def test_same_interval_length_1(self):
        # intersect = same interval, length = 1, not prime
        assert intersection((1, 2), (1, 2)) == "NO"

    def test_same_single_point(self):
        # single point interval, length = 0, not prime
        assert intersection((5, 5), (5, 5)) == "NO"


class TestReversedInputOrder:
    """The function should handle reversed argument order correctly."""

    def test_reversed_args(self):
        assert intersection((2, 3), (1, 2)) == "NO"

    def test_reversed_args_prime(self):
        assert intersection((2, 6), (1, 5)) == "YES"

    def test_reversed_args_large(self):
        assert intersection((-5, 5), (-3, -1)) == "YES"


class TestNegativeIntervals:
    """Test with negative numbers."""

    def test_both_negative(self):
        # interval1=(-5,-1), interval2=(-3,1) -> intersect=(-3,-1), len=2, prime
        assert intersection((-5, -1), (-3, 1)) == "YES"

    def test_both_negative_no_intersect(self):
        # interval1=(-10,-8), interval2=(-5,-3) -> no intersect
        assert intersection((-10, -8), (-5, -3)) == "NO"

    def test_crossing_zero(self):
        # interval1=(-3,3), interval2=(-1,5) -> intersect=(-1,3), len=4, not prime
        assert intersection((-3, 3), (-1, 5)) == "NO"

    def test_crossing_zero_prime_len3(self):
        # interval1=(-4,4), interval2=(-2,2) -> intersect=(-2,2), len=4, not prime
        assert intersection((-4, 4), (-2, 2)) == "NO"

    def test_crossing_zero_prime_len7(self):
        # interval1=(-5,5), interval2=(-3,4) -> intersect=(-3,4), len=7, prime
        assert intersection((-5, 5), (-3, 4)) == "YES"


class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_large_intervals(self):
        # intersect=(10,100), len=90, not prime
        assert intersection((0, 100), (10, 110)) == "NO"

    def test_exact_prime_boundary(self):
        # intersect=(0,101), len=101, prime
        assert intersection((0, 101), (0, 101)) == "YES"

    def test_one_contains_other_not_prime(self):
        # intersect = interval2 = (2,6), len=4, not prime
        assert intersection((0, 10), (2, 6)) == "NO"

    def test_one_contains_other_prime(self):
        # intersect = interval2 = (2,5), len=3, prime
        assert intersection((0, 10), (2, 5)) == "YES"

    def test_zero_length_intersection(self):
        # Touching at exactly one point
        assert intersection((1, 5), (5, 10)) == "NO"

    def test_completely_overlapping_not_prime(self):
        # intersect=(5,15), len=10, not prime
        assert intersection((0, 20), (5, 15)) == "NO"

    def test_completely_overlapping_prime(self):
        # intersect=(5,12), len=7, prime
        assert intersection((0, 20), (5, 12)) == "YES"


class TestSpecificPrimeValues:
    """Test for specific prime lengths to ensure correctness."""

    def test_prime_2(self):
        # length 2 is prime
        assert intersection((0, 4), (2, 6)) == "YES"  # intersect=(2,4), len=2

    def test_prime_3(self):
        # length 3 is prime
        assert intersection((0, 5), (2, 7)) == "YES"  # intersect=(2,5), len=3

    def test_prime_5(self):
        # length 5 is prime
        assert intersection((0, 7), (2, 9)) == "YES"  # intersect=(2,7), len=5

    def test_prime_7(self):
        # length 7 is prime
        assert intersection((0, 10), (3, 13)) == "YES"  # intersect=(3,10), len=7

    def test_prime_11(self):
        # length 11 is prime
        assert intersection((0, 15), (4, 20)) == "YES"  # intersect=(4,15), len=11

    def test_prime_13(self):
        # length 13 is prime
        assert intersection((0, 20), (7, 25)) == "YES"  # intersect=(7,20), len=13

    def test_prime_17(self):
        # length 17 is prime
        assert intersection((0, 25), (8, 30)) == "YES"  # intersect=(8,25), len=17

    def test_prime_19(self):
        # length 19 is prime
        assert intersection((0, 30), (11, 35)) == "YES"  # intersect=(11,30), len=19

    def test_prime_23(self):
        # length 23 is prime
        assert intersection((0, 35), (12, 40)) == "YES"  # intersect=(12,35), len=23


class TestCompositeLengths:
    """Test that composite (non-prime) lengths return 'NO'."""

    def test_length_4(self):
        assert intersection((0, 6), (2, 8)) == "NO"  # len=4

    def test_length_6(self):
        assert intersection((0, 8), (2, 10)) == "NO"  # len=6

    def test_length_8(self):
        assert intersection((0, 10), (2, 12)) == "NO"  # len=8

    def test_length_9(self):
        assert intersection((0, 12), (3, 15)) == "NO"  # len=9

    def test_length_10(self):
        assert intersection((0, 14), (4, 18)) == "NO"  # len=10

    def test_length_12(self):
        assert intersection((0, 18), (6, 24)) == "NO"  # len=12

    def test_length_14(self):
        assert intersection((0, 20), (6, 26)) == "NO"  # len=14

    def test_length_15(self):
        assert intersection((0, 22), (7, 29)) == "NO"  # len=15

    def test_length_16(self):
        assert intersection((0, 24), (8, 32)) == "NO"  # len=16

    def test_length_20(self):
        assert intersection((0, 30), (10, 40)) == "NO"  # len=20


class TestReturnTypes:
    """Ensure correct return types."""

    def test_returns_string_yes(self):
        result = intersection((0, 5), (0, 5))
        assert isinstance(result, str)
        assert result == "YES"

    def test_returns_string_no(self):
        result = intersection((1, 2), (3, 4))
        assert isinstance(result, str)
        assert result == "NO"
