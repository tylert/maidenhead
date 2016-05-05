#!/usr/bin/env python


# mh2ll -- Maidenhead grid to long/lat calculator not limited to 6 characters
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003

# rkanters 2004.2.20 version mh2ll2


import re
import sys
import string


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
        val[i * 2] = (ord(string.upper(x)) - ord('A'), ord(string.upper(y)) - ord('A'))
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


while 1:
    mh = sys.stdin.readline()
    if not mh:
        break
    lat, lon = ll2(mh)
    print('{0} {1}'.format(lon, lat))
