import pytest
from solution import is_multiply_prime


class TestIsMultiplyPrime:
    """Tests for the is_multiply_prime function."""

    # --- Edge cases ---

    def test_zero(self):
        assert is_multiply_prime(0) is False

    def test_one(self):
        assert is_multiply_prime(1) is False

    def test_negative(self):
        assert is_multiply_prime(-1) is False
        assert is_multiply_prime(-30) is False

    # --- Numbers that are products of exactly 3 primes ---

    def test_30(self):
        """30 = 2 * 3 * 5"""
        assert is_multiply_prime(30) is True

    def test_8(self):
        """8 = 2 * 2 * 2 (same prime repeated)"""
        assert is_multiply_prime(8) is True

    def test_12(self):
        """12 = 2 * 2 * 3"""
        assert is_multiply_prime(12) is True

    def test_27(self):
        """27 = 3 * 3 * 3"""
        assert is_multiply_prime(27) is True

    def test_42(self):
        """42 = 2 * 3 * 7"""
        assert is_multiply_prime(42) is True

    def test_105(self):
        """105 = 3 * 5 * 7"""
        assert is_multiply_prime(105) is True

    def test_98(self):
        """98 = 2 * 7 * 7"""
        assert is_multiply_prime(98) is True

    def test_99(self):
        """99 = 3 * 3 * 11"""
        assert is_multiply_prime(99) is True

    def test_18(self):
        """18 = 2 * 3 * 3 (exactly 3 primes)"""
        assert is_multiply_prime(18) is True

    def test_20(self):
        """20 = 2 * 2 * 5 (exactly 3 primes)"""
        assert is_multiply_prime(20) is True

    def test_50(self):
        """50 = 2 * 5 * 5 (exactly 3 primes)"""
        assert is_multiply_prime(50) is True

    def test_75(self):
        """75 = 3 * 5 * 5 (exactly 3 primes)"""
        assert is_multiply_prime(75) is True

    def test_60(self):
        """60 = 2 * 2 * 3 * 5 -> 4 prime factors counting multiplicity"""
        assert is_multiply_prime(60) is False

    def test_84(self):
        """84 = 2 * 2 * 3 * 7 -> 4 prime factors"""
        assert is_multiply_prime(84) is False

    # --- Numbers that are NOT products of exactly 3 primes ---

    def test_two_primes_product(self):
        """6 = 2 * 3 (only 2 primes)"""
        assert is_multiply_prime(6) is False

    def test_four_primes_product(self):
        """16 = 2 * 2 * 2 * 2 (4 primes)"""
        assert is_multiply_prime(16) is False

    def test_single_prime(self):
        """7 is prime itself (1 factor)"""
        assert is_multiply_prime(7) is False

    def test_prime_number(self):
        """13 is prime"""
        assert is_multiply_prime(13) is False

    def test_two_distinct_primes(self):
        """10 = 2 * 5 (2 primes)"""
        assert is_multiply_prime(10) is False

    def test_five_primes_product(self):
        """32 = 2^5 (5 primes)"""
        assert is_multiply_prime(32) is False

    def test_six_primes_product(self):
        """64 = 2^6 (6 primes)"""
        assert is_multiply_prime(64) is False

    def test_54(self):
        """54 = 2 * 3 * 3 * 3 (4 primes)"""
        assert is_multiply_prime(54) is False

    def test_100(self):
        """100 = 2 * 2 * 5 * 5 (4 primes)"""
        assert is_multiply_prime(100) is False

    # --- Boundary values ---

    def test_boundary_2(self):
        assert is_multiply_prime(2) is False

    def test_boundary_3(self):
        assert is_multiply_prime(3) is False

    def test_boundary_4(self):
        """4 = 2 * 2 (2 primes)"""
        assert is_multiply_prime(4) is False

    def test_boundary_5(self):
        assert is_multiply_prime(5) is False

    def test_boundary_9(self):
        """9 = 3 * 3 (2 primes)"""
        assert is_multiply_prime(9) is False

    def test_boundary_10(self):
        """10 = 2 * 5 (2 primes)"""
        assert is_multiply_prime(10) is False

    def test_boundary_14(self):
        """14 = 2 * 7 (2 primes)"""
        assert is_multiply_prime(14) is False

    def test_boundary_15(self):
        """15 = 3 * 5 (2 primes)"""
        assert is_multiply_prime(15) is False

    def test_boundary_21(self):
        """21 = 3 * 7 (2 primes)"""
        assert is_multiply_prime(21) is False

    def test_boundary_22(self):
        """22 = 2 * 11 (2 primes)"""
        assert is_multiply_prime(22) is False

    def test_boundary_25(self):
        """25 = 5 * 5 (2 primes)"""
        assert is_multiply_prime(25) is False

    def test_boundary_26(self):
        """26 = 2 * 13 (2 primes)"""
        assert is_multiply_prime(26) is False

    def test_boundary_33(self):
        """33 = 3 * 11 (2 primes)"""
        assert is_multiply_prime(33) is False

    def test_boundary_34(self):
        """34 = 2 * 17 (2 primes)"""
        assert is_multiply_prime(34) is False

    def test_boundary_35(self):
        """35 = 5 * 7 (2 primes)"""
        assert is_multiply_prime(35) is False

    def test_boundary_38(self):
        """38 = 2 * 19 (2 primes)"""
        assert is_multiply_prime(38) is False

    def test_boundary_39(self):
        """39 = 3 * 13 (2 primes)"""
        assert is_multiply_prime(39) is False

    def test_boundary_46(self):
        """46 = 2 * 23 (2 primes)"""
        assert is_multiply_prime(46) is False

    def test_boundary_51(self):
        """51 = 3 * 17 (2 primes)"""
        assert is_multiply_prime(51) is False

    def test_boundary_55(self):
        """55 = 5 * 11 (2 primes)"""
        assert is_multiply_prime(55) is False

    def test_boundary_57(self):
        """57 = 3 * 19 (2 primes)"""
        assert is_multiply_prime(57) is False

    def test_boundary_58(self):
        """58 = 2 * 29 (2 primes)"""
        assert is_multiply_prime(58) is False

    def test_boundary_62(self):
        """62 = 2 * 31 (2 primes)"""
        assert is_multiply_prime(62) is False

    def test_boundary_65(self):
        """65 = 5 * 13 (2 primes)"""
        assert is_multiply_prime(65) is False

    def test_boundary_69(self):
        """69 = 3 * 23 (2 primes)"""
        assert is_multiply_prime(69) is False

    def test_boundary_74(self):
        """74 = 2 * 37 (2 primes)"""
        assert is_multiply_prime(74) is False

    def test_boundary_77(self):
        """77 = 7 * 11 (2 primes)"""
        assert is_multiply_prime(77) is False

    def test_boundary_82(self):
        """82 = 2 * 41 (2 primes)"""
        assert is_multiply_prime(82) is False

    def test_boundary_85(self):
        """85 = 5 * 17 (2 primes)"""
        assert is_multiply_prime(85) is False

    def test_boundary_86(self):
        """86 = 2 * 43 (2 primes)"""
        assert is_multiply_prime(86) is False

    def test_boundary_87(self):
        """87 = 3 * 29 (2 primes)"""
        assert is_multiply_prime(87) is False

    def test_boundary_91(self):
        """91 = 7 * 13 (2 primes)"""
        assert is_multiply_prime(91) is False

    def test_boundary_93(self):
        """93 = 3 * 31 (2 primes)"""
        assert is_multiply_prime(93) is False

    def test_boundary_94(self):
        """94 = 2 * 47 (2 primes)"""
        assert is_multiply_prime(94) is False

    def test_boundary_95(self):
        """95 = 5 * 19 (2 primes)"""
        assert is_multiply_prime(95) is False
