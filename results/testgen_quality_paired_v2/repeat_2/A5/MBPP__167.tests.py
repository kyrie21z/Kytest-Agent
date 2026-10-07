# Accepted by submit_tests; explanations in testgen_report.json.

from solution import next_power_of_2 as _case0_next_power_of_2

def test_next_power_of_2_powers_of_two():
    '''Docstring quote: "Write a python function to find the smallest power of 2 greater than or equal to n."'''
    input_domain = 'n is a positive integer that is already a power of 2'
    oracle_reason = 'If n is already a power of 2, the smallest power of 2 >= n is n itself.'
    fault_hypothesis = 'Detects if the function fails to recognize existing powers of 2 and returns a larger value instead.'
    assert _case0_next_power_of_2(1) == 1
    assert _case0_next_power_of_2(2) == 2
    assert _case0_next_power_of_2(4) == 4
    assert _case0_next_power_of_2(8) == 8
    assert _case0_next_power_of_2(16) == 16
    assert _case0_next_power_of_2(256) == 256

from solution import next_power_of_2 as _case1_next_power_of_2

def test_next_power_of_2_non_powers():
    '''Docstring quote: "Write a python function to find the smallest power of 2 greater than or equal to n."'''
    input_domain = 'n is a positive integer that is not a power of 2'
    oracle_reason = 'For non-power-of-2 n, the result is the next power of 2 strictly greater than n. E.g., 3->4, 5->8, 7->8, 9->16.'
    fault_hypothesis = 'Detects if the function returns the wrong power of 2 (too small or too large) for non-power inputs.'
    assert _case1_next_power_of_2(3) == 4
    assert _case1_next_power_of_2(5) == 8
    assert _case1_next_power_of_2(6) == 8
    assert _case1_next_power_of_2(7) == 8
    assert _case1_next_power_of_2(9) == 16
    assert _case1_next_power_of_2(15) == 16
    assert _case1_next_power_of_2(17) == 32

from solution import next_power_of_2 as _case2_next_power_of_2

def test_next_power_of_2_zero():
    '''Docstring quote: "Write a python function to find the smallest power of 2 greater than or equal to n."'''
    input_domain = 'n == 0'
    oracle_reason = 'The smallest power of 2 >= 0 is 1 (2^0 = 1). Since 0 is not a power of 2, the function should compute ceil-log2 and return 1.'
    fault_hypothesis = 'Detects if the function returns 0 or raises an error for n=0, which would violate the contract.'
    result = _case2_next_power_of_2(0)
    assert isinstance(result, int)
    assert result == 1

from solution import next_power_of_2 as _case3_next_power_of_2

def test_next_power_of_2_boundary_values():
    '''Docstring quote: "Write a python function to find the smallest power of 2 greater than or equal to n."'''
    input_domain = 'n is near boundaries between powers of 2'
    oracle_reason = 'Values just below a power of 2 should round up to that power. Values just above should round up to the next power. E.g., 2^k-1 -> 2^k, 2^k+1 -> 2^(k+1).'
    fault_hypothesis = 'Detects off-by-one errors where the function rounds down instead of up, or skips a power level.'
    assert _case3_next_power_of_2(3) == 4
    assert _case3_next_power_of_2(7) == 8
    assert _case3_next_power_of_2(15) == 16
    assert _case3_next_power_of_2(63) == 64
    assert _case3_next_power_of_2(5) == 8
    assert _case3_next_power_of_2(9) == 16
    assert _case3_next_power_of_2(17) == 32

from solution import next_power_of_2 as _case4_next_power_of_2

def test_next_power_of_2_return_type():
    '''Docstring quote: "Write a python function to find the smallest power of 2 greater than or equal to n."'''
    input_domain = 'n is any non-negative integer'
    oracle_reason = 'The function always returns an integer (a power of 2), which is a valid Python int type.'
    fault_hypothesis = 'Detects if the function returns a non-integer type (e.g., float, None) due to implementation bugs.'
    for n in [0, 1, 2, 3, 4, 7, 8, 15, 16, 100, 1023, 1024]:
        result = _case4_next_power_of_2(n)
        assert isinstance(result, int), f'Expected int for n={n}, got {type(result)}'
        assert result > 0, f'Result must be positive for n={n}'
        assert result & result - 1 == 0, f'Result {result} for n={n} is not a power of 2'
