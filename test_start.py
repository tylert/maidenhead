import maidenhead


def test_one():
    assert maidenhead.ll1(mh='FN25AI') == (45.333333333333336, -76.0)

def test_two():
    assert maidenhead.ll2(mh='FN25AI') == (45.333333333333336, -76.0)

def test_three():
    assert maidenhead.ll3(mh='FN25AI') == (45.333333333333336, -76.0)

def test_four():
    assert maidenhead.mh1(lat=45.3333333333, lon=-76.0) == 'FN25AH'

def test_five():
    assert maidenhead.mh2(lat=45.3333333333, lon=-76.0) == 'FN25AH'
