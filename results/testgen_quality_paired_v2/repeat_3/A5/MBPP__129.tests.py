# Accepted by submit_tests; explanations in testgen_report.json.

from solution import magic_square_test as _case0_magic_square_test

def test_valid_3x3_magic_square():
    """Test a standard Lo Shu 3x3 magic square where every row, column,
    and both diagonals sum to 15."""
    matrix = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
    assert _case0_magic_square_test(matrix) is True

from solution import magic_square_test as _case1_magic_square_test

def test_valid_1x1_matrix():
    """A 1x1 matrix is trivially a magic square — single element equals itself.
    Tests the smallest valid input boundary."""
    assert _case1_magic_square_test([[5]]) is True

from solution import magic_square_test as _case2_magic_square_test

def test_non_magic_square_rows():
    """A 3x3 matrix where rows do not all sum equally — clearly not a magic square."""
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert _case2_magic_square_test(matrix) is False

from solution import magic_square_test as _case3_magic_square_test

def test_2x2_all_equal_elements():
    """A 2x2 matrix with all identical elements has equal sums everywhere.
    Tests the 2x2 boundary case."""
    matrix = [[3, 3], [3, 3]]
    assert _case3_magic_square_test(matrix) is True

from solution import magic_square_test as _case4_magic_square_test

def test_2x2_not_magic():
    """A 2x2 matrix that is not a magic square — row sums differ."""
    matrix = [[1, 2], [3, 4]]
    assert _case4_magic_square_test(matrix) is False

from solution import magic_square_test as _case5_magic_square_test

def test_magic_square_negative_values():
    """A 3x3 matrix with negative numbers where all sums are equal.
    Tests that the function handles negative values correctly."""
    matrix = [[-1, -6, 5], [4, -2, -3], [3, 0, -4]]
    matrix2 = [[1, -1, 0], [0, 0, 0], [-1, 1, 0]]
    matrix3 = [[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]
    matrix4 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert _case5_magic_square_test(matrix4) is True
