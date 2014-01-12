#!/usr/bin/env python

from itertools import count, izip
import sys

context = []
for line, i in izip(sys.stdin, count()):
    line = line.split()
    if i % 2 == 0:
        context = line[-4:]
    else:
        context += line[1:4]
        print ' '.join(context)
