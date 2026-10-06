import pytest
from solution import Strongest_Extension


class TestStrongestExtension:
    """Tests for the Strongest_Extension function."""

    def test_basic_example_from_docstring(self):
        """Test the example given in the docstring."""
        result = Strongest_Extension('my_class', ['AA', 'Be', 'CC'])
        assert result == 'my_class.AA'

    def test_slices_example_from_docstring(self):
        """Test the Slices example from the docstring."""
        result = Strongest_Extension('Slices', ['SErviNGSliCes', 'Cheese', 'StuFfed'])
        assert result == 'Slices.SErviNGSliCes'

    def test_single_extension(self):
        """When there is only one extension, it should be selected."""
        result = Strongest_Extension('MyClass', ['OnlyOne'])
        assert result == 'MyClass.OnlyOne'

    def test_all_uppercase_extension_wins(self):
        """An extension with all uppercase letters has positive strength."""
        # 'AAA' -> CAP=3, SM=0, strength=3
        # 'BBB' -> CAP=3, SM=0, strength=3
        # 'aBc' -> CAP=1, SM=2, strength=-1
        result = Strongest_Extension('Test', ['AAA', 'BBB', 'aBc'])
        assert result == 'Test.AAA'  # First among ties

    def test_all_lowercase_extension_has_negative_strength(self):
        """An extension with all lowercase letters has negative strength."""
        # 'abc' -> CAP=0, SM=3, strength=-3
        # 'ABC' -> CAP=3, SM=0, strength=3
        result = Strongest_Extension('Test', ['abc', 'ABC'])
        assert result == 'Test.ABC'

    def test_mixed_case_extension(self):
        """Test with mixed case extensions."""
        # 'MiXeD' -> CAP=2 (M, X), SM=3 (i, e, d), strength=-1
        # 'NoRmAl' -> CAP=1 (N), SM=5 (o, r, m, a, l), strength=-4
        result = Strongest_Extension('Test', ['MiXeD', 'NoRmAl'])
        assert result == 'Test.MiXeD'

    def test_tie_breaking_first_in_list(self):
        """When two extensions have equal strength, pick the first one."""
        # 'Ab' -> CAP=1, SM=1, strength=0
        # 'Ba' -> CAP=1, SM=1, strength=0
        result = Strongest_Extension('Test', ['Ab', 'Ba'])
        assert result == 'Test.Ab'

    def test_empty_extensions_list_raises_error(self):
        """Passing an empty list should raise an error (max of empty sequence)."""
        with pytest.raises(ValueError):
            Strongest_Extension('Test', [])

    def test_extension_with_numbers_and_special_chars(self):
        """Extensions may contain numbers and special characters which don't count."""
        # 'A1!' -> CAP=1, SM=0, strength=1
        # 'b2@' -> CAP=0, SM=1, strength=-1
        result = Strongest_Extension('Test', ['A1!', 'b2@'])
        assert result == 'Test.A1!'

    def test_extension_with_no_letters(self):
        """An extension with no letters has strength 0."""
        # '123' -> CAP=0, SM=0, strength=0
        # 'A' -> CAP=1, SM=0, strength=1
        result = Strongest_Extension('Test', ['123', 'A'])
        assert result == 'Test.A'

    def test_zero_strength_tie(self):
        """Multiple extensions with zero strength should pick the first."""
        # 'Ab' -> strength 0
        # 'Cd' -> strength 0
        # 'Ef' -> strength 0
        result = Strongest_Extension('Test', ['Ab', 'Cd', 'Ef'])
        assert result == 'Test.Ab'

    def test_class_name_preserved(self):
        """The class name should be preserved exactly as provided."""
        result = Strongest_Extension('MyCamelCaseClass', ['Ext'])
        assert result == 'MyCamelCaseClass.Ext'

    def test_extension_with_spaces(self):
        """Extensions with spaces - spaces are neither upper nor lower."""
        # 'A B' -> CAP=1, SM=1, strength=0
        # 'C D' -> CAP=1, SM=1, strength=0
        result = Strongest_Extension('Test', ['A B', 'C D'])
        assert result == 'Test.A B'

    def test_large_number_of_extensions(self):
        """Test with many extensions to ensure correctness at scale."""
        extensions = [f'E{i}' for i in range(100)]
        # All have strength 0 (one uppercase, one digit)
        result = Strongest_Extension('BigClass', extensions)
        assert result == 'BigClass.E0'

    def test_extension_with_only_digits(self):
        """Extension consisting only of digits has strength 0."""
        result = Strongest_Extension('Test', ['12345'])
        assert result == 'Test.12345'

    def test_extension_with_only_special_characters(self):
        """Extension with only special characters has strength 0."""
        result = Strongest_Extension('Test', ['!@#$%'])
        assert result == 'Test.!@#$%'

    def test_negative_strength_wins_over_more_negative(self):
        """Higher (less negative) strength should win."""
        # 'a' -> strength -1
        # 'ab' -> strength -2
        # 'abc' -> strength -3
        result = Strongest_Extension('Test', ['a', 'ab', 'abc'])
        assert result == 'Test.a'

    def test_positive_strength_wins_over_zero(self):
        """Positive strength should win over zero or negative."""
        # 'A' -> strength 1
        # '' -> strength 0 (empty string)
        # 'a' -> strength -1
        result = Strongest_Extension('Test', ['', 'A', 'a'])
        assert result == 'Test.A'
