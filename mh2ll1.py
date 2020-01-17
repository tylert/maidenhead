#!/usr/bin/env python

# maiden2lonlat -- Maidenhead grid to long/lat calculator not limited to 6
#                  characters
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003


import sys

import maidenhead


def main():

    while 1:
        mh = sys.stdin.readline()
        if not mh:
            break
        lat, lon = maidenhead.latlon1(mh)
        print('{0} {1}'.format(lat, lon))


if __name__ == '__main__':
    main()
