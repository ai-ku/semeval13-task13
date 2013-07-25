#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
some modification on find-sense-test.py in order to use pos approach

"""

from collections import defaultdict as dd
import gzip
import re
import sys

cluster = {}
for line in gzip.open(sys.argv[1]):
    line = line.strip().split("\t")
    cluster[line[0]] = line[1]

match = re.compile("<(\w+\.\w+)\.([^>]+)>")
sense_word_counts = dd(lambda: dd(lambda: dd(int)))
for line in sys.stdin:
    line = line.strip().split("\t")
    m = match.search(line[0])
    sense_word_counts[m.group(1)][m.group(2)][cluster[line[1]]] += 1


for word in sense_word_counts.keys():
    sense_counts = sense_word_counts[word]
    for instance, counts in sense_counts.iteritems():
        print "%s %s %s" % (word,
                word + '.' + instance,
                ' '.join(("%s.%s/%d" % (word, x[0], x[1]) for x in counts.iteritems())))


