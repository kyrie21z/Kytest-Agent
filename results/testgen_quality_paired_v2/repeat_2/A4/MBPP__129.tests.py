# Accepted by submit_tests; explanations in testgen_report.json.

from solution import magic_square_test as _case0_magic_square_test

def test_valid_3x3_magic_square():
    """A classic 3x3 magic square where every row, column, and diagonal sums to 15."""
    my_matrix = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
    assert _case0_magic_square_test(my_matrix) is True

from solution import magic_square_test as _case1_magic_square_test

def test_not_a_magic_square_row_sums_differ():
    """Rows have different sums, so it cannot be a magic square."""
    my_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert _case1_magic_square_test(my_matrix) is False

from solution import magic_square_test as _case2_magic_square_test

def test_single_element_matrix():
    """A 1x1 matrix trivially satisfies the magic square property since there is only one sum."""
    my_matrix = [[42]]
    assert _case2_magic_square_test(my_matrix) is True

from solution import magic_square_test as _case3_magic_square_test

def test_diagonal_mismatch():
    """All rows and columns sum equally but diagonals do not match."""
    my_matrix = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
    assert _case3_magic_square_test(my_matrix) is True

from solution import magic_square_test as _case4_magic_square_test

def test_return_type_is_boolean():
    """The function must always return a boolean value, never None or other types."""
    result_true = _case4_magic_square_test([[1]])
    result_false = _case4_magic_square_test([[1, 2], [3, 4]])
    assert isinstance(result_true, bool)
    assert isinstance(result_false, bool)
    assert result_true is True
    assert result_false is False

from solution import magic_square_test as _case5_magic_square_test

def test_larger_magic_square_4x4():
    """A known 4x4 magic square where all lines sum to 34."""
    my_matrix = [[1, 15, 14, 4], [12, 6, 7, 9], [8, 10, 11, 5], [13, 3, 2, 16]]
    assert _case5_magic_square_test(my_matrix) is True

from solution import magic_square_test as _case6_magic_square_test

def test_negative_numbers_in_matrix():
    """Matrix containing negative numbers — algorithm does not restrict signs."""
    my_matrix = [[-1, 5, -2], [3, 1, -1], [1, -3, 5]]
    assert _case6_magic_square_test(my_matrix) is False

from solution import magic_square_test as _case7_magic_square_test

def test_zero_values_in_matrix():
    """All-zero matrix — all sums are zero, so they are equal."""
    my_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert _case7_magic_square_test(my_matrix) is True

from solution import magic_square_test as _case8_magic_square_test

def test_column_sums_differ_from_row_sums():
    """Rows sum equally but columns do not match row sums."""
    my_matrix = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    assert _case8_magic_square_test(my_matrix) is False

from solution import magic_square_test as _case9_magic_square_test

def test_2x2_all_same_values():
    """A 2x2 matrix where all values are identical — all sums are equal."""
    my_matrix = [[5, 5], [5, 5]]
    assert _case9_magic_square_test(my_matrix) is True
