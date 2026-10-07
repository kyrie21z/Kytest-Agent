# Accepted by submit_tests; explanations in testgen_report.json.

def test_sum_div_prime():
    """Test that sum_div correctly computes the sum of proper divisors for a prime number.

    Contract quote: 'Write a function to return the sum of all divisors of a number.'
    Input domain: number = 7 (a prime number)
    Oracle: The only proper divisor of any prime p is 1. Therefore sum_div(7) must equal 1.
    Fault hypothesis: If the function incorrectly includes the number itself as a divisor,
        it would return 8 instead of 1. Or if it fails to include 1, it would return 0.
    """
    from solution import sum_div
    result = sum_div(7)
    assert result == 1
    assert isinstance(result, int)

def test_sum_div_perfect_number():
    """Test sum_div for a perfect number whose proper divisors sum to the number itself.

    Contract quote: 'Write a function to return the sum of all divisors of a number.'
    Input domain: number = 6 (perfect number)
    Oracle: Proper divisors of 6 are {1, 2, 3}. Their sum is 1 + 2 + 3 = 6.
    Fault hypothesis: A bug that skips divisor 2 would give 1+3=4; one that misses 3 gives 1+2=3.
    """
    from solution import sum_div
    result = sum_div(6)
    assert result == 6
    assert isinstance(result, int)

def test_sum_div_composite():
    """Test sum_div for a highly composite number with many divisors.

    Contract quote: 'Write a function to return the sum of all divisors of a number.'
    Input domain: number = 12
    Oracle: Proper divisors of 12 are {1, 2, 3, 4, 6}. Sum = 1+2+3+4+6 = 16.
    Fault hypothesis: Off-by-one in the loop range could miss divisor 6 (if range used <=) or
        incorrectly include 12 (if range went to number inclusive).
    """
    from solution import sum_div
    result = sum_div(12)
    assert result == 16
    assert isinstance(result, int)

def test_sum_div_square_number():
    """Test sum_div for a perfect square to verify the square root divisor is included.

    Contract quote: 'Write a function to return the sum of all divisors of a number.'
    Input domain: number = 9 (perfect square)
    Oracle: Proper divisors of 9 are {1, 3}. Sum = 1 + 3 = 4.
    Fault hypothesis: A common bug when finding divisors is to skip the square root or
        count it twice. Here sqrt(9)=3 is a proper divisor and must appear exactly once.
    """
    from solution import sum_div
    result = sum_div(9)
    assert result == 4
    assert isinstance(result, int)

def test_sum_div_small_numbers():
    """Test sum_div for small inputs at the lower boundary.

    Contract quote: 'Write a function to return the sum of all divisors of a number.'
    Input domain: number = 2 (smallest input where loop range is non-trivial)
    Oracle: Proper divisors of 2 are {1}. Sum = 1.
    Also test number = 4: proper divisors {1, 2}, sum = 3.
    Fault hypothesis: If range(2, number) were range(2, number+1), 4 would get 4 added,
        yielding 7 instead of 3.
    """
    from solution import sum_div
    assert sum_div(2) == 1
    assert sum_div(4) == 3
    assert isinstance(sum_div(2), int)
    assert isinstance(sum_div(4), int)

def test_sum_div_return_type():
    """Verify that sum_div always returns an integer for valid integer inputs.

    Contract quote: 'Write a function to return the sum of all divisors of a number.'
    Input domain: number = 10, 28, 100 (various positive integers)
    Oracle: The sum of integer divisors is always an integer. All results must be int type.
    Fault hypothesis: A bug using float division (/) instead of modulo (%) could produce floats.
    """
    from solution import sum_div
    for n in [10, 28, 100]:
        result = sum_div(n)
        assert isinstance(result, int), f'Expected int for sum_div({n}), got {type(result)}'
    assert sum_div(10) == 8
    assert sum_div(28) == 28
    assert sum_div(100) == 117
