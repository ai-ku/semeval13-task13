#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import os

__author__ = "Osman Baskaya"


# Some parameters
k= 100
metrics = [0, 1, 2, 3, 4]
ncpu = 1
option = "-k {} -d {} -p {}"

# inputs
inp_file = sys.argv[1]
words = sys.argv[2:]

template = "zcat {} | grep -P '^<{}\.\d{{1,3}}>' |  preinput.py | dists {} | gzip > knn/fastsub/{}.knn.{}.gz & \n "

for word in words:
    command = ""
    for m in metrics:
        opt = option.format(k, m, ncpu)
        command += template.format(inp_file, word, opt, word, m)
    command += "wait"
    print >> sys.stderr, command
    os.system(command)




