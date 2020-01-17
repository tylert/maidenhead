from maidenhead import (latlon2, latlon3, mh1, mh2)


class TestMaidenhead:
    def test_two(self):
        assert latlon2(mh='FN25AI') == (45.333333333333336, -76.0)

    def test_three(self):
        assert latlon3(mh='FN25AI') == (45.333333333333336, -76.0)

    def test_four(self):
        assert mh1(lat=45.3333333333, lon=-76.0) == 'FN25AH'

    def test_five(self):
        assert mh2(lat=45.3333333333, lon=-76.0) == 'FN25AH'
