#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

""" 
wordsub -> scode -> wkmeans sonrasinda

Y'ler tamamiyle unique olmadigindan oturu  wordsubs kadar gruplara ayrilmiyor
kmeans sonuclari. O yuzden bir mapping gerekiyor.

"""

import sys
import re
import gzip
#from collections import defaultdict as dd

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]


if len(sys.argv) != 6:
    print "Wrong number of parameters"
    exit(1)

cluster_ans = sys.argv[1] # answer key
scode_file = sys.argv[2]
wordsub_file = sys.argv[3]
field = int(sys.argv[4])  # 0 or 1 (0 for X, 1 for Y)
nsub = int(sys.argv[5]) # number of wordsub used

if field == 0 or field == 1:
    regex = r'%d:.*' % field
else:
    regex = r'[1|0]:.*'

sc_lines = gzip.open(scode_file).read()
sc = re.findall(regex, sc_lines)

clabels = map(str.strip, open(cluster_ans).readlines()) # cluster labels
sc_subs = [line.split()[0][2:] for line in sc] # target words or wordsubs depends on regex

d = dict(zip(sc_subs, clabels))
assert len(sc_subs) == len(clabels)
wordsubs = [line.split()[1] for line in gzip.open(wordsub_file).readlines()]
mapped_labels = [d[w] for w in wordsubs]
answers = chunks(mapped_labels, nsub)

for inst in answers:
    print ' '.join(inst)
