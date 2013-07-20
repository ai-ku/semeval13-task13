#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

import sys
import re
from nlp_utils import calc_perp_semeval

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
    plist = []
    r = regex.format(tw)
    nsense = 0
    tw_lines = re.findall(r, ff)
    senses = set()
    for line in tw_lines:
        line = line.split()
        count += len(line[2:])
        plist.append(line[2:])
        for ss in line[2:]:
            sense = ss.split('/')[0]
            senses.add(sense)
    total_sense += len(senses)
    print tw, len(senses)


avg_sense = total_sense / len(tw_list)
avg_sense_inst = count / num_inst
avg_perp = calc_perp_semeval(plist)
print "-----"
print "Avg. senses:\t{}\nAvg. # of s for inst\t{}\nAvg. perp\t{}".format(avg_sense,
                                                        avg_sense_inst, avg_perp)
