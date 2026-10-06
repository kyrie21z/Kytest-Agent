import pytest
from solution import get_closest_vowel


class TestGetClosestVowelBasic:
    """Tests based on the examples provided in the docstring."""

    def test_yogurt(self):
        assert get_closest_vowel("yogurt") == "u"

    def test_full(self):
        assert get_closest_vowel("FULL") == "U"

    def test_quick(self):
        assert get_closest_vowel("quick") == ""

    def test_ab(self):
        assert get_closest_vowel("ab") == ""


class TestGetClosestVowelEdgeCases:
    """Tests for edge cases."""

    def test_empty_string(self):
        assert get_closest_vowel("") == ""

    def test_single_char_vowel(self):
        assert get_closest_vowel("a") == ""

    def test_single_char_consonant(self):
        assert get_closest_vowel("b") == ""

    def test_two_chars_vowel_consonant(self):
        assert get_closest_vowel("ae") == ""

    def test_two_chars_consonant_vowel(self):
        assert get_closest_vowel("ba") == ""

    def test_three_chars_cvc(self):
        # c = consonant, v = vowel => "cat" -> 'a' is between 'c' and 't'
        assert get_closest_vowel("cat") == "a"

    def test_three_chars_ccc(self):
        assert get_closest_vowel("bcd") == ""

    def test_three_chars_vcv(self):
        # vowel at start doesn't count as "between two consonants"
        assert get_closest_vowel("aba") == ""

    def test_four_chars_cvcc(self):
        # 'v' is between 'c' and 'c', but we search from right
        assert get_closest_vowel("acbd") == ""

    def test_four_chars_ccvc(self):
        # 'v' is between 'c' and 'c'
        assert get_closest_vowel("abcd") == ""


class TestGetClosestVowelRightToLeftSearch:
    """Tests verifying the right-to-left search behavior."""

    def test_multiple_candidates_returns_rightmost(self):
        # "bcdfegh": e is between f and g (consonants), search from right:
        #   i=6: h (not vowel)
        #   i=5: g (not vowel)
        #   i=4: f (not vowel)
        #   i=3: e (vowel), word[2]=d (not vowel), word[4]=f (not vowel) -> return 'e'
        assert get_closest_vowel("bcdfegh") == "e"

    def test_rightmost_valid_vowel_returned(self):
        # "xcade": 
        #   i=3: d (not vowel)
        #   i=2: a (vowel), word[1]=c (not vowel), word[3]=d (not vowel) -> return 'a'
        assert get_closest_vowel("xcade") == "a"

    def test_no_vowel_between_consonants(self):
        # All vowels adjacent or at edges
        assert get_closest_vowel("aeiou") == ""

    def test_vowel_at_start_not_counted(self):
        # 'a' is at index 0, so it can't be between two consonants
        assert get_closest_vowel("apple") == ""

    def test_vowel_in_middle_even_if_near_end(self):
        # "base": 'a' at index 1, word[0]='b'(consonant), word[2]='s'(consonant)
        # 'a' IS between two consonants, so it should be returned
        assert get_closest_vowel("base") == "a"


class TestGetClosestVowelCaseSensitivity:
    """Tests for case-sensitive behavior."""

    def test_uppercase_word(self):
        # "HELLO": 'E' at index 1, word[0]='H'(consonant), word[2]='L'(consonant)
        # 'E' IS between two consonants
        assert get_closest_vowel("HELLO") == "E"

    def test_mixed_case(self):
        # "bAcD": 'A' is between 'b' and 'C' (both consonants)
        assert get_closest_vowel("bAcD") == "A"

    def test_lowercase_result(self):
        assert get_closest_vowel("bAd") == "A"

    def test_preserves_original_case(self):
        # The returned vowel should match the case in the input
        assert get_closest_vowel("bAd") == "A"
        assert get_closest_vowel("bad") == "a"


class TestGetClosestVowelConsonantPatterns:
    """Tests with various consonant/vowel patterns."""

    def test_all_consonants(self):
        assert get_closest_vowel("bcdfghjkl") == ""

    def test_all_vowels(self):
        assert get_closest_vowel("aeiou") == ""

    def test_alternating_cvcvc(self):
        # "babab": from right, i=3: 'a'(vowel), word[2]='b'(not vowel), word[4]='b'(not vowel)
        # So 'a' IS between two consonants
        assert get_closest_vowel("babab") == "a"

    def test_consonant_vowel_consonant_in_middle(self):
        # "xyzaxz": 'a' at index 3, between 'x'(2) and 'x'(4)
        assert get_closest_vowel("xyzaxz") == "a"

    def test_double_consonants_with_vowel(self):
        # "bbcb": 'b','b','c','b' - 'c' is a consonant, not a vowel
        # There is no vowel between two consonants here
        assert get_closest_vowel("bbcb") == ""

    def test_long_word_with_vowel_between_consonants(self):
        # "strengths" - no vowel between two consonants from right
        # s-t-r-e-n-g-t-h-s
        # From right: s(8), h(7), t(6), g(5), n(4), e(3), r(2), t(1), s(0)
        # i=6: t(not vowel), i=5: g(not vowel), i=4: n(not vowel), i=3: e(vowel)
        #   word[2]=r(not vowel), word[4]=n(not vowel) -> return 'e'
        assert get_closest_vowel("strengths") == "e"


class TestGetClosestVowelYBehavior:
    """Tests for 'y' which is treated as a consonant."""

    def test_y_as_consonant(self):
        # 'y' is not a vowel in this implementation
        assert get_closest_vowel("byrd") == ""

    def test_y_in_pattern(self):
        # "xyaz": y(consonant), a(vowel), z(consonant) -> 'a' is between 'y' and 'z'
        assert get_closest_vowel("xyaz") == "a"


class TestGetClosestVowelSpecialCharacters:
    """Tests with special inputs."""

    def test_numbers_in_string(self):
        # The docstring says English letters only, but test robustness
        assert get_closest_vowel("a1b") == ""

    def test_repeated_letters(self):
        # "bookkeeper": o,o,k,e,e,p,k,e,r
        # From right: r(8), e(7), k(6), p(5), e(4), e(3), k(2), o(1), o(0)
        # i=7: e(vowel), word[6]=k(not vowel), word[8]=r(not vowel) -> return 'e'
        assert get_closest_vowel("bookkeeper") == "e"

    def test_vowel_sandwiched_by_same_consonant(self):
        # "bcb": 'c' is a consonant, not a vowel. No vowel between consonants.
        assert get_closest_vowel("bcb") == ""

    def test_vowel_between_identical_consonants(self):
        # "babb": 'a' at index 1, word[0]='b', word[2]='b' -> return 'a'
        assert get_closest_vowel("babb") == "a"

    def test_adjacent_vowels_not_matched(self):
        # "baad": 'a' at index 1, word[0]='b', word[2]='a'(vowel!) -> not matched
        # 'a' at index 2, word[1]='a'(vowel!) -> not matched
        assert get_closest_vowel("baad") == ""

    def test_vowel_before_adjacent_vowels(self):
        # "bacdd": 'a' at index 1, word[0]='b', word[2]='c' -> return 'a'
        assert get_closest_vowel("bacdd") == "a"
