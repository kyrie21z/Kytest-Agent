# Accepted by submit_tests; explanations in testgen_report.json.

from solution import next_power_of_2 as _case0_next_power_of_2

def test_power_of_two_identity():
    '''Docstring quote: "Write a python function to find the smallest power of 2 greater than or equal to n."'''
    assert _case0_next_power_of_2(1) == 1
    assert _case0_next_power_of_2(2) == 2
    assert _case0_next_power_of_2(4) == 4
    assert _case0_next_power_of_2(8) == 8
    assert _case0_next_power_of_2(16) == 16
    assert _case0_next_power_of_2(1024) == 1024

from solution import next_power_of_2 as _case1_next_power_of_2

def test_non_power_boundary():
    '''Docstring quote: "Write a python function to find the smallest power of 2 greater than or equal to n."'''
    assert _case1_next_power_of_2(3) == 4
    assert _case1_next_power_of_2(5) == 8
    assert _case1_next_power_of_2(6) == 8
    assert _case1_next_power_of_2(7) == 8
    assert _case1_next_power_of_2(9) == 16
    assert _case1_next_power_of_2(15) == 16
    assert _case1_next_power_of_2(17) == 32

from solution import next_power_of_2 as _case2_next_power_of_2

def test_zero_input():
    '''Docstring quote: "Write a python function to find the smallest power of 2 greater than or equal to n."'''
    assert _case2_next_power_of_2(0) == 1

from solution import next_power_of_2 as _case3_next_power_of_2

def test_return_type():
    '''Docstring quote: "Write a python function to find the smallest power of 2 greater than or equal to n."'''
    result = _case3_next_power_of_2(7)
    assert isinstance(result, int)
    assert result > 0
    assert result & result - 1 == 0
    result2 = _case3_next_power_of_2(100)
    assert isinstance(result2, int)
    assert result2 > 0
    assert result2 & result2 - 1 == 0

from solution import next_power_of_2 as _case4_next_power_of_2

def test_larger_values():
    '''Docstring quote: "Write a python function to find the smallest power of 2 greater than or equal to n."'''
    assert _case4_next_power_of_2(100) == 128
    assert _case4_next_power_of_2(128) == 128
    assert _case4_next_power_of_2(129) == 256
    assert _case4_next_power_of_2(255) == 256
    assert _case4_next_power_of_2(256) == 256
    assert _case4_next_power_of_2(257) == 512
    assert _case4_next_power_of_2(511) == 512
    assert _case4_next_power_of_2(512) == 512
    assert _case4_next_power_of_2(1000) == 1024
    assert _case4_next_power_of_2(1024) == 1024
    assert _case4_next_power_of_2(2047) == 2048
    assert _case4_next_power_of_2(2048) == 2048
