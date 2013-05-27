#!/usr/bin/env python

from itertools import izip
import gzip
import sys

lemma = []
pos = []
for l, p in izip(gzip.open(sys.argv[1]), gzip.open(sys.argv[2])):
    l = l.split()
    p = p.split()
    assert(len(l) == len(p))
    for l, p in izip(l, p):
        lemma.append(l)
        if p != 'NP' and p != 'NPS':
            pos.append(p[0].lower())
        else:
            pos.append('x')

write_to = [gzip.open("verb.sub.gz", 'w'),
            gzip.open("noun.sub.gz", 'w'),
            gzip.open("adj.sub.gz", 'w')]
for line, l, p in izip(sys.stdin, lemma, pos):
    line = line.split("\t")
    line[0] = l + '.' + p
    if p == 'v':
        write_to[0].write("\t".join(line))
    elif p == 'n':
        write_to[1].write("\t".join(line))
    elif p == 'j':
        write_to[2].write("\t".join(line))
