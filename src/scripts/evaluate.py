#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


import sys
#import os

# arguments

from optparse import OptionParser
from collections import Counter
from itertools import chain

### Input Parsing ###
parser = OptionParser()
parser.add_option("-m", "--multiple", dest="multi", default='0',
                  help="multiple clustering results", metavar="MULTIPLE_CLUST")
parser.add_option("-g", "--goldfile", dest="gold_file", default='',
                  help="gold file related to input", metavar="GOLDFILE")
(opts, args) = parser.parse_args() 

multi = False
if opts.multi > 0:
    multi = True

g_lines = open(opts.gold_file).readlines()


for i, line in enumerate(sys.stdin):
    line = line.split()
    denominator = len(line)
    counter = Counter(line)
    values = map(lambda x: x/float(denominator), counter.values())
    infor = g_lines[i].split()[:2]
    
    tuples = zip(counter.keys(), values)
    ans = list(chain(*tuples))

    out = ' sense{}/{}' * len(counter.keys())

    print ' '.join(infor) + out.format(*ans)




