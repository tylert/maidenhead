#!/usr/bin/env python


import sys
from re import findall

from maidenhead import mh2


def main():

    if len(sys.argv) == 2:  # slob city
        stringlength = int(sys.argv[1])
        if stringlength < 2 or stringlength % 2 != 0:
            raise RuntimeError('String length requested must be even ' 'integer > 0.')
    else:
        stringlength = 6

    while 1:
        line = sys.stdin.readline()
        if not line:
            break
        latlon = findall(r'([-0-9.]+)\s+([-0-9.]+)', line)

        if latlon:
            for leftval, rightval in latlon:
                lat = float(leftval)
                lon = float(rightval)
        else:
            raise RuntimeError('Cannot even get the basic items.')

        astring = mh2(lat, lon, stringlength)
        print('{0}'.format(astring))


if __name__ == '__main__':
    main()
