#!/usr/bin/env python


import sys

from maidenhead import latlon2


def main():

    while 1:
        mh = sys.stdin.readline()
        if not mh:
            break
        lat, lon = latlon2(mh)
        print('{0} {1}'.format(lat, lon))


if __name__ == '__main__':
    main()
