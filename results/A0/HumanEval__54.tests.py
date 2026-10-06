"""Unit tests for solution.py using pytest."""

from solution import same_chars


class TestSameChars:
    """Tests for the same_chars function."""

    # ---- Doctest examples from the docstring ----

    def test_same_chars_doctest_1(self):
        assert same_chars('eabcdzzzz', 'dddzzzzzzzddeddabc') is True

    def test_same_chars_doctest_2(self):
        assert same_chars('abcd', 'dddddddabc') is True

    def test_same_chars_doctest_3(self):
        assert same_chars('dddddddabc', 'abcd') is True

    def test_same_chars_doctest_4(self):
        assert same_chars('eabcd', 'dddddddabc') is False

    def test_same_chars_doctest_5(self):
        assert same_chars('abcd', 'dddddddabce') is False

    def test_same_chars_doctest_6(self):
        assert same_chars('eabcdzzzz', 'dddzzzzzzzddddabc') is False

    # ---- Basic / trivial cases ----

    def test_identical_strings(self):
        assert same_chars('hello', 'hello') is True

    def test_empty_strings(self):
        assert same_chars('', '') is True

    def test_one_empty_string(self):
        assert same_chars('', 'a') is False

    def test_single_char_same(self):
        assert same_chars('a', 'a') is True

    def test_single_char_different(self):
        assert same_chars('a', 'b') is False

    # ---- Character set equivalence ----

    def test_repeated_chars_same_set(self):
        assert same_chars('aaa', 'a') is True

    def test_all_unique_chars_same(self):
        assert same_chars('abc', 'cba') is True

    def test_overlapping_but_not_equal_sets(self):
        assert same_chars('abc', 'abd') is False

    def test_no_common_characters(self):
        assert same_chars('abc', 'def') is False

    def test_superset_of_chars(self):
        assert same_chars('ab', 'abc') is False

    def test_subset_of_chars(self):
        assert same_chars('abc', 'ab') is False

    # ---- Case sensitivity ----

    def test_case_sensitive_upper_lower(self):
        assert same_chars('A', 'a') is False

    def test_case_sensitive_mixed(self):
        assert same_chars('Abc', 'abc') is False

    def test_case_insensitive_same_if_only_upper(self):
        assert same_chars('ABC', 'CBA') is True

    # ---- Longer / more complex strings ----

    def test_longer_strings_same_set(self):
        assert same_chars(
            'abcdefghijklmnopqrstuvwxyz',
            'zyxwvutsrqponmlkjihgfedcba'
        ) is True

    def test_longer_strings_different_set(self):
        assert same_chars(
            'abcdefghijklmnopqrstuvwxyz',
            'abcdefghijklmnopqrstuvwxyZ'
        ) is False

    def test_spaces_in_strings(self):
        assert same_chars('a b', 'ba ') is True

    def test_spaces_differ(self):
        # 'a b' has chars {' ', 'a', 'b'}, 'ac ' has chars {' ', 'a', 'c'}
        assert same_chars('a b', 'ac ') is False

    def test_special_characters(self):
        assert same_chars('!@#', '#@!') is True

    def test_special_characters_differ(self):
        assert same_chars('!@#', '!$#') is False

    # ---- Numeric-like strings ----

    def test_numeric_strings_same(self):
        assert same_chars('123', '321') is True

    def test_numeric_strings_different(self):
        assert same_chars('123', '124') is False

    # ---- Unicode support ----

    def test_unicode_chars_same(self):
        assert same_chars('éàü', 'üéà') is True

    def test_unicode_chars_different(self):
        assert same_chars('éàü', 'éàö') is False

    # ---- Boolean return type ----

    def test_returns_boolean_true(self):
        result = same_chars('a', 'a')
        assert isinstance(result, bool)
        assert result is True

    def test_returns_boolean_false(self):
        result = same_chars('a', 'b')
        assert isinstance(result, bool)
        assert result is False
