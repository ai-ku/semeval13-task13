#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
files = sys.argv[1].split()

ADDITIONAL = 1000


for f in files:
    numline = len(open(f).readlines())
    print f[:-6], numline-1000
