# Accepted by submit_tests; explanations in testgen_report.json.

def test_magic_square_3x3_standard():
    """Verify a well-known 3x3 magic square returns True.
    
    Contract quote: 'Write a function to calculate whether the matrix is a magic square.'
    
    Input domain: my_matrix = [[8,1,6],[3,5,7],[4,9,2]] — a classic Lo Shu magic square.
    
    Oracle: Every row sums to 15, every column sums to 15, main diagonal (8+5+2) = 15,
    anti-diagonal (6+5+4) = 15. All eight sums are identical, so the function must return True.
    
    Fault hypothesis: Detects any regression that breaks correct detection of valid magic squares,
    e.g., off-by-one in diagonal traversal or incorrect column summation.
    """
    from solution import magic_square_test
    my_matrix = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
    assert magic_square_test(my_matrix) is True

def test_non_magic_square_rows_differ():
    """Verify a non-magic square returns False when row sums differ.
    
    Contract quote: 'Write a function to calculate whether the matrix is a magic square.'
    
    Input domain: my_matrix = [[1,2,3],[4,5,6],[7,8,9]].
    
    Oracle: Row sums are [6, 15, 24] which are not all equal. Therefore the function must
    return False regardless of other sums.
    
    Fault hypothesis: Detects bugs where the function incorrectly returns True despite
    clearly unequal row sums, e.g., if row summation were skipped or overwritten.
    """
    from solution import magic_square_test
    my_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert magic_square_test(my_matrix) is False

def test_single_element_matrix():
    """Verify a 1x1 matrix is treated as a magic square.
    
    Contract quote: 'Write a function to calculate whether the matrix is a magic square.'
    
    Input domain: my_matrix = [[5]].
    
    Oracle: There is one row (sum=5), one column (sum=5), one main diagonal (sum=5),
    and one anti-diagonal (sum=5). All sums equal, so return True.
    
    Fault hypothesis: Detects edge-case failures where iSize=1 causes incorrect loop bounds
    or indexing errors that produce wrong results instead of True.
    """
    from solution import magic_square_test
    my_matrix = [[5]]
    assert magic_square_test(my_matrix) is True

def test_uniform_matrix_all_equal():
    """Verify a uniform matrix (all same values) returns True.
    
    Contract quote: 'Write a function to calculate whether the matrix is a magic square.'
    
    Input domain: my_matrix = [[2, 2], [2, 2]].
    
    Oracle: Every row sums to 4, every column sums to 4, main diagonal = 2+2 = 4,
    anti-diagonal = 2+2 = 4. All sums equal → True.
    
    Fault hypothesis: Detects bugs in diagonal computation that might differentiate
    the two diagonals when they should be identical (e.g., reversed index error).
    """
    from solution import magic_square_test
    my_matrix = [[2, 2], [2, 2]]
    assert magic_square_test(my_matrix) is True

def test_column_sums_break_magic():
    """Verify False when row sums match but column sums differ.
    
    Contract quote: 'Write a function to calculate whether the matrix is a magic square.'
    
    Input domain: my_matrix = [[1, 3], [2, 2]].
    
    Oracle: Row sums = [4, 4] (equal). Column sums = [1+2, 3+2] = [3, 5] (not equal).
    Main diagonal = 1+2 = 3. Anti-diagonal = 3+2 = 5. Since column sums differ,
    the function must return False.
    
    Fault hypothesis: Detects bugs where column summation is skipped or computed incorrectly,
    causing a false positive when only row sums happen to match.
    """
    from solution import magic_square_test
    my_matrix = [[1, 3], [2, 2]]
    assert magic_square_test(my_matrix) is False

def test_diagonal_mismatch():
    """Verify False when all rows and columns match but diagonals differ.
    
    Contract quote: 'Write a function to calculate whether the matrix is a magic square.'
    
    Input domain: my_matrix = [[1, 2], [2, 1]].
    
    Oracle: Row sums = [3, 3], column sums = [3, 3], main diagonal = 1+1 = 2,
    anti-diagonal = 2+2 = 4. Not all equal → False.
    
    Fault hypothesis: Detects bugs where diagonal sums are computed incorrectly,
    such as using the wrong indices or iterating in the wrong direction.
    """
    from solution import magic_square_test
    my_matrix = [[1, 2], [2, 1]]
    assert magic_square_test(my_matrix) is False
