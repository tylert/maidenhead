import maidenhead


class TestMaidenhead:
    def test_one(self):
        assert maidenhead.latlon1(mh='FN25AI') == (45.333333333333336, -76.0)

    def test_two(self):
        assert maidenhead.latlon2(mh='FN25AI') == (45.333333333333336, -76.0)

    def test_three(self):
        assert maidenhead.latlon3(mh='FN25AI') == (45.333333333333336, -76.0)

    def test_four(self):
        assert maidenhead.mh1(lat=45.3333333333, lon=-76.0) == 'FN25AH'

    def test_five(self):
        assert maidenhead.mh2(lat=45.3333333333, lon=-76.0) == 'FN25AH'
