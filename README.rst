Maidenhead
==========

* http://jidanni.org/geo/maidenhead/index.html
* https://en.wikipedia.org/wiki/Maidenhead_Locator_System

From wikipedia...

To simplify manual encoding, the base for the first pair of
letters—traditionally called a field—was chosen to be 18, thus dividing the
globe into 18 zones of longitude of 20° each, and 18 zones of latitude 10°
each. These zones are encoded with the letters "A" through "R".

The first pair of numbers, called a square and placed after the first pair of
letters, uses a base number of 10, and is encoded using the digits "0" to "9".
This is where the alternative name "grid squares" comes from. Each of these
squares represents 1° of latitude by 2° of longitude.

For additional precision, each square can optionally be sub-divided further,
into subsquares. These are encoded into a second pair of letters, often (but
not always) presented in lowercase, and again, to make manual calculations from
degrees and minutes easier, 24 was chosen as the base number, giving these
subsquares dimensions of 2.5' of latitude by 5' of longitude. The letters used
are "A" through "X".

The resulting Maidenhead subsquare locator string is hence composed of two
letters, two digits, and two more letters. To give an example, W1AW, the
American Radio Relay League's Hiram Percy Maxim Memorial Station in Newington,
Connecticut, is found in grid locator FN31pr. Two points within the same
Maidenhead subsquare are always less than 12 km apart, which means a Maidenhead
locator can give significant precision from just six easily transmissible
characters.

For even more precise location mapping, two additional digits were proposed and
ratified as an extended locator, making it altogether eight characters long,
and dividing subsquares into even smaller ones. Such precision has uses in very
short communication spans. Beyond this, no common definition exists to extend
the system further into even smaller squares. Most often the extending is done
by repeating alternating subsquare and square rules (base numbers 24 and 10
respectively). However, other bases for letter encodings have also been
observed, and therefore such extended extended locators might not be
compatible.

The Maidenhead locator system has been explicitly based on the WGS 84 geodetic
datum since 1999.[citation needed] Before that time, it was usually based on
each user's local national datum, which do differ slightly from one another and
WGS 84. As a result, stations very near the edges of squares at denoted
precision may have changed their locators when changing over to the use of WGS
84.

To summarise:

Character pairs encode longitude first, and then latitude.
The first pair (a field) encodes with base 18 and the letters "A" to "R".
The second pair (square) encodes with base 10 and the digits "0" to "9".
The third pair (subsquare) encodes with base 24 and the letters "A" to "X".
The fourth pair (extended square) encodes with base 10 and the digits "0" to
"9".

The fifth and subsequent pairs are not formally defined, but recycling the
third and fourth pair algorithms is one possible definition:

BL11BH16oo66
