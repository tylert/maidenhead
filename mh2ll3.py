#!/usr/bin/env python
# mh2ll -- Maidenhead grid to long/lat calculator not limited to 6 characters
# Copyright       : http://www.fsf.org/copyleft/gpl.html
# Author          : Dan Jacobson -- http://jidanni.org/geo/maidenhead/
# Created On      : Sat Mar 15 03:54:08 2003

# rkanters 2004.2.20 version mh2ll3

# if one assumes no input errors, we could change the whole val stuff all together:
A=ord('A');Zero=ord('0')
import sys, string
# c2v converts a letter or digit to the value above A or 0 (assume no nonsence
# characters passed to the function...
# since it is used for both the longitude and latitude characters I made it
# into a function as opposed to expanding the if/then/else twice in the body code
def c2v(c):
	c = ord(string.upper(c))
	if c >= A:
		v = c-A
	else:
		v = c-Zero
	return v
while 1:
	mh=sys.stdin.readline()
	if not mh: break
	lon=lat=-90.0
	i=0
	res = 10.0	# the initial resolution of the grid in degrees
	npair = len(mh)/2
	while i<npair:
		lon += res*c2v(mh[2*i])
		lat += res*c2v(mh[2*i+1])
		# calculate the alternating 10,24 resolution increment for the next
		# grid level, i.e., 10,24,10,24, etc.
		if i%2:	# calculate the resolution for the next subgrid
			res /= 24.0
		else:
			res /= 10.0
		i += 1
	lon*=2
	print lon,lat
