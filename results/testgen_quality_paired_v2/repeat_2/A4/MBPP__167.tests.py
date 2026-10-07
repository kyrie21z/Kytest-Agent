# Accepted by submit_tests; explanations in testgen_report.json.

def test_already_power_of_two():
    from solution import next_power_of_2
    assert next_power_of_2(4) == 4
    assert next_power_of_2(8) == 8
    assert next_power_of_2(16) == 16
    assert next_power_of_2(1) == 1
    assert next_power_of_2(2) == 2

def test_not_power_of_two_rounds_up():
    from solution import next_power_of_2
    assert next_power_of_2(3) == 4
    assert next_power_of_2(5) == 8
    assert next_power_of_2(6) == 8
    assert next_power_of_2(7) == 8
    assert next_power_of_2(9) == 16
    assert next_power_of_2(10) == 16

def test_zero_input():
    from solution import next_power_of_2
    assert next_power_of_2(0) == 1

def test_return_type_is_int():
    from solution import next_power_of_2
    result = next_power_of_2(7)
    assert isinstance(result, int)
    result = next_power_of_2(0)
    assert isinstance(result, int)
    result = next_power_of_2(1024)
    assert isinstance(result, int)

def test_boundary_between_powers():
    from solution import next_power_of_2
    assert next_power_of_2(15) == 16
    assert next_power_of_2(16) == 16
    assert next_power_of_2(17) == 32
    assert next_power_of_2(255) == 256
    assert next_power_of_2(256) == 256
    assert next_power_of_2(257) == 512
