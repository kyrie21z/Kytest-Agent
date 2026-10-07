import pytest
from solution import magic_square_test


class TestMagicSquareTest:
    """Tests for the magic_square_test function."""

    # --- Valid magic squares (3x3) ---

    def test_lo_shu_magic_square(self):
        """Standard 3x3 Lo Shu magic square."""
        my_matrix = [
            [8, 1, 6],
            [3, 5, 7],
            [4, 9, 2],
        ]
        assert magic_square_test(my_matrix) is True

    def test_another_3x3_magic_square(self):
        """Another valid 3x3 magic square (rows permuted)."""
        my_matrix = [
            [2, 7, 6],
            [9, 5, 1],
            [4, 3, 8],
        ]
        assert magic_square_test(my_matrix) is True

    # --- Valid magic squares (4x4) ---

    def test_4x4_magic_square(self):
        """A valid 4x4 magic square (all rows/cols/diags sum to 34)."""
        my_matrix = [
            [1, 15, 14, 4],
            [12, 6, 7, 9],
            [8, 10, 11, 5],
            [13, 3, 2, 16],
        ]
        assert magic_square_test(my_matrix) is True

    # --- Invalid cases ---

    def test_non_square_matrix_rows_different_lengths(self):
        """Matrix where rows have different lengths should fail or raise."""
        my_matrix = [
            [1, 2, 3],
            [4, 5],
            [7, 8, 9],
        ]
        try:
            result = magic_square_test(my_matrix)
            assert result is False
        except (IndexError, TypeError):
            pass  # Acceptable behavior for malformed input

    def test_all_zeros(self):
        """A matrix of all zeros — technically all sums are 0, so it's 'magic'."""
        my_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        assert magic_square_test(my_matrix) is True

    def test_row_sum_differs(self):
        """Rows do not sum to the same value."""
        my_matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        assert magic_square_test(my_matrix) is False

    def test_column_sum_differs(self):
        """Columns do not sum to the same value as rows."""
        my_matrix = [
            [1, 2, 3],
            [6, 5, 4],
            [7, 8, 9],
        ]
        assert magic_square_test(my_matrix) is False

    def test_main_diagonal_differs(self):
        """Main diagonal sum differs from row/column sums."""
        my_matrix = [
            [2, 2, 2],
            [2, 3, 2],
            [2, 2, 2],
        ]
        assert magic_square_test(my_matrix) is False

    def test_anti_diagonal_differs(self):
        """Anti-diagonal sum differs from row/column sums."""
        my_matrix = [
            [1, 5, 3],
            [3, 5, 7],
            [5, 5, 5],
        ]
        assert magic_square_test(my_matrix) is False

    def test_negative_numbers_valid(self):
        """A magic square with negative numbers (all sums = 0).
        
        Derived from Lo Shu by subtracting 5 from each element.
        """
        my_matrix = [
            [3, -4, 1],
            [-2, 0, 2],
            [-1, 4, -3],
        ]
        assert magic_square_test(my_matrix) is True

    def test_single_element_matrix(self):
        """A 1x1 matrix is trivially a magic square."""
        my_matrix = [[42]]
        assert magic_square_test(my_matrix) is True

    def test_two_by_two_cannot_be_magic(self):
        """A 2x2 matrix with all equal elements is technically magic."""
        my_matrix = [
            [1, 1],
            [1, 1],
        ]
        assert magic_square_test(my_matrix) is True

    def test_two_by_two_not_magic(self):
        """A 2x2 matrix that is not magic."""
        my_matrix = [
            [1, 2],
            [3, 4],
        ]
        assert magic_square_test(my_matrix) is False

    def test_larger_even_order_magic_square(self):
        """A valid 6x6 magic square (all rows, cols, diags sum to 111)."""
        my_matrix = [
            [35, 1, 6, 26, 19, 24],
            [3, 32, 7, 21, 23, 25],
            [31, 9, 2, 22, 27, 20],
            [8, 28, 33, 17, 10, 15],
            [30, 5, 34, 12, 14, 16],
            [4, 36, 29, 13, 18, 11],
        ]
        assert magic_square_test(my_matrix) is True

    def test_partial_match_rows_and_cols_but_diagonals_fail(self):
        """Rows and columns match but diagonals don't."""
        my_matrix = [
            [1, 5, 3],
            [5, 5, 5],
            [3, 5, 7],
        ]
        assert magic_square_test(my_matrix) is False

    def test_float_values(self):
        """Magic square with float values (all sums = 3.0)."""
        my_matrix = [
            [1.5, 0.5, 1.0],
            [0.5, 1.0, 1.5],
            [1.0, 1.5, 0.5],
        ]
        assert magic_square_test(my_matrix) is True

    def test_empty_matrix_raises(self):
        """An empty matrix should raise an error."""
        with pytest.raises(IndexError):
            magic_square_test([])

    def test_matrix_with_empty_rows(self):
        """A matrix with empty inner lists returns True (trivially, since no cols/diags)."""
        my_matrix = [[]]
        assert magic_square_test(my_matrix) is True
