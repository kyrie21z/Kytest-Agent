import pytest
from solution import is_happy


class TestIsHappy:
    """Tests for the is_happy function."""

    # --- Strings too short (length < 3) should return False ---
    def test_empty_string(self):
        assert is_happy("") is False

    def test_single_char(self):
        assert is_happy("a") is False

    def test_two_chars(self):
        assert is_happy("aa") is False
        assert is_happy("ab") is False

    # --- Strings of length >= 3 with all consecutive triples distinct ---
    def test_length_3_all_distinct(self):
        assert is_happy("abc") is True
        assert is_happy("xyz") is True
        assert is_happy("adb") is True

    def test_length_4_all_distinct(self):
        assert is_happy("abcd") is True
        assert is_happy("abce") is True

    def test_length_5_all_distinct(self):
        assert is_happy("abcde") is True
        assert is_happy("abcdef") is True

    def test_longer_string_all_distinct(self):
        assert is_happy("abcdefgh") is True
        assert is_happy("zyxwvutsr") is True

    # --- Strings where some triple has duplicate characters ---
    def test_adjacent_duplicates_in_triple(self):
        # "aabb" -> triple "aab" has 'a' == 'a'
        assert is_happy("aabb") is False
        assert is_happy("baab") is False
        assert is_happy("abbc") is False

    def test_second_and_third_same(self):
        # "xyy" -> triple "xyy" has 'y' == 'y'
        assert is_happy("xyy") is False
        # "aay" -> triple "aay" has 'a' == 'a'
        assert is_happy("aay") is False
        # "axy" where x != y is happy since all three chars are distinct
        assert is_happy("axy") is True

    def test_first_and_third_same(self):
        # "aba" -> triple "aba" has 'a' == 'a'
        assert is_happy("aba") is False
        # "abac" -> triple "aba" fails
        assert is_happy("abac") is False
        # "abcda" -> triples: abc(ok), bcd(ok), cda(ok) => True
        assert is_happy("abcda") is True

    def test_middle_duplicate(self):
        assert is_happy("abca") is True  # triples: abc(ok), bca(ok)
        assert is_happy("abac") is False  # triples: aba(fail)

    # --- Edge cases with repeated patterns ---
    def test_alternating_pattern(self):
        assert is_happy("abab") is False  # triple "aba" fails
        assert is_happy("abac") is False  # triple "aba" fails

    def test_all_same_characters(self):
        assert is_happy("aaa") is False
        assert is_happy("aaaa") is False
        assert is_happy("aaaaa") is False

    def test_mixed_with_later_failure(self):
        # First few triples ok, but one later fails
        assert is_happy("abcdde") is False  # triple "dde" fails
        assert is_happy("abcdd") is False   # triple "bdd" fails

    # --- Mixed valid/invalid scenarios ---
    def test_valid_then_invalid(self):
        assert is_happy("abcdde") is False

    def test_invalid_then_valid(self):
        assert is_happy("aabcde") is False  # triple "aab" fails

    # --- Numeric and special character strings ---
    def test_numeric_string(self):
        assert is_happy("123") is True
        assert is_happy("112") is False
        assert is_happy("121") is False

    def test_special_characters(self):
        assert is_happy("!@#") is True
        assert is_happy("!!@") is False
        assert is_happy("!@!") is False

    def test_mixed_alphanumeric(self):
        assert is_happy("a1b") is True
        assert is_happy("a1a") is False
        assert is_happy("a11") is False

    # --- Boundary: exactly length 3 ---
    def test_boundary_length_3_true(self):
        assert is_happy("abc") is True

    def test_boundary_length_3_false(self):
        assert is_happy("aab") is False
        assert is_happy("aba") is False
        assert is_happy("abb") is False

    # --- Long strings with no issues ---
    def test_long_happy_string(self):
        assert is_happy("abcdefghijklmnopqrstuvwxyz") is True

    # --- Long strings with issues ---
    def test_long_unhappy_string(self):
        assert is_happy("abcdefghijklmnopqrsstuvwxyz") is False  # "sst" fails

    # --- Verify docstring examples ---
    def test_docstring_examples(self):
        assert is_happy("a") is False
        assert is_happy("aa") is False
        assert is_happy("abcd") is True
        assert is_happy("aabb") is False
        assert is_happy("adb") is True
        assert is_happy("xyy") is False
