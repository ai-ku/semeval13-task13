#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


""" Random answer key creator """

import sys
import random
from collections import defaultdict as dd

if len(sys.argv) == 2:
    keyfile = sys.argv[1]
else:
    print "usage: {} keyfile".format(sys.argv[0])
    exit(1)


files = map(lambda x: open('eval/rand.exp.' + x + '.ans', 'w'), ['induced', 'wn'])


lines = open(keyfile).readlines()
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
    k = len(wn[tw]) - 1
    
    r = random.randint(0, k)
    s = ' '.join(line[:2]) +  ' ' + str(r) + '\n'
    files[0].write(s)

    r = random.randint(0, k)
    s = ' '.join(line[:2]) + ' ' +  wn[tw][r] + '\n'
    files[1].write(s)


map(lambda f: f.close(), files)
