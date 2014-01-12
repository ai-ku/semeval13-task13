#!/usr/bin/env python

import gzip
import re
import sys

part = sys.argv[1]

files = map(lambda x: gzip.open(x + part + '.gz', 'w'), 'tok pos lemma'.split())
lines = [[], [], []]

sentence = False
for line in sys.stdin:
    if line.startswith('<s>'):
        sentence = True
    elif line.startswith('</s>'):
        sentence = False
        for i in xrange(3):
            files[i].write(' '.join(lines[i]) + "\n")
            lines[i] = []
    elif sentence:
        cols = line.strip().split("\t")
        for i in xrange(3):
            lines[i].append(cols[i])

for i in xrange(3):
    files[i].write(' '.join(lines[i]) + "\n")

map(lambda f: f.close(), files)
