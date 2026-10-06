import pytest
from solution import decimal_to_binary


class TestDecimalToBinary:
    """Unit tests for the decimal_to_binary function."""

    # --- Basic / documented examples ---
    def test_example_15(self):
        assert decimal_to_binary(15) == "db1111db"

    def test_example_32(self):
        assert decimal_to_binary(32) == "db100000db"

    # --- Edge cases ---
    def test_zero(self):
        """0 in binary is '0', so result should be 'db0db'."""
        assert decimal_to_binary(0) == "db0db"

    def test_one(self):
        """1 in binary is '1', so result should be 'db1db'."""
        assert decimal_to_binary(1) == "db1db"

    def test_two(self):
        """2 in binary is '10', so result should be 'db10db'."""
        assert decimal_to_binary(2) == "db10db"

    # --- Powers of two ---
    @pytest.mark.parametrize("value,expected_bin", [
        (4, "100"),
        (8, "1000"),
        (16, "10000"),
        (64, "1000000"),
        (128, "10000000"),
        (256, "100000000"),
    ])
    def test_powers_of_two(self, value, expected_bin):
        assert decimal_to_binary(value) == f"db{expected_bin}db"

    # --- Small positive integers ---
    @pytest.mark.parametrize("decimal,expected", [
        (3, "db11db"),
        (5, "db101db"),
        (7, "db111db"),
        (10, "db1010db"),
        (16, "db10000db"),
        (20, "db10100db"),
        (42, "db101010db"),
        (100, "db1100100db"),
        (255, "db11111111db"),
        (256, "db100000000db"),
    ])
    def test_various_decimals(self, decimal, expected):
        assert decimal_to_binary(decimal) == expected

    # --- Return type checks ---
    def test_returns_string(self):
        assert isinstance(decimal_to_binary(10), str)

    def test_starts_and_ends_with_db(self):
        """Every result must start and end with 'db'."""
        result = decimal_to_binary(42)
        assert result.startswith("db")
        assert result.endswith("db")

    def test_middle_part_is_valid_binary(self):
        """The inner part (excluding 'db' prefix/suffix) should contain only '0' or '1'."""
        result = decimal_to_binary(99)
        inner = result[2:-2]
        assert all(c in ("0", "1") for c in inner)

    # --- Round-trip consistency ---
    def test_round_trip_consistency(self):
        """Converting back from the binary portion should yield the original number."""
        for n in range(0, 200):
            result = decimal_to_binary(n)
            inner = result[2:-2]
            assert int(inner, 2) == n

    # --- Large numbers ---
    def test_large_number(self):
        assert decimal_to_binary(1024) == "db10000000000db"

    def test_larger_number(self):
        assert decimal_to_binary(12345) == "db11000000111001db"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
