#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Osman Baskaya"

import sys
import os
import re
import math

key_folder = sys.argv[-1]
pos = sys.argv[1]

var_lines = open(pos+'.var').readlines()

if pos == 'adj':
    pos = 'adjective'

pos = pos + 's'

key_lines = open(os.path.join(key_folder, pos) + '.key')

def calc_perp(sense_list):
    entropy = 0.
    for sense in sense_list:
        entropy += -sense * math.log(sense, 2)
    return 2 ** entropy 

d = {}

for line in key_lines:
    line = line.split()
    key = line[1]
    senses = [float(sense.split('/')[-1]) for sense in line[2:]]
    total = sum(senses)
    senses = [s/total for s in senses]
    perp = calc_perp(senses)
    d[key] = perp

regex = re.compile('<(.*)>')

for line in var_lines:
    line = line.split()
    key = regex.search(line[0]).group(1)
    std = line[1]
    if key in d:
        print "{}\t{}\t{}".format(key, std, d[key])




