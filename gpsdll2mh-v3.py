#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# gpsdll2mh.py
#
##########################################################################
#
# Copyright:
#
# G1OGY 20081102  Initial release
#
# G1OGY 20090419: Updated to cope with increased precision of gpsd v2.39
#
# G1OGY 20120218: Updated to cope with major change of API in v2.92
#
##########################################################################
#
# Description:
#
# `gpsd' [http://www.catb.org/gpsd (previously http://gpsd.berlios.de) ]
# console-client which prints Amateur Radio Maidenhead LOCATOR
# at user-determined, arbitary, even-number precision.
#
# (LOCATOR precision max=52 - it gets _quite_ silly long before that).
#
# This program is intended for 'Rover-style' operation (or WAB, perhaps)
# so that one's 'new' locator can be sent as soon as neccessary.
# It will also assist in calculating a (static) locator to a greater
# precision for microwave dish aiming purposes.
#
##########################################################################
#
# Features:
#
# Command line args are supported to select
# Locator precision     (default=6 char)
# repeat frequency      (default=5 seconds)
# server:port           (default=localhost:2947 (IANA))
#
# Requires: access to a `gpsd' daemon > v2.91
#           python interpreter > v2.4 & < v3.x
#
# Command line (console) usage:
#
#       python gpsdll2mh.py [[[precision] [repeat]] [server:port]]]
#
##########################################################################
#
# Credits:
# The Lat/Long to Maidenhead part of this program is a rework of an
# original script by Dan Jacobson -- http://jidanni.org/geo/maidenhead/ ;
# latterly updated by Rene Kanter.
#
# lonlat2maidenhead -- long/lat to Maidenhead grid calculator not limited
# to 6 characters.
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003
# rkanters 2004.2.20 version ll2mh
#
# Thank you, gentlemen.
#
##########################################################################
#
# Licence:
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#      http://www.gnu.org/licenses/gpl.html
#
#
##########################################################################
#

# get modules
import re
import sys
import string
import os
import gps
from time import sleep

# Set variables (defaults)
gpsdHost = 'localhost'
gpsdPort = 2947                         # gpsd default (IANA)

# print usage at default start ('cos of my cheap way to do cmd-line args parse)
print '\n***********************************************************************'
print '\n', sys.argv[0], '\n'
if len(sys.argv) < 2:
    print "Running : 6-char LOC, 5 sec rptr, `gpsd' local, default \n"
    print 'Usage:'
    print '      ', sys.argv[0], '[[[LOC Precision] [Repeat delay]] [Server:port]]]\n'
# Abort!
print '\nINFO :: ** Ctrl-C to stop **\n\n'

# validate the input precision value: even number
if len(sys.argv) > 1:
    loclen = int(sys.argv[1])
    if loclen < 2 or loclen % 2 != 0:
        sys.stderr.write(
            'ERROR :: Locator precision requested must be an even number \n\n')
        sys.exit(87)
else:
    # why report only Square? (it won't often change unless you're airborne!)
    loclen = 6
    # if only Square is really? needed: then '4'
maxn = loclen / 2

# grab or set repeat value
if len(sys.argv) > 2:
    snooze = int(sys.argv[2])
else:
    snooze = 5                          # seconds


# gpsd network server
if len(sys.argv) > 3:
    sp = sys.argv[3].split(":")
    gpsdHost = sp[0]
    gpsdPort = int(sp[1])
print 'INFO :: Connecting to :  ', gpsdHost, ':', gpsdPort, '\n'


# connect to gpsd daemon: python gps API interface handles the intricacies
try:
    gpsdSock = gps.gps(host=gpsdHost, port=gpsdPort, mode=gps.WATCH_NEWSTYLE)

except Exception, e:
    print " FATAL ERROR :: Cannot connect to `gpsd'!"
    print "  Is `gpsd' running? Is your server:port address correct?\n"
    print "  System message ::", e, '\n'
    sys.exit(87)

gpsdSock.stream()

# Pause to show usage - User may comment this out (add # ahead of raw_input)
# to go straight to the display
raw_input("Press ENTER to continue")

try:
    while True:
        os.system('clear')
        if gps.PACKET_SET:
            gpsdSock.poll()
        if gpsdSock.fix.latitude:
            latlong = `gpsdSock.fix.latitude` +' ' + `gpsdSock.fix.longitude`
            # need float, numeric


# comment block retained from v2 of the program, just to keep it front-of-mind

# Following commented code allowed for manual entry of the lat/long values -
# maybe I'll revisit this sometime.
#
# while 1:
# line=sys.stdin.re adline()
# if not line: break
# ll=re.findall(r'([-0-9.]+)\s+([-0-9.]+)',line)
#

            ll = re.findall(r'([-0-9.]+)\s+([-0-9.]+)', latlong)
            if ll:
                for x, y in ll:
                    glat = float(x)
                    glon = float(y)
            else:
                sys.stderr.write(sys.argv[
                                 0] + ': ERROR :: Cannot determine LAT / LONG.  Is ''`gpsd'' running?\n\n')
                sys.exit(44)

            if -180 <= glon < 180:
                pass
            else:
                sys.stderr.write(
                    'ERROR :: longitude must be -180<=glon<180\n\n')
                sys.exit(32)

            if -90 <= glat < 90:
                pass
            else:
                sys.stderr.write('ERROR :: latitude must be -90<=lat<90\n\n')
                # can't handle North pole, sorry, [A-R]
                sys.exit(33)

            # scale down and set up for first digit
            glon = (glon + 180.0) / 20
            glat = (glat + 90.0) / 10
            mhloc = ""
            i = 0
            while i < maxn:
                i += 1
                loni = int(glon)
                lati = int(glat)
                if i % 2:
                    mhloc += chr(ord('A') + loni) + chr(ord('A') + lati)
                    glon = (glon - loni) * 10
                    glat = (glat - lati) * 10
                else:
                    mhloc += str(loni) + str(lati)
                    glon = (glon - loni) * 24
                    glat = (glat - lati) * 24

# print lat/long 'cos a short (<12) locator won't update much
# (unless you've got the hammer down)

            print 'Lat / Long: ', latlong, '\n', 'Locator:    ', mhloc, '\n'
            sleep(snooze)

# Close down

except KeyboardInterrupt:                       # inhibits the traceback on exit
    gpsdSock.close()

# returns the grid square, to the precision given, that contains the given point.
#
