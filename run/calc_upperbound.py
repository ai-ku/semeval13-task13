#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

"""
call example: 

zcat knn/fastsub/add.v.knn.gz | ./knn-eval.py -g <(cat {} |
grep -P "{} ") -i <(zcat target.sub.gz | grep -P "^<{}\.\d{{1,3}}>" | 
cut -f1 | sed 's/[<>]//g') -t fastsub >> eval/fastsub.knn.{}.ans"""

import sys
import os 
import subprocess
import re
from collections import defaultdict as dd

keyfile = sys.argv[1]
t = sys.argv[2]
FILES=sys.argv[3:]

K=5 #number of neighbor


out_file_dict = dd(lambda: False)

def check_remove(outfile):
    if not out_file_dict[outfile]:
        if os.path.exists(outfile):
            os.remove(outfile)
        out_file_dict[outfile] = True

def run(command, out, files=FILES, r='(\w+\.\w+)\.knn\.(\d)\.gz'):
    for f in files:
        regex = re.compile(r)
        tw, d = get_tw_d(regex, os.path.basename(f))
        outfile = out.format(K, d)
        print >> sys.stderr, outfile
        check_remove(outfile)
        c = command.format(f, keyfile, tw, tw, K, outfile)
        print >> sys.stderr, tw
        print >> sys.stderr, c
        subprocess.call(c, shell=True, executable='/bin/bash')

def get_tw_d(regex, basename):
    g = regex.search(basename)
    tw = g.group(1)
    d = g.group(2)
    return (tw, d)

# Main #
#FIXME: Duzelt buralari. in ['fastsub', 'scode'] sonra direk type'i bas command'e.
if t == 'fastsub':
    print >> sys.stderr, "fastsub upperbound calc started"
    command = """./knn-eval.py -s {} -g <(cat {} |
             grep -P "{} ") -i <(zcat target.sub.gz | grep -P "^<{}\.\d{{1,3}}>" | 
             cut -f1 | sed 's/[<>]//g') -t fastsub -k {} >> {} """
    out = "eval/fastsub.knn{}.{}.ans"
    run(command, out)
elif t == 'scode':
    print >> sys.stderr, "scode (X) upperbound calc started"
    command = """./knn-eval.py -s {} -g <(cat {} |
             grep -P "{} ") -i <(zcat target.sub.gz | grep -P "^<{}\.\d{{1,3}}>" | 
             cut -f1 | sed 's/[<>]//g') -t scode -k {} >> {} """
    out = "eval/scode.knn{}.{}.ans"
    run(command, out)
else:
    raise ValueError, 'wrong argument: input scode or fastsub'
