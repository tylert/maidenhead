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


def ll1(mh):
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


def mh2(lat, lon, length=6):
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


def mh1(lat, lon, length=6):
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

        if not(i % 2):
            astring += str(int(a[0])) + str(int(b[0]))
            lon = 24 * a[1]
            lat = 24 * b[1]
        else:
            astring += chr(ord('A') + int(a[0])) + chr(ord('A') + int(b[0]))
            lon = 10 * a[1]
            lat = 10 * b[1]
    return astring


# From https://en.wikipedia.org/wiki/Maidenhead_Locator_System
'''

To simplify manual encoding, the base for the first pair of
letters—traditionally called a field—was chosen to be 18, thus dividing the
globe into 18 zones of longitude of 20° each, and 18 zones of latitude 10°
each. These zones are encoded with the letters "A" through "R".

The first pair of numbers, called a square and placed after the first pair of
letters, uses a base number of 10, and is encoded using the digits "0" to "9".
This is where the alternative name "grid squares" comes from. Each of these
squares represents 1° of latitude by 2° of longitude.

For additional precision, each square can optionally be sub-divided further,
into subsquares. These are encoded into a second pair of letters, often (but
not always) presented in lowercase, and again, to make manual calculations from
degrees and minutes easier, 24 was chosen as the base number, giving these
subsquares dimensions of 2.5' of latitude by 5' of longitude. The letters used
are "A" through "X".

The resulting Maidenhead subsquare locator string is hence composed of two
letters, two digits, and two more letters. To give an example, W1AW, the
American Radio Relay League's Hiram Percy Maxim Memorial Station in Newington,
Connecticut, is found in grid locator ​FN31pr. Two points within the same
Maidenhead subsquare are always less than 12 km apart, which means a Maidenhead
locator can give significant precision from just six easily transmissible
characters.

For even more precise location mapping, two additional digits were proposed and
ratified as an extended locator, making it altogether eight characters long,
and dividing subsquares into even smaller ones. Such precision has uses in very
short communication spans. Beyond this, no common definition exists to extend
the system further into even smaller squares. Most often the extending is done
by repeating alternating subsquare and square rules (base numbers 24 and 10
respectively). However, other bases for letter encodings have also been
observed, and therefore such extended extended locators might not be
compatible.

The Maidenhead locator system has been explicitly based on the WGS 84 geodetic
datum since 1999.[citation needed] Before that time, it was usually based on
each user's local national datum, which do differ slightly from one another and
WGS 84. As a result, stations very near the edges of squares at denoted
precision may have changed their locators when changing over to the use of WGS
84.

To summarise:

Character pairs encode longitude first, and then latitude.
The first pair (a field) encodes with base 18 and the letters "A" to "R".
The second pair (square) encodes with base 10 and the digits "0" to "9".
The third pair (subsquare) encodes with base 24 and the letters "A" to "X".
The fourth pair (extended square) encodes with base 10 and the digits "0" to
"9".

The fifth and subsequent pairs are not formally defined, but recycling the
third and fourth pair algorithms is one possible definition:

BL11BH16oo66

'''
