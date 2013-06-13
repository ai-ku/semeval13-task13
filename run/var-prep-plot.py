#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys
import os
import re

key_folder = sys.argv[-1]
pos = sys.argv[1]

var_lines = open(pos+'.var').readlines()

if pos == 'adj':
    pos = 'adjective'

pos = pos + 's'

key_lines = open(os.path.join(key_folder, pos) + '.key')


d = {}

for line in key_lines:
    line = line.split()
    key = line[1]
    num_sense = len(line) - 2
    d[key] = num_sense

regex = re.compile('<(.*)>')

for line in var_lines:
    line = line.split()
    key = regex.search(line[0]).group(1)
    std = line[1]
    if key in d:
        print "{}\t{}\t{}".format(key, std, d[key])



