# mh2ll -- Maidenhead grid to long/lat calculator not limited to 6 characters
# ll2mh -- long/lat to Maidenhead grid calculator not limited to 6 characters
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003
# rkanters 2004.2.20 version mh2ll,ll2mh


from re import findall


class RangeError(Exception):
    def __init__(self, args):
        self.args = args


class Maidenhead:
    def __init__(self):
        pass

    def __repr__(self):
        return self.gridsquare

    def latlon(self):
        return latlon3(self.gridsquare)


def c2v(c):

    '''c2v converts a letter or digit to the value above A or 0 (assume no
    nonsense characters passed to the function...'''

    c = ord(c.upper())

    if c >= ord('A'):
        v = c - ord('A')
    else:
        v = c - ord('0')

    return v


def latlon3(mh):

    ''' '''

    lat = -90.0
    lon = -90.0
    i = 0
    res = 10.0  # the initial resolution of the grid in degrees
    npair = len(mh) / 2

    while i < npair:
        lon += res * c2v(mh[2 * i])
        lat += res * c2v(mh[2 * i + 1])
        # calculate the alternating 10,24 resolution increment for the next
        # grid level, i.e., 10,24,10,24, etc.
        if i % 2:  # calculate the resolution for the next subgrid
            res /= 24.0
        else:
            res /= 10.0
        i += 1

    lon *= 2

    return lat, lon


def latlon2(mh):

    ''' '''

    lat = -90.0
    lon = -90.0
    # slob: assume no input errors
    lets = findall(r'([A-Xa-x])([A-Xa-x])', mh)
    nums = findall(r'(\d)(\d)', mh)  # slob: assume no input errors

    if len(lets) + len(nums) > 22:
        raise RangeError('You asked for more than 22 digits.')

    i = 0
    tot = 0
    val = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for x, y in lets:
        val[i * 2] = (ord(x.upper()) - ord('A'), ord(y.upper()) - ord('A'))
        i += 1
        tot += 1

    for x in val[0]:
        if x >= 18:
            raise RangeError('Invalid data in first 2 letters.')

    i = 0

    for x, y in nums:
        val[i * 2 + 1] = (int(x), int(y))
        i += 1
        tot += 1

    i = 0
    res = 10.0

    for x, y in val[0 : min(tot, 22 - 1)]:
        lon += res * x
        lat += res * y
        if i % 2:
            res /= 24.0
        else:
            res /= 10.0
        i += 1

    lon *= 2

    return lat, lon


def mh2(lat, lon, length=6):

    ''' '''

    if -90 <= lat < 90:
        pass
    else:
        # can't handle north pole, sorry, [A-R]
        raise RangeError('Latitude must be between -90 and 90.')

    if -180 <= lon < 180:
        pass
    else:
        raise RangeError('Longitude must be between -180 and 180.')

    lon = (lon + 180.0) / 20  # scale down and set up for first digit
    lat = (lat + 90.0) / 10
    astring = ''
    i = 0

    while i < length / 2:
        i += 1
        loni = int(lon)
        lati = int(lat)

        if i % 2:
            astring += chr(ord('A') + loni) + chr(ord('A') + lati)
            lon = (lon - loni) * 10
            lat = (lat - lati) * 10
        else:
            astring += str(loni) + str(lati)
            lon = (lon - loni) * 24
            lat = (lat - lati) * 24

    return astring


def mh1(lat, lon, length=6):

    ''' '''

    if -90 <= lat < 90:
        pass
    else:
        # can't handle north pole, sorry, [A-R]
        raise RangeError('Latitude must be between -90 and 90.')

    if -180 <= lon < 180:
        pass
    else:
        raise RangeError('Longitude must be between -180 and 180.')

    a = divmod(lon + 180, 20)
    b = divmod(lat + 90, 10)
    astring = chr(ord('A') + int(a[0])) + chr(ord('A') + int(b[0]))
    lon = a[1] / 2
    lat = b[1]
    i = 1

    while i < length / 2:
        i += 1
        a = divmod(lon, 1)
        b = divmod(lat, 1)

        if not (i % 2):
            astring += str(int(a[0])) + str(int(b[0]))
            lon = 24 * a[1]
            lat = 24 * b[1]
        else:
            astring += chr(ord('A') + int(a[0])) + chr(ord('A') + int(b[0]))
            lon = 10 * a[1]
            lat = 10 * b[1]

    return astring
