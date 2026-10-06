import pytest
from solution import encode_cyclic, decode_cyclic


# ---------------------------------------------------------------------------
# encode_cyclic tests
# ---------------------------------------------------------------------------

class TestEncodeCyclic:

    def test_empty_string(self):
        assert encode_cyclic("") == ""

    def test_single_character(self):
        # Length < 3 → no cycling
        assert encode_cyclic("a") == "a"

    def test_two_characters(self):
        # Length < 3 → no cycling
        assert encode_cyclic("ab") == "ab"

    def test_exactly_three_characters(self):
        # One full group: "abc" → "bca"
        assert encode_cyclic("abc") == "bca"

    def test_six_characters_two_groups(self):
        # "abcdef" → ["abc", "def"] → ["bca", "efd"] → "bcaefd"
        assert encode_cyclic("abcdef") == "bcaefd"

    def test_four_characters_one_full_plus_remainder(self):
        # "abcd" → ["abc", "d"] → ["bca", "d"] → "bcad"
        assert encode_cyclic("abcd") == "bcad"

    def test_five_characters(self):
        # "abcde" → ["abc", "de"] → ["bca", "de"] → "bcade"
        assert encode_cyclic("abcde") == "bcade"

    def test_nine_characters_three_groups(self):
        # "abcdefghi" → ["abc","def","ghi"] → ["bca","efd","hig"]
        assert encode_cyclic("abcdefghi") == "bcaefdhig"

    def test_mixed_case(self):
        # "Abc" → ["Abc"] → "bcA"
        assert encode_cyclic("Abc") == "bcA"

    def test_special_characters(self):
        assert encode_cyclic("!@#") == "@#!"

    def test_spaces_in_group_of_three(self):
        # "a b" has length 3 → one group "a b" → cycle → " ba"
        assert encode_cyclic("a b") == " ba"

    def test_spaces_not_a_full_group(self):
        # "a b " → groups=["a b", " "] → cycled=[" ba", " "] → " ba "
        assert encode_cyclic("a b ") == " ba "

    def test_longer_string(self):
        # "hello world" → groups=["hel","lo ","wor","ld"]
        # cycled=["elh","ol ","row","ld"] → "elhol rowld"
        assert encode_cyclic("hello world") == "elhol rowld"

    def test_numbers(self):
        # "123456" → ["123","456"] → ["231","564"] → "231564"
        assert encode_cyclic("123456") == "231564"

    def test_all_same_characters(self):
        assert encode_cyclic("aaa") == "aaa"

    def test_length_7(self):
        # "abcdefg" → ["abc","def","g"] → ["bca","efd","g"] → "bcaefdg"
        assert encode_cyclic("abcdefg") == "bcaefdg"

    def test_length_8(self):
        # "abcdefgh" → ["abc","def","gh"] → ["bca","efd","gh"] → "bcaefdgh"
        assert encode_cyclic("abcdefgh") == "bcaefdgh"

    def test_length_10(self):
        # "abcdefghij" → ["abc","def","ghi","j"] → ["bca","efd","hig","j"]
        assert encode_cyclic("abcdefghij") == "bcaefdhigj"


# ---------------------------------------------------------------------------
# decode_cyclic tests
# ---------------------------------------------------------------------------

class TestDecodeCyclic:

    def test_empty_string(self):
        assert decode_cyclic("") == ""

    def test_single_character(self):
        assert decode_cyclic("a") == "a"

    def test_two_characters(self):
        assert decode_cyclic("ab") == "ab"

    def test_exactly_three_characters(self):
        # "bca" → "abc"
        assert decode_cyclic("bca") == "abc"

    def test_six_characters_two_groups(self):
        # "bcaefd" → ["bca","efd"] → ["abc","def"] → "abcdef"
        assert decode_cyclic("bcaefd") == "abcdef"

    def test_four_characters(self):
        # "bcad" → ["bca","d"] → ["abc","d"] → "abcd"
        assert decode_cyclic("bcad") == "abcd"

    def test_five_characters(self):
        # "bcade" → ["bca","de"] → ["abc","de"] → "abcde"
        assert decode_cyclic("bcade") == "abcde"

    def test_nine_characters(self):
        assert decode_cyclic("bcaefdhig") == "abcdefghi"

    def test_mixed_case(self):
        # "bcA" → ["bcA"] → reverse cycle → "Abc"
        assert decode_cyclic("bcA") == "Abc"

    def test_special_characters(self):
        assert decode_cyclic("@#!") == "!@#"

    def test_spaces_in_group_of_three(self):
        # " ba" has length 3 → one group " ba" → reverse cycle → "a b"
        assert decode_cyclic(" ba") == "a b"

    def test_spaces_not_a_full_group(self):
        # " ba " → groups=[" ba", " "] → reverse=["a b", " "] → "a b "
        assert decode_cyclic(" ba ") == "a b "

    def test_longer_string(self):
        # "elhol rowld" → ["elh","ol ","row","ld"] → ["hel","lo ","wor","ld"] → "hello world"
        assert decode_cyclic("elhol rowld") == "hello world"

    def test_numbers(self):
        # "231564" → ["231","564"] → ["123","456"] → "123456"
        assert decode_cyclic("231564") == "123456"

    def test_all_same_characters(self):
        assert decode_cyclic("aaa") == "aaa"

    def test_length_7(self):
        assert decode_cyclic("bcaefdg") == "abcdefg"

    def test_length_8(self):
        # "bcaefdgh" → ["bca","efd","gh"] → ["abc","def","gh"] → "abcdefgh"
        assert decode_cyclic("bcaefdgh") == "abcdefgh"

    def test_length_10(self):
        assert decode_cyclic("bcaefdhigj") == "abcdefghij"


# ---------------------------------------------------------------------------
# Round-trip tests: encode then decode should return original
# ---------------------------------------------------------------------------

class TestRoundTrip:

    @pytest.mark.parametrize(
        "input_str",
        [
            "",
            "a",
            "ab",
            "abc",
            "abcd",
            "abcde",
            "abcdef",
            "abcdefgh",
            "abcdefghi",
            "abcdefghij",
            "hello world",
            "The quick brown fox jumps over the lazy dog.",
            "!!!",
            "123456789",
            "aA1bB2cC3",
            "   ",
            " a ",
            "a b",
            "a b ",
            " abc",
        ],
    )
    def test_encode_decode_roundtrip(self, input_str):
        encoded = encode_cyclic(input_str)
        decoded = decode_cyclic(encoded)
        assert decoded == input_str

    @pytest.mark.parametrize(
        "input_str",
        [
            "",
            "a",
            "ab",
            "abc",
            "abcd",
            "abcde",
            "abcdef",
            "abcdefgh",
            "abcdefghi",
            "abcdefghij",
            "hello world",
            "The quick brown fox jumps over the lazy dog.",
            "!!!",
            "123456789",
            "aA1bB2cC3",
            "   ",
            " a ",
            "a b",
            "a b ",
            " abc",
        ],
    )
    def test_decode_encode_roundtrip(self, input_str):
        decoded_back = encode_cyclic(decode_cyclic(input_str))
        assert decoded_back == input_str
