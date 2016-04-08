#!/usr/bin/python
# lonlat2maiden -- long/lat to Maidenhead grid calculator not limited to 6 characters
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003
# Last Modified On: Fri Nov 28 06:00:24 2003
# Update Count    : 175
import re,sys,string
if len(sys.argv)==2: # slob city
    stringlength=string.atoi(sys.argv[1])
    if stringlength<2 or stringlength%2!=0:
        sys.stderr.write('string length requested must be even integer > 0\n')
        sys.exit(87)
else:
    stringlength=6
maxn=stringlength/2
A=ord('A')
while 1:
    line=sys.stdin.readline()
    if not line: break
    ll=re.findall(r'([-0-9.]+)\s+([-0-9.]+)',line)
    if ll:
        for x,y in ll:
            lon=string.atof(x)
            lat=string.atof(y)
    else:
        sys.stderr.write(sys.argv[0]+': cannot even get the basic items\n')
        sys.exit(44)
    if -180<=lon<180:pass
    else:
        sys.stderr.write('longitude must be -180<=lon<180\n')
        sys.exit(32)
    if -90<=lat<90:pass
    else:
        sys.stderr.write('latitude must be -90<=lat<90\n')
        sys.exit(33) #can't handle north pole, sorry, [A-R]
    a=divmod(lon+180,20)
    b=divmod(lat+90,10)
    astring=chr(A+int(a[0]))+chr(A+int(b[0]))
    lon=a[1]/2
    lat=b[1]
    i=1
    while i<maxn:
        i+=1
        a=divmod(lon,1)
        b=divmod(lat,1)
        if not(i%2):
            astring+=str(int(a[0]))+str(int(b[0]))
            lon=24*a[1]
            lat=24*b[1]
        else:
            astring+=chr(A+int(a[0]))+chr(A+int(b[0]))
            lon=10*a[1]
            lat=10*b[1]
    print astring
#We return the grid square, to the precision given, that contains the given point.
