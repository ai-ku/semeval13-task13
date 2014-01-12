#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
from collections import defaultdict as dd

""" Vocabulary statistics for HDP input """
__author__ = "Osman Baskaya"


tw = sys.argv[1]
lemma = tw.split('.')[0]

file_d = dd(int)
numsent = 0
line_d = dd(int)
num = 0
maximum = 0

for line in sys.stdin:
    line = line.split()
    if line[0] == '<sentence>' and len(line_d) > 0:
        maximum += sorted(line_d.items(), key=lambda x: x[1], reverse=True)[0][1]
        line_d = dd(int)
        numsent += 1
    else:
        if len(line) == 3 and line[2] != '<unknown>':
            line_d[line[2]] += 1
            file_d[line[2]] += 1
        elif len(line) == 1:
            line_d[line[0]] += 1
            file_d[line[0]] += 1

tt = sorted(file_d.items(), key=lambda x: x[1], reverse=True)
print "{:<20}\t{:<20}\t{:<20}\t{:<20}".format(tw, maximum / numsent, file_d[lemma] / sum(file_d.values()), tt[:5])









