#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import os
import glob
#from utils import get_uniq_field

path = sys.argv[1]

#if sys.argv[2] != None:
    #ind = sys.argv[2]
#get_uniq_field(path, ind=ind)

ext = "*.eval"
files = glob.glob(os.path.join(path, ext))
files.sort()

for fname in files:
    print >> sys.stderr, fname
    lines = open(fname)
    c = 0
    for line in lines:
        line = line.strip()
        if line.startswith('---'):
            c += 1
            continue
        elif line.startswith('===') and c>0:
            break
        if c>0:
            print line



