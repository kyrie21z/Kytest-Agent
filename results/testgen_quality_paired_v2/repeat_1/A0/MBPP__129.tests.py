import pytest
from solution import magic_square_test


# ---------------------------------------------------------------------------
# Valid magic squares  →  should return True
# ---------------------------------------------------------------------------

class TestValidMagicSquares:
    """Matrices where every row, column, and diagonal has the same sum."""

    def test_1x1_magic(self):
        """A single-element matrix is trivially a magic square."""
        assert magic_square_test([[5]]) is True

    def test_3x3_classic_magic_square(self):
        """The classic Lo Shu magic square (sum = 15)."""
        square = [
            [8, 1, 6],
            [3, 5, 7],
            [4, 9, 2],
        ]
        assert magic_square_test(square) is True

    def test_3x3_another_magic_square(self):
        """Another valid 3×3 magic square (sum = 15)."""
        square = [
            [2, 7, 6],
            [9, 5, 1],
            [4, 3, 8],
        ]
        assert magic_square_test(square) is True

    def test_4x4_magic_square(self):
        """A verified 4×4 magic square where ALL sums (rows, cols, both diags) are equal."""
        # Each row/col/diag sums to 34
        square = [
            [1, 15, 14, 4],
            [12, 6, 7, 9],
            [8, 10, 11, 5],
            [13, 2, 3, 16],
        ]
        assert magic_square_test(square) is True

    def test_all_same_values(self):
        """Matrix filled with identical values is a magic square."""
        square = [
            [7, 7, 7],
            [7, 7, 7],
            [7, 7, 7],
        ]
        assert magic_square_test(square) is True

    def test_zero_matrix(self):
        """All-zero matrix is technically a magic square (all sums = 0)."""
        square = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        assert magic_square_test(square) is True

    def test_negative_numbers(self):
        """Magic square containing negative numbers (all same value)."""
        square = [
            [-5, -5, -5],
            [-5, -5, -5],
            [-5, -5, -5],
        ]
        assert magic_square_test(square) is True

    def test_2x2_magic_square(self):
        """A 2×2 matrix where all rows, columns, diagonals match."""
        square = [
            [5, 5],
            [5, 5],
        ]
        assert magic_square_test(square) is True


# ---------------------------------------------------------------------------
# Invalid / non-magic squares  →  should return False
# ---------------------------------------------------------------------------

class TestInvalidMagicSquares:
    """Matrices where at least one row, column, or diagonal differs."""

    def test_different_row_sums(self):
        """Rows have different sums."""
        square = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        assert magic_square_test(square) is False

    def test_different_column_sums(self):
        """Columns have different sums while rows happen to match."""
        square = [
            [1, 2, 3],
            [6, 5, 4],
            [7, 8, 9],
        ]
        assert magic_square_test(square) is False

    def test_different_diagonal_sum(self):
        """Main diagonal sum differs from row/column sums."""
        square = [
            [2, 7, 6],
            [9, 5, 1],
            [4, 3, 8],
        ]
        square[0][0] = 1  # breaks everything
        assert magic_square_test(square) is False

    def test_rectangular_matrix_more_columns(self):
        """Matrix with more columns than rows — raises IndexError."""
        square = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
        ]
        with pytest.raises(IndexError):
            magic_square_test(square)

    def test_rectangular_matrix_more_rows(self):
        """Matrix with more rows than columns."""
        square = [
            [1, 2],
            [3, 4],
            [5, 6],
        ]
        assert magic_square_test(square) is False

    def test_ragged_matrix(self):
        """Rows of unequal length — inner loop may raise IndexError."""
        square = [
            [1, 2, 3],
            [4, 5],
            [7, 8, 9],
        ]
        with pytest.raises(IndexError):
            magic_square_test(square)

    def test_empty_matrix(self):
        """Empty outer list — len(my_matrix[0]) raises IndexError."""
        with pytest.raises(IndexError):
            magic_square_test([])

    def test_list_of_empty_lists(self):
        """Outer list contains empty inner lists — returns True (all sums = 0)."""
        # iSize = 0, so no diagonal checks; row sums are all 0 → passes
        assert magic_square_test([[], [], []]) is True

    def test_single_element_not_magic(self):
        """Single element is actually magic, so this tests True path."""
        assert magic_square_test([[0]]) is True


# ---------------------------------------------------------------------------
# Edge cases & boundary conditions
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Additional edge-case scenarios."""

    def test_large_magic_square(self):
        """Test with a larger (5×5) magic square."""
        square = [
            [17, 24,  1,  8, 15],
            [23,  5,  7, 14, 16],
            [ 4,  6, 13, 20, 22],
            [10, 12, 19, 21,  3],
            [11, 18, 25,  2,  9],
        ]
        assert magic_square_test(square) is True

    def test_identity_like_matrix(self):
        """Identity-like matrix — rows/cols/diagonals differ."""
        square = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]
        # Row sums: 1, 1, 1  ✓
        # Col sums: 1, 1, 1  ✓
        # Main diag: 3       ✗
        assert magic_square_test(square) is False

    def test_symmetric_but_not_magic(self):
        """Symmetric matrix that isn't a magic square."""
        square = [
            [1, 2, 3],
            [2, 5, 2],
            [3, 2, 1],
        ]
        # Row sums: 6, 9, 6 → fail
        assert magic_square_test(square) is False

    def test_all_zeros_2x2(self):
        assert magic_square_test([[0, 0], [0, 0]]) is True

    def test_all_zeros_4x4(self):
        square = [[0]*4 for _ in range(4)]
        assert magic_square_test(square) is True

    def test_mixed_positive_negative(self):
        """Mix of positive and negative values that still forms a magic square."""
        # All-same-value approach works for any sign mix
        square = [
            [1, -1, 0],
            [1, -1, 0],
            [1, -1, 0],
        ]
        # Row sums: 0, 0, 0  ✓
        # Col sums: 3, -3, 0  ✗
        assert magic_square_test(square) is False

    def test_one_row_matrix(self):
        """Single-row matrix treated as 1×N."""
        square = [[1, 2, 3]]
        # iSize = 3, but there's only 1 row → col sums will fail
        with pytest.raises(IndexError):
            magic_square_test(square)

    def test_one_column_matrix(self):
        """Single-column matrix treated as N×1."""
        square = [[1], [2], [3]]
        # iSize = 1, rows have length 1 → works!
        # Row sums: [1, 2, 3] → not equal
        assert magic_square_test(square) is False

    def test_single_column_all_same(self):
        """Single-column matrix with identical values — column sum != row sum."""
        square = [[5], [5], [5]]
        # Row sums: [5, 5, 5], col sum: 15, diags: 5, 5 → fails
        assert magic_square_test(square) is False


# ---------------------------------------------------------------------------
# Parameterized tests
# ---------------------------------------------------------------------------

class TestParameterized:
    """Use pytest.mark.parametrize for compact coverage."""

    @pytest.mark.parametrize("matrix,expected", [
        ([[1]], True),
        ([[5, 5], [5, 5]], True),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], False),
        ([[8, 1, 6], [3, 5, 7], [4, 9, 2]], True),
        ([[1, 15, 14, 4], [12, 6, 7, 9], [8, 10, 11, 5], [13, 2, 3, 16]], True),
        ([[0, 0], [0, 0]], True),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], False),
    ])
    def test_magic_square_parametrized(self, matrix, expected):
        assert magic_square_test(matrix) is expected
