import pytest
from solution import file_name_check


class TestFileNameCheckValid:
    """Tests for valid file names that should return 'Yes'."""

    def test_txt_extension(self):
        assert file_name_check("example.txt") == "Yes"

    def test_exe_extension(self):
        assert file_name_check("program.exe") == "Yes"

    def test_dll_extension(self):
        assert file_name_check("library.dll") == "Yes"

    def test_uppercase_start(self):
        assert file_name_check("Example.txt") == "Yes"

    def test_single_char_name(self):
        assert file_name_check("a.txt") == "Yes"

    def test_digits_in_name_within_limit(self):
        assert file_name_check("file1.txt") == "Yes"

    def test_multiple_digits_within_limit(self):
        assert file_name_check("file12.txt") == "Yes"

    def test_three_digits_within_limit(self):
        assert file_name_check("file123.txt") == "Yes"

    def test_three_digits_all_in_name(self):
        # Name starts with letter, has exactly 3 digits
        assert file_name_check("abc123.txt") == "Yes"

    def test_underscore_in_name(self):
        assert file_name_check("my_file.txt") == "Yes"

    def test_hyphen_in_name(self):
        assert file_name_check("my-file.txt") == "Yes"

    def test_numbered_file(self):
        assert file_name_check("file1.exe") == "Yes"

    def test_complex_valid_name(self):
        # backup_2024_v1.dll has 5 digits -> No, use a name with <= 3 digits
        assert file_name_check("backup_v1.dll") == "Yes"

    def test_digits_at_end_within_limit(self):
        # report2023.txt has 4 digits -> No, use within limit
        assert file_name_check("report23.txt") == "Yes"

    def test_mixed_case_name_lowercase_ext(self):
        # Extension must be lowercase per spec
        assert file_name_check("MyFile.txt") == "Yes"

    def test_long_valid_name(self):
        assert file_name_check("very_long_filename_that_is_still_valid.txt") == "Yes"

    def test_name_with_numbers_and_letters(self):
        assert file_name_check("test123file.exe") == "Yes"

    def test_lowercase_extensions(self):
        assert file_name_check("file.txt") == "Yes"
        assert file_name_check("file.exe") == "Yes"
        assert file_name_check("file.dll") == "Yes"


class TestFileNameCheckInvalid:
    """Tests for invalid file names that should return 'No'."""

    # More than three digits
    def test_four_digits(self):
        assert file_name_check("file1234.txt") == "No"

    def test_many_digits(self):
        assert file_name_check("1234567890.txt") == "No"

    def test_four_digits_middle(self):
        assert file_name_check("fi1234le.txt") == "No"

    # No dot or multiple dots
    def test_no_dot(self):
        assert file_name_check("exampletxt") == "No"

    def test_two_dots(self):
        assert file_name_check("example.tar.gz") == "No"

    def test_three_dots(self):
        assert file_name_check("a.b.c.txt") == "No"

    def test_dot_only(self):
        assert file_name_check(".") == "No"

    # Empty substring before dot
    def test_empty_before_dot(self):
        assert file_name_check(".txt") == "No"

    def test_empty_before_dot_exe(self):
        assert file_name_check(".exe") == "No"

    # Name doesn't start with a letter
    def test_starts_with_digit(self):
        assert file_name_check("1example.txt") == "No"

    def test_starts_with_underscore(self):
        assert file_name_check("_example.txt") == "No"

    def test_starts_with_hyphen(self):
        assert file_name_check("-example.txt") == "No"

    def test_starts_with_special_char(self):
        assert file_name_check("@example.txt") == "No"

    # Invalid extension
    def test_invalid_extension_pdf(self):
        assert file_name_check("example.pdf") == "No"

    def test_invalid_extension_jpg(self):
        assert file_name_check("photo.jpg") == "No"

    def test_invalid_extension_py(self):
        assert file_name_check("script.py") == "No"

    def test_invalid_extension_csv(self):
        assert file_name_check("data.csv") == "No"

    def test_invalid_extension_uppercase(self):
        assert file_name_check("example.TXT") == "No"

    def test_invalid_extension_mixed_case(self):
        assert file_name_check("example.TxT") == "No"

    # Edge cases
    def test_empty_string(self):
        assert file_name_check("") == "No"

    def test_only_dot(self):
        assert file_name_check(".") == "No"

    def test_only_extension(self):
        assert file_name_check(".txt") == "No"

    def test_only_digits_and_dot(self):
        assert file_name_check("123.txt") == "No"

    def test_numeric_name(self):
        assert file_name_check("1234.txt") == "No"

    def test_single_digit_start(self):
        assert file_name_check("1.txt") == "No"

    def test_non_alpha_start_special(self):
        assert file_name_check("!file.txt") == "No"

    def test_report_with_four_digits(self):
        # report2023.txt has 4 digits -> No
        assert file_name_check("report2023.txt") == "No"

    def test_backup_with_five_digits(self):
        # backup_2024_v1.dll has 5 digits -> No
        assert file_name_check("backup_2024_v1.dll") == "No"

    def test_name_starting_with_three_digits(self):
        # 123abc.txt starts with digit -> No
        assert file_name_check("123abc.txt") == "No"


class TestFileNameCheckEdgeCases:
    """Additional edge case tests."""

    def test_exactly_three_digits(self):
        assert file_name_check("abc123.txt") == "Yes"

    def test_extension_not_in_list(self):
        assert file_name_check("file.doc") == "No"

    def test_uppercase_extension(self):
        assert file_name_check("file.TXT") == "No"

    def test_space_in_name_allowed_by_function(self):
        # The function splits on '.', so "my file.txt" -> ["my file", "txt"]
        # "my file" starts with 'm' (alpha), 0 digits -> Yes
        assert file_name_check("my file.txt") == "Yes"

    def test_spaces_around_dot_allowed(self):
        # "example .txt" -> ["example ", "txt"]
        # "example " starts with 'e' (alpha), 0 digits -> Yes
        assert file_name_check("example .txt") == "Yes"

    def test_three_digits_one_each_part(self):
        # "a1.b1t1.txt" -> split gives ["a1.b1t1", "txt"] -> wait, split on '.' gives ["a1", "b1t1", "txt"] -> len != 2 -> No
        assert file_name_check("a1.b1t1.txt") == "No"
