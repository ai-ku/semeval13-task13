#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import os

__author__ = "Osman Baskaya"


# Some parameters
k= 100
metrics = [0,1,2,3]
#metrics = [0, 1, 2, 3, 4]
ncpu = 1
option = "-k {} -d {} -p {}"

# inputs
words = sys.argv[1:]

template = "zcat scode_vec/{}.scode.gz  | grep -P '^0:' | cut -f3- | preinput-scode.py | dists {} | gzip > knn/scode/{}.knn.{}.gz & "
#template = "zcat scode/{}.scode.gz  | grep -P '^0:' | cut -f3- | preinput-scode.py | gzip > dummy.gz & "

for word in words:
    command = ""
    for m in metrics:
        opt = option.format(k, m, ncpu)
        command += template.format(word, opt, word, m)
        #command += template.format(word)# opt, word, m)
    command += "wait"
    print >> sys.stderr, command
    os.system(command)
