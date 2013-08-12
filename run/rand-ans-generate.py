#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


""" Random answer key creator """

import sys
import random
from collections import defaultdict as dd

if len(sys.argv) == 4:
    induced = bool(int(sys.argv[1]))
    k = int(sys.argv[2])
    keyfile = sys.argv[3]
else:
    print "usage: {} is_induced k keyfile".format(sys.argv[0])
    exit(1)


lines = open(keyfile).readlines()


if induced: # induced senses
    for line in lines:
        r = random.randint(1, k)
        line = line.split()[:2]
        print ' '.join(line), r
else: # wordnet senses 
    senses = dd(set)
    for line in lines:
        line = line.split()
        senses[line[0]].add(line[2].split('/')[0])
    wn = dict()
    for s in senses: # convert a list to index it
        wn[s] = list(senses[s])
    for line in lines:
        line = line.split()
        tw = line[0]
        r = random.randint(0, len(wn[tw]) - 1)
        print ' '.join(line[:2]), wn[tw][r]
