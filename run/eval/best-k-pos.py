#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


pos = ['noun', 'verb', 'adj']
k = [2, 4, 8, 16, 32, 40, 60, 70, 80, 100, 120]
fname = "{}.{}.scores"

metric_line = 9 # line number of single sense precission in .scores file

for p in pos:
    max_score = -1
    max_k_val = -1
    for i in k:
        f = fname.format(p, i)
        score_line = open(f).readlines()[metric_line]
        score = float(score_line.split()[-1])
        if max_score < score:
            max_score = score
            max_k_val = i
    print "{}\t{}\t{}".format(p, max_k_val, max_score)



