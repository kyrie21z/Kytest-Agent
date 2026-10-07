# Accepted by submit_tests; explanations in testgen_report.json.

def test_basic_order():
    """Test that bf returns planets between Jupiter and Neptune in correct order."""
    from solution import bf
    result = bf('Jupiter', 'Neptune')
    assert result == ('Saturn', 'Uranus')
    assert isinstance(result, tuple)

def test_reversed_order():
    """Test that bf handles reversed planet order correctly."""
    from solution import bf
    result = bf('Earth', 'Mercury')
    assert result == ('Venus',)
    assert isinstance(result, tuple)

def test_adjacent_planets():
    """Test that bf returns empty tuple when planets are adjacent in orbit."""
    from solution import bf
    result = bf('Earth', 'Mars')
    assert result == ()
    assert isinstance(result, tuple)
    result2 = bf('Mars', 'Earth')
    assert result2 == ()
    assert isinstance(result2, tuple)

def test_invalid_planet_name():
    """Test that bf returns empty tuple for invalid planet names."""
    from solution import bf
    result = bf('Pluto', 'Earth')
    assert result == ()
    assert isinstance(result, tuple)
    result2 = bf('Mars', 'Krypton')
    assert result2 == ()
    assert isinstance(result2, tuple)
    result3 = bf('Pluto', 'Krypton')
    assert result3 == ()
    assert isinstance(result3, tuple)

def test_same_planet():
    """Test that bf returns empty tuple when both arguments are the same planet."""
    from solution import bf
    result = bf('Earth', 'Earth')
    assert result == ()
    assert isinstance(result, tuple)
    result2 = bf('Mercury', 'Mercury')
    assert result2 == ()
    result3 = bf('Neptune', 'Neptune')
    assert result3 == ()

def test_full_range_reverse():
    """Test that bf returns all intermediate planets regardless of argument order."""
    from solution import bf
    result_forward = bf('Mercury', 'Neptune')
    result_reverse = bf('Neptune', 'Mercury')
    expected = ('Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus')
    assert result_forward == expected
    assert result_reverse == expected
    assert isinstance(result_forward, tuple)
    assert isinstance(result_reverse, tuple)
