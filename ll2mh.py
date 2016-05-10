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


if len(sys.argv) == 2:  # slob city
    stringlength = string.atoi(sys.argv[1])
    if stringlength < 2 or stringlength % 2 != 0:
        sys.stderr.write('string length requested must be even integer > 0\n')
        sys.exit(87)
else:
    stringlength = 6


while 1:
    line = sys.stdin.readline()
    if not line:
        break
    ll = re.findall(r'([-0-9.]+)\s+([-0-9.]+)', line)

    if ll:
        for x, y in ll:
            lon = string.atof(x)
            lat = string.atof(y)
    else:
        sys.stderr.write(sys.argv[0] + ': cannot even get the basic items\n')
        sys.exit(44)

    astring = maidenhead.mh(lat, lon, stringlength)
    print('{0}'.format(astring))
