import pytest
from solution import check_dict_case


class TestCheckDictCase:
    """Tests for the check_dict_case function."""

    # --- All lowercase keys (should return True) ---

    def test_all_lowercase_single_key(self):
        assert check_dict_case({"a": "apple"}) is True

    def test_all_lowercase_multiple_keys(self):
        assert check_dict_case({"a": "apple", "b": "banana"}) is True

    def test_all_lowercase_with_numbers_in_values(self):
        assert check_dict_case({"name": "John", "age": "36"}) is True

    def test_all_lowercase_underscored_keys(self):
        assert check_dict_case({"first_name": "John", "last_name": "Doe"}) is True

    # --- All uppercase keys (should return True) ---

    def test_all_uppercase_single_key(self):
        assert check_dict_case({"A": "apple"}) is True

    def test_all_uppercase_multiple_keys(self):
        assert check_dict_case({"STATE": "NC", "ZIP": "12345"}) is True

    def test_all_uppercase_with_numbers_in_values(self):
        assert check_dict_case({"NAME": "John", "AGE": "36"}) is True

    def test_all_uppercase_underscored_keys(self):
        assert check_dict_case({"FIRST_NAME": "John", "LAST_NAME": "Doe"}) is True

    # --- Mixed case keys (should return False) ---

    def test_mixed_case_same_key(self):
        assert check_dict_case({"a": "apple", "A": "banana", "B": "banana"}) is False

    def test_mixed_case_different_keys(self):
        assert check_dict_case({"Name": "John", "Age": "36", "City": "Houston"}) is False

    def test_mixed_case_one_lower_one_upper(self):
        assert check_dict_case({"key": "value", "KEY2": "value2"}) is False

    def test_mixed_case_title_case(self):
        assert check_dict_case({"Key": "value"}) is False

    # --- Empty dictionary (should return False) ---

    def test_empty_dict(self):
        assert check_dict_case({}) is False

    # --- Non-string keys (should return False) ---

    def test_integer_key(self):
        assert check_dict_case({8: "banana"}) is False

    def test_mixed_string_and_integer_keys(self):
        assert check_dict_case({"a": "apple", 8: "banana"}) is False

    def test_float_key(self):
        assert check_dict_case({3.14: "pi"}) is False

    def test_tuple_key(self):
        assert check_dict_case({(1, 2): "value"}) is False

    def test_none_key(self):
        assert check_dict_case({None: "value"}) is False

    # --- Boolean keys (should return False since bool is not str) ---

    def test_boolean_key(self):
        assert check_dict_case({True: "value"}) is False

    # --- Single key edge cases ---

    def test_single_uppercase_key(self):
        assert check_dict_case({"STATE": "NC"}) is True

    def test_single_lowercase_key(self):
        assert check_dict_case({"state": "NC"}) is True

    # --- Keys with special characters ---

    def test_lowercase_with_hyphen(self):
        assert check_dict_case({"my-key": "value"}) is True

    def test_uppercase_with_hyphen(self):
        assert check_dict_case({"MY-KEY": "value"}) is True

    def test_lowercase_with_dots(self):
        assert check_dict_case({"my.key": "value"}) is True

    def test_uppercase_with_dots(self):
        assert check_dict_case({"MY.KEY": "value"}) is True

    # --- Values should not affect the result ---

    def test_empty_values(self):
        assert check_dict_case({"a": "", "b": ""}) is True

    def test_none_values(self):
        assert check_dict_case({"a": None, "b": None}) is True

    def test_numeric_values(self):
        assert check_dict_case({"a": 1, "b": 2}) is True

    def test_list_values(self):
        assert check_dict_case({"a": [1, 2], "b": [3, 4]}) is True

    def test_nested_dict_values(self):
        assert check_dict_case({"a": {"nested": True}, "b": {"nested": False}}) is True
