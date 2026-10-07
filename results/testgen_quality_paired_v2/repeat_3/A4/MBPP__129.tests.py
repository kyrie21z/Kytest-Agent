# Accepted by submit_tests; explanations in testgen_report.json.

def test_valid_3x3_magic_square():
    """Test that a well-known 3x3 magic square returns True.

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
    Oracle reasoning: This is the classic Lo Shu magic square. Row sums are all 15,
      column sums are all 15, main diagonal (2+5+8=15), anti-diagonal (6+5+4=15).
      Since all eight sums equal 15, the function must return True.
    Fault hypothesis: A buggy implementation might miss one of the diagonal sums
      or miscalculate a row/column sum, causing a valid magic square to be rejected.
    """
    from solution import magic_square_test
    result = magic_square_test([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
    assert result is True

def test_non_magic_square_row_sum_mismatch():
    """Test that a matrix with unequal row sums returns False.

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Oracle reasoning: Row sums are 6, 15, 24 — clearly not equal. Therefore this
      cannot be a magic square and the function must return False.
    Fault hypothesis: If the function only checked columns but not rows, it might
      incorrectly return True for matrices where columns happen to balance.
    """
    from solution import magic_square_test
    result = magic_square_test([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert result is False

def test_single_element_matrix():
    """Test that a 1x1 matrix returns True.

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[42]]
    Oracle reasoning: A single element has one row sum (42), one column sum (42),
      one main diagonal sum (42), and one anti-diagonal sum (42). All are equal,
      so it is trivially a magic square and must return True.
    Fault hypothesis: An implementation that requires n >= 2 or miscomputes indices
      for n=1 could return False or crash.
    """
    from solution import magic_square_test
    result = magic_square_test([[42]])
    assert result is True

def test_2x2_not_magic():
    """Test that a 2x2 matrix that is not a magic square returns False.

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[1, 2], [3, 4]]
    Oracle reasoning: Row sums are 3 and 7 — already unequal, so not a magic square.
      Even ignoring rows: col sums are 4 and 6, main diag = 5, anti-diag = 5.
      Multiple sums differ, so must return False.
    Fault hypothesis: A bug in column summation (e.g., wrong indexing) could mask
      the inequality and return True incorrectly.
    """
    from solution import magic_square_test
    result = magic_square_test([[1, 2], [3, 4]])
    assert result is False

def test_all_zeros_magic_square():
    """Test that a matrix of all zeros returns True.

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    Oracle reasoning: Every row sum = 0, every column sum = 0, both diagonals = 0.
      All eight sums are 0, so they are all equal. Must return True.
    Fault hypothesis: An implementation using set() on sum_list could work correctly
      here, but a bug involving division by zero or special-casing zero would fail.
    """
    from solution import magic_square_test
    result = magic_square_test([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert result is True

def test_semi_magic_fails_diagonal():
    """Test a semi-magic square (rows/cols equal but diagonals differ).

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
    Oracle reasoning: This is the classic Lo Shu magic square — rows, cols, and
      both diagonals all equal 15. Must return True.
    Fault hypothesis: A bug in diagonal indexing could cause a valid magic square
      to be rejected.
    """
    from solution import magic_square_test
    result = magic_square_test([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
    assert result is True

def test_4x4_magic_square():
    """Test a known 4x4 magic square returns True.

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[1, 15, 14, 4], [12, 6, 7, 9], [8, 10, 11, 5], [13, 3, 2, 16]]
    Oracle reasoning: This is Durer's magic square. Each row sums to 34, each column
      sums to 34, main diagonal (1+6+11+16=34), anti-diagonal (4+7+10+13=34). All
      eight sums equal 34, so must return True.
    Fault hypothesis: Off-by-one errors in loop bounds for n=4 could miss elements.
    """
    from solution import magic_square_test
    result = magic_square_test([[1, 15, 14, 4], [12, 6, 7, 9], [8, 10, 11, 5], [13, 3, 2, 16]])
    assert result is True

def test_negative_values_magic_square():
    """Test a magic square with negative values returns True.

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[-1, 5, -3], [-4, 1, 6], [7, -3, 1]]
    Oracle reasoning: Row sums: -1+5-3=1, -4+1+6=3, 7-3+1=5. These are not equal,
      so this is NOT a magic square. Must return False.
    Fault hypothesis: Sign errors or incorrect summation could produce wrong results.
    """
    from solution import magic_square_test
    result = magic_square_test([[-1, 5, -3], [-4, 1, 6], [7, -3, 1]])
    assert result is False

def test_column_sum_mismatch():
    """Test a matrix where rows match but columns do not.

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[1, 4, 3], [2, 5, 4], [3, 6, 5]]
    Oracle reasoning: Row sums: 8, 11, 14 — already unequal. Also col sums:
      1+2+3=6, 4+5+6=15, 3+4+5=12. Multiple mismatches. Must return False.
    Fault hypothesis: If only rows were checked, this might pass incorrectly.
    """
    from solution import magic_square_test
    result = magic_square_test([[1, 4, 3], [2, 5, 4], [3, 6, 5]])
    assert result is False

def test_return_type_bool():
    """Test that the function always returns a Python bool.

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
    Oracle reasoning: The contract says "whether" implying a boolean answer.
      The implementation uses `return True` / `return False`, so the result
      must be exactly the bool type, not an int or other truthy value.
    Fault hypothesis: If someone changed the return to `return len(set(sum_list)) == 1`
      it would still work, but if they returned `not (len(set(sum_list)) > 1)`
      it would also work. However, asserting `isinstance(result, bool)` catches
      accidental returns like integers or strings.
    """
    from solution import magic_square_test
    result = magic_square_test([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
    assert isinstance(result, bool)
    assert result is True

def test_larger_non_magic():
    """Test a 5x5 matrix that is clearly not a magic square.

    Contract quote: "Write a function to calculate whether the matrix is a magic square."
    Input domain: my_matrix = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15],
                              [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
    Oracle reasoning: Row sums are 15, 40, 65, 90, 115 — wildly different.
      Must return False.
    Fault hypothesis: Large number overflow or incorrect loop bounds could
      produce wrong results.
    """
    from solution import magic_square_test
    result = magic_square_test([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]])
    assert result is False
