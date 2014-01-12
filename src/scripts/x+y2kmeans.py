#!/usr/bin/env python

from collections import defaultdict as dd
import gzip
from optparse import OptionParser
import sys

parser = OptionParser(usage='Finds unique x-y pairs and concatenates their vectors. Requires scode output to stdin.')
parser.add_option('-p', '--pairs', dest='pairs', help='wordsub output')

(options, args) = parser.parse_args()

assert(options.pairs)

if options.pairs.endswith('.gz'):
    f = gzip.open(options.pairs)
else:
    f = open(options.pairs)

pairs = dd(int)
for line in f:
    line = line.strip().split("\t")
    pairs[(line[0], line[1])] += 1
f.close()

scode_x = {}
scode_y = {}
for line in sys.stdin:
    if line.startswith('0:'):
        add_to = scode_x
    elif line.startswith('1:'):
        add_to = scode_y
    line = line[2:].strip().split("\t")
    add_to[line[0]] = "\t".join(line[2:])

for pair, count in pairs.iteritems():
    word, sub = pair
    if scode_x.get(word) and scode_y.get(sub):
        print "%s][%s\t%d\t%s\t%s" % (word, sub, count, scode_x[word], scode_y[sub])
