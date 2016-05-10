#!/usr/bin/env python


# mh2ll -- Maidenhead grid to long/lat calculator not limited to 6 characters
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003

# rkanters 2004.2.20 version mh2ll2


import sys
import maidenhead


while 1:
    mh = sys.stdin.readline()
    if not mh:
        break
    lat, lon = maidenhead.ll2(mh)
    print('{0} {1}'.format(lon, lat))
