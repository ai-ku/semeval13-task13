#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys

files=sys.argv[1].split()


for fn in files:
    f = open("new/"+fn, 'w')
    for line in open(fn):
        line = line.split()
        tw = line[0].rsplit('.', 1)[0]
        line.insert(0, tw)
        f.write(' '.join(line))
        f.write('\n')
    f.close()

