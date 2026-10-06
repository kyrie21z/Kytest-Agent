"""Unit tests for solution.py — encode_shift and decode_shift functions."""

import pytest
from solution import encode_shift, decode_shift


# ---------------------------------------------------------------------------
# encode_shift tests
# ---------------------------------------------------------------------------

class TestEncodeShift:
    """Tests for the encode_shift function."""

    def test_basic_lowercase(self):
        """Shifting each lowercase letter forward by 5 positions."""
        # a->f, b->g, c->h
        assert encode_shift("abc") == "fgh"

    def test_single_character_a(self):
        """Encoding the first lowercase letter."""
        assert encode_shift("a") == "f"

    def test_single_character_z(self):
        """Encoding the last lowercase letter wraps around."""
        # z(122): ((122+5-97)%26)+97 = (30%26)+97 = 4+97 = 101 = 'e'
        assert encode_shift("z") == "e"

    def test_wrap_around_vwx(self):
        """Characters near 'z' wrap around to the beginning of the alphabet."""
        # v(118)->a, w(119)->b, x(120)->c
        assert encode_shift("vwx") == "abc"

    def test_wrap_around_xyz(self):
        """More wrap-around examples."""
        # y(121)->d, z(122)->e
        assert encode_shift("xyz") == "cde"

    def test_empty_string(self):
        """An empty string should return an empty string."""
        assert encode_shift("") == ""

    def test_all_lowercase_letters(self):
        """Every lowercase letter is shifted by 5."""
        result = encode_shift("abcdefghijklmnopqrstuvwxyz")
        expected = "fghijklmnopqrstuvwxyzabcde"
        assert result == expected

    def test_round_trip_lowercase_only(self):
        """Decoding an encoded string yields the original for lowercase-only input."""
        original = "hello"
        encoded = encode_shift(original)
        decoded = decode_shift(encoded)
        assert decoded == original

    def test_round_trip_identity_longer_text(self):
        """Round-trip works for longer lowercase-only strings."""
        original = "abcdefghijklmnopqrstuvwxyz"
        assert decode_shift(encode_shift(original)) == original

    def test_round_trip_with_spaces_fails(self):
        """Round-trip does NOT preserve spaces because encode always outputs lowercase."""
        original = "hello world"
        encoded = encode_shift(original)
        decoded = decode_shift(encoded)
        assert decoded != original
        assert " " not in decoded

    def test_numbers_are_also_shifted(self):
        """Numbers are shifted by the same formula (producing lowercase letters)."""
        encoded = encode_shift("123")
        assert encoded.isalpha()
        assert len(encoded) == 3

    def test_decode_is_inverse_of_encode_for_lowercase(self):
        """encode_shift(decode_shift(s)) == s when s is all lowercase."""
        encoded = "fghijklmnopqrstuvwxyzabcde"
        assert encode_shift(decode_shift(encoded)) == encoded

    def test_decode_shift_basic(self):
        """decode_shift reverses encode_shift correctly."""
        assert decode_shift("fgh") == "abc"

    def test_decode_shift_wrap_around(self):
        """Decoding characters that wrapped around during encoding."""
        assert decode_shift("abc") == "vwx"

    def test_decode_shift_empty(self):
        """Decoding an empty string returns an empty string."""
        assert decode_shift("") == ""

    def test_decode_shift_all_lowercase(self):
        """Decoding all lowercase encoded letters."""
        result = decode_shift("fghijklmnopqrstuvwxyzabcde")
        assert result == "abcdefghijklmnopqrstuvwxyz"

    def test_consistency_multiple_calls(self):
        """Calling encode_shift multiple times produces consistent results."""
        s = "python"
        assert encode_shift(s) == encode_shift(s)

    def test_consistency_decode_multiple_calls(self):
        """Calling decode_shift multiple times produces consistent results."""
        s = "fghijkl"
        assert decode_shift(s) == decode_shift(s)

    def test_special_characters_behavior(self):
        """Special characters are processed by the same formula."""
        result = encode_shift("!@#")
        assert result.isalpha()
        assert len(result) == 3

    def test_uppercase_not_handled_as_lowercase(self):
        """Uppercase letters follow the same formula (not treated specially)."""
        result = encode_shift("A")
        assert result == "z"

    def test_mixed_case(self):
        """Mixed-case strings are encoded character-by-character."""
        result = encode_shift("AbC")
        assert len(result) == 3
        assert result.isalpha()

    def test_whitespace_handling(self):
        """Whitespace characters are shifted according to the formula."""
        result = encode_shift("a b c")
        assert len(result) == 5
        assert result.isalpha()

    def test_newline_and_tab(self):
        """Newline and tab characters are also shifted."""
        result = encode_shift("a\tb\nc")
        assert len(result) == 5
        assert result.isalpha()

    def test_long_string(self):
        """Encoding a long string works correctly."""
        long_str = "a" * 1000
        encoded = encode_shift(long_str)
        assert len(encoded) == 1000
        assert all(ch == "f" for ch in encoded)

    def test_decode_long_string(self):
        """Decoding a long string works correctly."""
        long_encoded = "f" * 1000
        decoded = decode_shift(long_encoded)
        assert len(decoded) == 1000
        assert all(ch == "a" for ch in decoded)

    def test_encode_then_decode_returns_original_lowercase(self):
        """Comprehensive round-trip test with lowercase-only inputs."""
        test_cases = [
            "",
            "a",
            "z",
            "hello",
            "world",
            "python",
            "programming",
            "abcdefghijklmnopqrstuvwxyz",
        ]
        for original in test_cases:
            assert decode_shift(encode_shift(original)) == original

    def test_decode_then_encode_returns_original_lowercase(self):
        """Encoding a decoded string returns the original encoded form (lowercase only)."""
        test_cases = [
            "",
            "f",
            "e",
            "mjrqx",
            "btwqi",
            "utymtn",
        ]
        for encoded in test_cases:
            assert encode_shift(decode_shift(encoded)) == encoded

    def test_output_is_always_lowercase(self):
        """encode_shift always outputs lowercase letters regardless of input."""
        for inp in ["ABC", "123", "!@#", " \t\n", "Hello World"]:
            result = encode_shift(inp)
            assert result.islower(), f"Expected lowercase for input {inp!r}, got {result!r}"

    def test_decode_output_is_always_lowercase(self):
        """decode_shift always outputs lowercase letters regardless of input."""
        for inp in ["ABC", "123", "!@#", " \t\n", "Hello World"]:
            result = decode_shift(inp)
            assert result.islower(), f"Expected lowercase for input {inp!r}, got {result!r}"

    def test_length_preserved(self):
        """Both functions preserve string length."""
        test_strings = ["", "a", "hello", "hello world", "abc123!@#"]
        for s in test_strings:
            assert len(encode_shift(s)) == len(s)
            assert len(decode_shift(s)) == len(s)

    def test_specific_encoding_hello(self):
        """Verify encoding of 'hello' character by character."""
        # h(104)->m(109), e(101)->j(106), l(108)->q(113), l(108)->q(113), o(111)->t(116)
        assert encode_shift("hello") == "mjqq" + "t"

    def test_specific_decoding_mjqq(self):
        """Verify decoding of 'mjqq'."""
        assert decode_shift("mjqq") == "hell"

    def test_encode_decode_symmetry(self):
        """If A = encode(B), then B = decode(A)."""
        test_inputs = ["a", "z", "abc", "xyz", "python", "test"]
        for original in test_inputs:
            encoded = encode_shift(original)
            assert decode_shift(encoded) == original

    def test_decode_encode_symmetry(self):
        """If B = decode(A), then A = encode(B)."""
        test_inputs = ["f", "e", "fgh", "cde", "utymtn", "yjxy"]
        for encoded in test_inputs:
            decoded = decode_shift(encoded)
            assert encode_shift(decoded) == encoded
