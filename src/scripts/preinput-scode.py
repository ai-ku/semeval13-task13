#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys
from itertools import count

"""
Dists input should be a specific format:
<n:number of elements in the row> <c_i:column id> <c_i_v:column val> ... <c_n:column id> <c_n_v:column val>

preinput.py is for fastsub
preinput-scode for scode in order to calculate KNN
---------------------------------------------------------------

INPUT:
zcat scode/add.v.scode.gz  | grep -P "^0:" | cut -f3- | ./preinput-scode.py 
----

zcat scode/add.v.scode.gz  | grep -P "^0:" | cut -f3- | ./preinput-scode.py | ../bin/dists -k 100 -d 0

"""

for line in sys.stdin:
    c = count()
    line = line.split()
    n = len(line)
    for i in xrange(0,n*2,2):
        line.insert(i, str(c.next()))
    line.insert(0, str(n))
    print ' '.join(line)





