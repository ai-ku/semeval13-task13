#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Osman Baskaya"

import sys
import os
import re
import math
from collections import defaultdict as dd

key_folder = sys.argv[-1]
pos = sys.argv[1]

var_file = open(pos+'.var').read()

if pos == 'adj':
    pos = 'adjective'

pos = pos + 's'

key_lines = open(os.path.join(key_folder, pos) + '.key')


#d[image.n] = {s1:[], s2:[]}


def calc_perp_dict(d):
    entropy = 0.
    tt = [(key, len(val)) for key, val in d.iteritems()]
    total = sum([x[1] for x in tt])
    for i, j in tt:
        p = j / total
        entropy += -p * math.log(p, 2)
    return 2 ** entropy

def calc_perp_dict_graded(d):
    entropy = 0.
    tt = [(key, len(val)) for key, val in d.iteritems()]
    total = sum([x[1] for x in tt])
    for i, j in tt:
        p = j / total
        entropy += -p * math.log(p, 2)
    return 2 ** entropy
    

def calc_perp(sense_list):
    entropy = 0.
    for sense in sense_list:
        entropy += -sense * math.log(sense, 2)
    return 2 ** entropy 

d = dd(lambda: dd(list))

for line in key_lines:
    line = line.split()
    key = line[0]
    sense_classes = [sense.split('/')[0] for sense in line[2:]]
    sense_grades = [float(sense.split('/')[-1]) for sense in line[2:]]
    for c, g in zip(sense_classes, sense_grades):
        d[key][c].append(g)


for word in d.keys():
    reg = '<{}.\d+>\t(\d\.\d+)'.format(word)
    co = re.findall(reg, var_file)
    mean_std = sum([float(val) for val in co]) / len(co)
    print "{}\t{}\t{}".format(word, mean_std, calc_perp_dict(d[word]))

#for line in var_lines:
    #line = line.split()
    #key = regex.search(line[0]).group(1)
    #std = line[1]
    #if key in d:
        #print "{}\t{}\t{}".format(key, std, d[key])




