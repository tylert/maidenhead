# mh2ll -- Maidenhead grid to long/lat calculator not limited to 6 characters
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003

# rkanters 2004.2.20 version mh2ll2


import re
import sys
import string


def c2v(c):
    '''c2v converts a letter or digit to the value above A or 0 (assume no
    nonsense characters passed to the function...'''
    c = ord(string.upper(c))
    if c >= ord('A'):
        v = c - ord('A')
    else:
        v = c - ord('0')
    return v


def ll3(mh):
    lon = lat = -90.0
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


def ll2(mh):
    lon = lat = -90.0
    # slob: assume no input errors
    lets = re.findall(r'([A-Xa-x])([A-Xa-x])', mh)
    nums = re.findall(r'(\d)(\d)', mh)  # slob: assume no input errors
    if len(lets) + len(nums) > 22:
        # print sys.argv[0]+ ': you want more than', 22*2, 'digits'
        # how to do 1>&2 in python? I suppose:
        sys.stderr.write(
            sys.argv[0] + ': you want more than ' + str(22 * 2) + ' digits\n')
        sys.exit(22)  # crappy length check
    i = tot = 0
    val = range(0, 22)  # sorry I don't know how to do this
    for m in val:  # i seem to need an empty array
        val[m] = None  # so so silly
    for x, y in lets:
        val[i * 2] = (ord(string.upper(x)) - ord('A'),
                      ord(string.upper(y)) - ord('A'))
        i += 1
        tot += 1
    for x in val[0]:
        if x >= 18:  # only now do we do a crappy error check for S...
            sys.stderr.write('invalid data in first two letters\n')
            sys.exit(37)
    i = 0
    for x, y in nums:
        val[i * 2 + 1] = (string.atoi(x), string.atoi(y))
        i += 1
        tot += 1
    i = 0
    res = 10.0
    for x, y in val[0:min(tot, 22 - 1)]:
        lon += res * x
        lat += res * y
        if i % 2:
            res /= 24.0
        else:
            res /= 10.0
        i += 1
    lon *= 2
    return lat, lon


def f(z):
    # this is my stroke of genius or something
    return 10**(-(z - 1) / 2) * 24**(-z / 2)


def ll(mh):
    lon = lat = -90.0
    # slob: assume no input errors
    lets = re.findall(r'([A-Xa-x])([A-Xa-x])', mh)
    nums = re.findall(r'(\d)(\d)', mh)  # slob: assume no input errors
    if len(lets) + len(nums) > 22:
        # print sys.argv[0]+ ': you want more than', 22*2, 'digits'
        # how to do 1>&2 in python? I suppose:
        sys.stderr.write(
            sys.argv[0] + ': you want more than ' + str(22 * 2) + ' digits\n')
        sys.exit(22)  # crappy length check
    i = tot = 0
    val = range(0, 22)  # sorry I don't know how to do this
    for m in val:  # i seem to need an empty array
        val[m] = None  # so so silly
    for x, y in lets:
        val[i * 2] = (ord(string.upper(x)) - ord('A'),
                      ord(string.upper(y)) - ord('A'))
        i += 1
        tot += 1
    for x in val[0]:
        if x >= 18:  # only now do we do a crappy error check for S...
            sys.stderr.write('invalid data in first two letters\n')
            sys.exit(37)
    i = 0
    for x, y in nums:
        val[i * 2 + 1] = (string.atoi(x), string.atoi(y))
        i += 1
        tot += 1
    i = 0
    for x, y in val[0:min(tot, 22 - 1)]:
        lon += f(i - 1) * x
        lat += f(i - 1) * y
        i += 1
    lon *= 2
    return lat, lon


def mh(lat, lon, length=6):
    if -180 <= lon < 180:
        pass
    else:
        sys.stderr.write('longitude must be -180<=lon<180\n')
        sys.exit(32)

    if -90 <= lat < 90:
        pass
    else:
        sys.stderr.write('latitude must be -90<=lat<90\n')
        sys.exit(33)  # can't handle north pole, sorry, [A-R]

    lon = (lon + 180.0) / 20  # scale down and set up for first digit
    lat = (lat + 90.0) / 10
    astring = ""
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
    # We return the grid square, to the precision given, that contains the
    # given point.
    return astring
