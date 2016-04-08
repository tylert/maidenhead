#!/usr/bin/env python

# gpsdll2mh.py
#
# G1OGY 20081102
#
# `gpsdll2mh.py` is a `gpsd' [http://gpsd.berlios.de] console-client which
# prints Maidenhead LOCATOR at user-determined, arbitary, even-number
# precision; (GPS precision max=52 - it gets quite silly long before that).
#
# PREREQUISITES: this program requires access to a running `gpsd' daemon 
# (with a GPS receiver attached and functional).
#
# `gpsdll2mh.py` is intended for 'Rover-style' operation ( WAB, WAS, perhaps)
# so that one's 'new' locator can be sent as soon as it becomes apparant.
# It will also assist in calculating a (static) locator to a greater
# precision for microwave dish aiming purposes.
#
# 
#
# Command line args are supported to select Locator precision (default=6);
# repeat frequency; server:port 
#
#
# Command line (console) usage:
#
#       python gpsdll2mh.py [[[precision] [repeat]] [server:port]]] <additive>
#
# like: python gpsdll2mh.py 10 30 (on a linux laptop running gpsd)
# or  : python gpsdll2mh.py 10 30 192.168.1.99:2947 (on a (Windows) laptop connecting
#						     to linux server on standard port)
# so:		10-char locator evey 30 seconds 
#
#
# Credits:
# The Lat/Long to Maidenhead part of this program is a rework of an original script by 
# Dan Jacobson -- http://jidanni.org/geo/maidenhead/ ; latterly updated by Rene Kanter.
#
## lonlat2maidenhead -- long/lat to Maidenhead grid calculator not limited to 6 characters
## Created On      : Sat Mar 15 03:54:08 2003
## rkanters 2004.2.20 version ll2mh
#
# Thank you, gentlemen.
#

#
# gpsdll2mh.py Program code
# -------------------------


# get modules
import re, sys, string
from time import sleep
from socket import *

# Set variables (defaults)
gpsdHost = 'localhost'
gpsdPort = 2947                         # gpsd default (IANA)
gpsdCall = ['p']                        # fixed gpsd command for 'position'

# print usage at default (no args) start ('cos of cheap way to do command-line args)
print '\n***********************************************************************'
print '\n',sys.argv[0],

# Ah! running with no args
if len(sys.argv)<2:
    print "Running : 6-char LOC, 5 sec rptr, `gpsd' is local, default port \n"
    print 'Usage:'
    print '      ',sys.argv[0],'[[[LOC Precision] [Repeat delay]] [Server:port]]]\n'
# Abort!
print '\nINFO :: ** Ctrl-C to stop **\n\n'

# Ah! Now have args to chobble...
# validate the input precision value: must have an even number
if len(sys.argv)>1:
    loclen=int(sys.argv[1])
    if loclen<2 or loclen%2!=0:
        sys.stderr.write('ERROR :: Locator precision requested must be an even number \n\n')
        sys.exit(87)
else:
    loclen=6                            # why report only Square? (won't often change unless you're in a 'plane!)
                                        # if only sqare is needed then '4' on cmd line
                                        
maxn=loclen/2                           # program constant

# grab or set repeat value
if len(sys.argv)>2:
    snooze=int(sys.argv[2])
else:
    snooze = 5                          # seconds


# gpsd network server
if len(sys.argv)>3:
     sp = sys.argv[3].split(":")
     gpsdHost=sp[0]
     gpsdPort=int(sp[1])
print 'INFO :: Connecting to :  ', gpsdHost,':',gpsdPort,'\n'

# Networking
# create local socket
gpsdSock = socket(AF_INET, SOCK_STREAM)

# connect to gpsd daemon
try:
    gpsdSock.connect((gpsdHost, gpsdPort))
except Exception, e:
    print " FATAL ERROR :: Cannot connect to `gpsd'!\n"
    print "Is `gpsd' running? Is your server:port address correct?\n"
    print "System message ::" , e ,'\n'
    

# send position query, receive response and calculate LOCATOR
# ~persevere~ if daemon is recalcitrant
try:
    while 1:
        for Query in gpsdCall:
            gpsdSock.send(Query)
            data = gpsdSock.recv(32)
            if len(data)<12:
                break
            latlong = data[7:]

            A=ord('A')                  # set a base value for the calcs.
            
# Following commented code originally allowed for manual entry of the lat/long values - 
# I'll revisit this sometime so that there's a stand-alone option.
# run the prog with a switch - it sits and waits for input: LAT.###### <space> LONG.###### [CR]
# JIC the OPS have only a handheld GPS or Sat-Nav system available.
##            
### while 1:
###    line=sys.stdin.re adline()
###    if not line: break
###    ll=re.findall(r'([-0-9.]+)\s+([-0-9.]+)',line)
##

            ll=re.findall(r'([-0-9.]+)\s+([-0-9.]+)',latlong)
            if ll:
                for x,y in ll:
                    lat=float(x)
                    lon=float(y)
            else:
                sys.stderr.write(sys.argv[0]+': ERROR :: Cannot determine LAT / LONG. Is ''`gpsd'' running?\n\n')
                sys.exit(44)
                if -180<=lon<180: pass
                else:
                    sys.stderr.write('ERROR :: longitude must be -180<=lon<180\n\n')
                    sys.exit(32)
                
            if -90<=lat<90: pass
            else:
                sys.stderr.write('ERROR :: latitude must be -90<=lat<90\n\n')
                sys.exit(33)                    # can't handle north pole, sorry, [A-R]
                
            lon=(lon+180.0)/20                  # scale down and set up for first digit
            lat=(lat+90.0)/10
            mhloc=""
            i=0
            while i<maxn:
                i+=1
                loni=int(lon)
                lati=int(lat)
                if i%2:
                    mhloc+=chr(A+loni)+chr(A+lati)
                    lon=(lon-loni)*10
                    lat=(lat-lati)*10
                else:
                    mhloc+=str(loni)+str(lati)
                    lon=(lon-loni)*24
                    lat=(lat-lati)*24
            
# print lat/long 'cos a short (<12) locator won't update much 
# (unless you've got the hammer down)                 

            print 'Lat / Long: ', latlong, 'Locator:    ', mhloc, '\n'      # main output
            sleep(snooze)                                                   # repeat delay
# Close down            

except KeyboardInterrupt:                       # inhibits the traceback on exit
    gpsdSock.shutdown(1)
    gpsdSock.close()
            
# returns the grid square, to the precision given, that contains the given point.
#


# TO DO
# DONE! Trap no valid GPS Data - if GPS device is unplugged gpsd continues but provides `?'

# DONE! Trap no gpsd daemon - can't connect
# Esoteric...
    # keep count (and display on close) of all Fields [IO, JO, JN], Squares [JO01, IO91, JP63] 
    # and Sub-Squares [JO01BR, JO01HQ] traversed on the journey.
    # 3 counters inside. Storage??  mySQL-Lite??
    # print 'em ???
