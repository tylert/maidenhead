#!/usr/bin/env python


# mh2ll -- Maidenhead grid to long/lat calculator not limited to 6 characters
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003

# rkanters 2004.2.20 version mh2ll3


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


while 1:
    mh = sys.stdin.readline()
    if not mh:
        break
    lat, lon = ll3(mh)
    print('{0} {1}'.format(lon, lat))
