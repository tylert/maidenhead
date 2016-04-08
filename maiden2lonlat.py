#!/usr/bin/env python
# maiden2lonlat -- Maidenhead grid to long/lat calculator not limited to 6 characters
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003
# Last Modified On: Fri Nov 28 05:58:24 2003
# Update Count    : 333
A=ord('A');safety=22
import re, sys, string
def f(z):
    return 10**(-(z-1)/2)*24**(-z/2) #this is my stroke of genius or something
while 1:
    line=sys.stdin.readline()
    if not line: break
    lon=lat=-90
    lets=re.findall(r'([A-Xa-x])([A-Xa-x])',line) #slob: assume no input errors
    nums=re.findall(r'(\d)(\d)',line) #slob: assume no input errors
    if len(lets)+len(nums)>safety:
        #print sys.argv[0]+ ': you want more than', safety*2, 'digits'
        # how to do 1>&2 in python? I suppose:
        sys.stderr.write(sys.argv[0]+ ': you want more than '+str(safety*2)+' digits\n')
        sys.exit(22) #crappy length check
    i=tot=0
    val=range(0,safety) #sorry I don't know how to do this
    for m in val: #i seem to need an empty array
        val[m]=None #so so silly
    for x,y in lets:
        val[i*2]=(ord(string.upper(x))-A,ord(string.upper(y))-A)
        i+=1
        tot+=1
    for x in val[0]:
        if x>=18: #only now do we do a crappy error check for S...
            sys.stderr.write('invalid data in first two letters\n')
            sys.exit(37)
    i=0
    for x,y in nums:
        val[i*2+1]=(string.atoi(x),string.atoi(y))
        i+=1
        tot+=1
    i=0
    for x,y in val[0:min(tot,safety-1)]:
        lon+=f(i-1)*x
        lat+=f(i-1)*y
        i+=1
    lon*=2
    print lon,lat
