from maidenhead import (latlon2, latlon3, mh1, mh2)


class TestMaidenhead:
    def test_two(self):
        assert latlon2(mh='FN25AI') == (45.333333333333336, -76.0)
        assert latlon2(mh='FN25AI73CN') == (
            45.348090277777786, -75.94097222222221)
        assert latlon2(mh='FN25AI73DN') == (45.348090277777786, -75.940625)

    def test_three(self):
        assert latlon3(mh='FN25AI') == (45.333333333333336, -76.0)
        assert latlon3(mh='FN25AI73CN') == (
            45.348090277777786, -75.94097222222221)
        assert latlon3(mh='FN25AI73DN') == (45.348090277777786, -75.940625)

    def test_four(self):
        assert mh1(lat=45.3333333333, lon=-76.0) == 'FN25AH'
        assert mh1(lat=45.34815941779998, lon=-
                   75.94086880907598, length=10) == 'FN25AI73CN'
        assert mh1(lat=45.348090277777786, lon=-
                   75.940625, length=10) == 'FN25AI73DM'

    def test_five(self):
        assert mh2(lat=45.3333333333, lon=-76.0) == 'FN25AH'
        assert mh2(lat=45.34815941779998, lon=-
                   75.94086880907598, length=10) == 'FN25AI73CN'
        assert mh2(lat=45.348090277777786, lon=-
                   75.940625, length=10) == 'FN25AI73DM'
