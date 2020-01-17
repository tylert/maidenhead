#!/usr/bin/env python

# ll2mh -- long/lat to Maidenhead grid calculator not limited to 6 characters
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003
# rkanters 2004.2.20 version ll2mh


import re
import sys
import string

import maidenhead


def main():

    if len(sys.argv) == 2:  # slob city
        stringlength = string.atoi(sys.argv[1])
        if stringlength < 2 or stringlength % 2 != 0:
            raise RuntimeError('String length requested must be even '
                               'integer > 0.')
    else:
        stringlength = 6

    while 1:
        line = sys.stdin.readline()
        if not line:
            break
        latlon = re.findall(r'([-0-9.]+)\s+([-0-9.]+)', line)

        if latlon:
            for leftval, rightval in latlon:
                lat = string.atof(leftval)
                lon = string.atof(rightval)
        else:
            raise RuntimeError('Cannot even get the basic items.')

        astring = maidenhead.mh2(lat, lon, stringlength)
        print('{0}'.format(astring))


if __name__ == '__main__':
    main()
