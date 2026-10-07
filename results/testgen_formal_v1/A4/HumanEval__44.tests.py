# Accepted by submit_tests; explanations in testgen_report.json.

def test_change_base_docstring_example_8_to_base3():
    """Test: change_base(8, 3) -> '22'.

    Contract quote:
        Change numerical base of input number x to base.

    Input domain: x=8 (positive int), base=3 (valid base < 10).

    Oracle reasoning:
        8 / 3 = 2 remainder 2  -> least significant digit is '2'
        2 / 3 = 0 remainder 2  -> next digit is '2'
        Result: '22'

    Fault hypothesis:
        Detects incorrect digit ordering or wrong modular arithmetic.
    """
    from solution import change_base
    result = change_base(8, 3)
    assert result == '22'
    assert isinstance(result, str)

def test_change_base_binary_8():
    """Test: change_base(8, 2) -> '1000'.

    Contract quote:
        Change numerical base of input number x to base.

    Input domain: x=8 (positive int), base=2 (smallest valid base).

    Oracle reasoning:
        8 in binary is 1000 (2^3 = 8).

    Fault hypothesis:
        Detects failure in the core conversion loop.
    """
    from solution import change_base
    result = change_base(8, 2)
    assert result == '1000'
    assert isinstance(result, str)

def test_change_base_binary_7():
    """Test: change_base(7, 2) -> '111'.

    Contract quote:
        Change numerical base of input number x to base.

    Input domain: x=7 (positive int), base=2.

    Oracle reasoning:
        7 = 4 + 2 + 1 = 1*2^2 + 1*2^1 + 1*2^0, so binary is '111'.

    Fault hypothesis:
        Detects incorrect handling when all bits are 1.
    """
    from solution import change_base
    result = change_base(7, 2)
    assert result == '111'
    assert isinstance(result, str)

def test_change_base_zero():
    """Test: change_base(0, any_base) -> '0'.

    Contract quote:
        Change numerical base of input number x to base.

    Input domain: x=0 (boundary value), base=5.

    Oracle reasoning:
        Zero represented in any base is "0".

    Fault hypothesis:
        Detects if zero guard is broken, causing empty string from while loop.
    """
    from solution import change_base
    result = change_base(0, 5)
    assert result == '0'
    assert isinstance(result, str)

def test_change_base_single_digit():
    """Test: change_base(1, 2) -> '1'.

    Contract quote:
        Change numerical base of input number x to base.

    Input domain: x=1 (smallest positive int), base=2.

    Oracle reasoning:
        1 < 2, so single-digit representation is '1'.

    Fault hypothesis:
        Detects edge-case failure for one-digit results.
    """
    from solution import change_base
    result = change_base(1, 2)
    assert result == '1'
    assert isinstance(result, str)

def test_change_base_larger_number_base10():
    """Test: change_base(100, 10) -> '100'.

    Contract quote:
        Change numerical base of input number x to base.

    Input domain: x=100, base=10 (largest valid base per docstring).

    Oracle reasoning:
        In base 10, 100 is simply "100". Identity property for base-10.

    Fault hypothesis:
        Detects subtle bugs in multi-digit conversions with repeated zeros.
    """
    from solution import change_base
    result = change_base(100, 10)
    assert result == '100'
    assert isinstance(result, str)
