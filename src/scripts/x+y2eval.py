#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import gzip
#from collections import defaultdict as dd

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]



#TODO: option parser
if len(sys.argv) != 5:
    print "Wrong number of parameters"
    exit(1)

cluster_ans = sys.argv[1] # cluster output file
xy_file = sys.argv[2] # x+y2kmeans output
wordsub_file = sys.argv[3] # wordsub output
nsub = int(sys.argv[4]) # number of wordsub used


xy_pairs = [line.split()[0] for line in open(xy_file).readlines()]
clabels = map(str.strip, open(cluster_ans).readlines()) # cluster labels

d = dict(zip(xy_pairs, clabels))
assert len(xy_pairs) == len(clabels)

wordsubs_pairs = [line.split() for line in gzip.open(wordsub_file).readlines()]
wordsubs = map(lambda x: x[0] + '_' + x[1], wordsubs_pairs)

mapped_labels = [d[w] for w in wordsubs]
answers = chunks(mapped_labels, nsub)

for inst in answers:
    print ' '.join(inst)
