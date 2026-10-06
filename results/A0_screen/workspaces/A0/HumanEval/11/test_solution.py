import pytest
from solution import string_xor


class TestStringXor:
    """Tests for the string_xor function."""

    def test_basic_example(self):
        """Test the example from the docstring."""
        assert string_xor('010', '110') == '100'

    def test_all_zeros(self):
        """XOR of all zeros should yield all zeros."""
        assert string_xor('0000', '0000') == '0000'

    def test_all_ones(self):
        """XOR of all ones should yield all zeros."""
        assert string_xor('1111', '1111') == '0000'

    def test_single_characters(self):
        """Test with single-character strings."""
        assert string_xor('0', '0') == '0'
        assert string_xor('0', '1') == '1'
        assert string_xor('1', '0') == '1'
        assert string_xor('1', '1') == '0'

    def test_longer_strings(self):
        """Test with longer binary strings."""
        assert string_xor('11111111', '00000000') == '11111111'
        assert string_xor('10101010', '01010101') == '11111111'
        assert string_xor('11001100', '11001100') == '00000000'

    def test_alternating_patterns(self):
        """Test with alternating bit patterns."""
        assert string_xor('1010', '1010') == '0000'
        assert string_xor('1010', '0101') == '1111'

    def test_mixed_bits(self):
        """Test with various mixed bit combinations."""
        assert string_xor('0011', '1100') == '1111'
        assert string_xor('0110', '1001') == '1111'
        assert string_xor('1001', '0110') == '1111'

    def test_one_bit_different(self):
        """Test where only one bit differs between the two strings."""
        assert string_xor('0000', '0001') == '0001'
        assert string_xor('0000', '0010') == '0010'
        assert string_xor('0000', '0100') == '0100'
        assert string_xor('0000', '1000') == '1000'

    def test_complement_strings(self):
        """Test with strings that are bitwise complements of each other."""
        assert string_xor('0000', '1111') == '1111'
        assert string_xor('1111', '0000') == '1111'
        assert string_xor('0101', '1010') == '1111'

    def test_identity_with_zeros(self):
        """XORing with all zeros should return the original string."""
        assert string_xor('10101', '00000') == '10101'
        assert string_xor('01010', '00000') == '01010'

    def test_self_xor_is_zero(self):
        """XORing a string with itself should always yield all zeros."""
        assert string_xor('11111', '11111') == '00000'
        assert string_xor('0101010101', '0101010101') == '0000000000'

    def test_equal_length_strings(self):
        """Ensure both strings must be the same length."""
        # The function iterates over range(len(a)), so it assumes equal length.
        # If lengths differ, it will raise an IndexError or produce unexpected results.
        # We test that equal-length strings work correctly.
        assert string_xor('10', '11') == '01'
        assert string_xor('01', '10') == '11'

    def test_docstring_example(self):
        """Verify the doctest example passes."""
        assert string_xor('010', '110') == '100'
