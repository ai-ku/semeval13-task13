#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
__author__ = "Osman Baskaya"

import sys
import re

PATH="eval/"

filename = sys.argv[1]
f = open(PATH + filename)

target_words = set()
lines = f.readlines()
num_inst = len(lines)

for line in lines:
    line = line.split()
    target_words.add(line[0])


tw_list = list(target_words)
tw_list.sort()

f.seek(0) # reset the file
ff = f.read()
regex = "{} .*\n"
total_sense = 0
count = 0
for tw in tw_list:
    r = regex.format(tw)
    nsense = 0
    tw_lines = re.findall(r, ff)
    senses = set()
    for line in tw_lines:
        line = line.split()
        count += len(line[2:])
        for ss in line[2:]:
            sense = ss.split('/')[0]
            senses.add(sense)
    total_sense += len(senses)
    print tw, len(senses)
print "-----\nAverage senses: {}".format(total_sense / len(tw_list))
print "Average # of senses for instance: {}".format(count / num_inst)
