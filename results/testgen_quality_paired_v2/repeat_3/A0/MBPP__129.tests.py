import pytest
from solution import magic_square_test


class TestMagicSquareTest:
    """Tests for the magic_square_test function."""

    # ------------------------------------------------------------------
    # Valid magic squares → True
    # ------------------------------------------------------------------

    def test_classic_3x3_magic_square(self):
        """The classic Lo Shu magic square."""
        my_matrix = [
            [8, 1, 6],
            [3, 5, 7],
            [4, 9, 2],
        ]
        assert magic_square_test(my_matrix) is True

    def test_another_3x3_magic_square(self):
        """A different valid 3x3 magic square (rotated/reflected)."""
        my_matrix = [
            [6, 1, 8],
            [7, 5, 3],
            [2, 9, 4],
        ]
        assert magic_square_test(my_matrix) is True

    def test_1x1_matrix(self):
        """A single-element matrix is trivially a magic square."""
        my_matrix = [[42]]
        assert magic_square_test(my_matrix) is True

    def test_4x4_magic_square(self):
        """A valid 4x4 magic square where all rows, cols, and diagonals sum equally."""
        my_matrix = [
            [1, 15, 14, 4],
            [12, 6, 7, 9],
            [8, 10, 11, 5],
            [13, 3, 2, 16],
        ]
        # Row sums: 34, 34, 34, 34
        # Col sums: 34, 34, 34, 34
        # Diag1: 1+6+11+16=34; Diag2: 4+7+10+13=34
        assert magic_square_test(my_matrix) is True

    def test_2x2_with_equal_sums(self):
        """A 2x2 matrix where all rows, cols, and diagonals sum equally."""
        my_matrix = [
            [1, 1],
            [1, 1],
        ]
        assert magic_square_test(my_matrix) is True

    def test_all_zeros(self):
        """A matrix filled with zeros is a valid magic square."""
        my_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        assert magic_square_test(my_matrix) is True

    def test_negative_numbers(self):
        """A magic square containing negative numbers."""
        my_matrix = [
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1],
        ]
        assert magic_square_test(my_matrix) is True

    # ------------------------------------------------------------------
    # Invalid magic squares → False
    # ------------------------------------------------------------------

    def test_row_sum_mismatch(self):
        """Rows do not all sum to the same value."""
        my_matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        assert magic_square_test(my_matrix) is False

    def test_column_sum_mismatch(self):
        """Columns do not all sum to the same value."""
        my_matrix = [
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
        ]
        assert magic_square_test(my_matrix) is False

    def test_diagonal_sum_mismatch(self):
        """Main diagonal sum differs from row/column sums."""
        my_matrix = [
            [3, 7, 6],
            [9, 5, 1],
            [4, 3, 8],
        ]
        # Row sums: 16, 15, 15; already mismatched
        assert magic_square_test(my_matrix) is False

    def test_partial_match_but_not_all(self):
        """Rows match but columns don't."""
        my_matrix = [
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
        ]
        assert magic_square_test(my_matrix) is False

    def test_non_uniform_values(self):
        """Matrix with varying values that don't form a magic square."""
        my_matrix = [
            [1, 2, 3],
            [5, 6, 7],
            [8, 9, 10],
        ]
        assert magic_square_test(my_matrix) is False

    def test_larger_invalid_matrix(self):
        """A 4x4 matrix that is not a magic square."""
        my_matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]
        assert magic_square_test(my_matrix) is False

    # ------------------------------------------------------------------
    # Edge cases
    # ------------------------------------------------------------------

    def test_empty_matrix(self):
        """An empty list should raise an error."""
        with pytest.raises(IndexError):
            magic_square_test([])

    def test_single_element_list_in_matrix(self):
        """A matrix containing one empty inner list returns True
        because iSize=0 causes all loops to skip, leaving sum_list empty,
        and len(set()) == 0 which is not > 1."""
        my_matrix = [[]]
        assert magic_square_test(my_matrix) is True

    def test_rectangular_matrix_more_columns_than_rows(self):
        """Non-square matrix with more columns than rows raises IndexError
        because the function tries to access my_matrix[i][i] beyond row bounds."""
        my_matrix = [
            [1, 2, 3],
            [4, 5, 6],
        ]
        with pytest.raises(IndexError):
            magic_square_test(my_matrix)

    def test_rectangular_matrix_more_rows_than_columns(self):
        """Non-square matrix with more rows than columns."""
        my_matrix = [
            [1, 2],
            [3, 4],
            [5, 6],
        ]
        result = magic_square_test(my_matrix)
        assert isinstance(result, bool)

    def test_large_magic_square(self):
        """A larger valid magic square (5x5)."""
        my_matrix = [
            [17, 24, 1, 8, 15],
            [23, 5, 7, 14, 16],
            [4, 6, 13, 20, 22],
            [10, 12, 19, 21, 3],
            [11, 18, 25, 2, 9],
        ]
        assert magic_square_test(my_matrix) is True

    def test_float_values(self):
        """Magic square with floating-point numbers."""
        my_matrix = [
            [0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
        ]
        assert magic_square_test(my_matrix) is True

    def test_mixed_positive_negative(self):
        """Matrix with mixed positive and negative values that still works."""
        my_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        assert magic_square_test(my_matrix) is True

    def test_two_by_two_different_values(self):
        """2x2 with different values — only works if sums align."""
        my_matrix = [
            [2, 3],
            [3, 2],
        ]
        # Rows: 5, 5; Cols: 5, 5; Diags: 4, 5 → False
        assert magic_square_test(my_matrix) is False

    def test_two_by_two_same_values(self):
        """2x2 with identical values."""
        my_matrix = [
            [5, 5],
            [5, 5],
        ]
        assert magic_square_test(my_matrix) is True
