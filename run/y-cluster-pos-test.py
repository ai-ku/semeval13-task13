#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import os

assert len(sys.argv) > 2

seed = sys.argv[1]
pos = ['adj', 'verb', 'noun']
kvals = sys.argv[2:]

input_base = "zcat {}.all.scode.gz"
column = "perl -ne 'print if s/^1://'";
kmeans_base = "wkmeans -r 128 -l -w -v -s {} -k {}";
kmeans_out_base = "gzip > kmeans/{}.all.{}.kmeans.gz & "

pairs_base = "zcat {}.all.pairs.100.gz"
word_filter = "grep -P '^<\w+\.\w+\.\d+>'"
sense_find = "./sense-find.py kmeans/{}.all.{}.kmeans.gz > keys/{}.all.{}.key & \n"

process = ""
for k in kvals:
    for p in pos:
        inp = input_base.format(p)
        kmeans = kmeans_base.format(seed, k)
        out = kmeans_out_base.format(p, k)
        process += ' | '.join([inp, column, kmeans, out])

os.system(process + "wait")

process = ""
for k in kvals:
    for p in pos:
        inp = pairs_base.format(p)
        script = sense_find.format(p, k, p, k)
        process += ' | '.join([inp, word_filter, script])

os.system(process + "wait")

