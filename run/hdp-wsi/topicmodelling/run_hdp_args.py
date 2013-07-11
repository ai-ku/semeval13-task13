#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys

max_iter = sys.argv[1]
gamma_b = sys.argv[2]
alpha_b = sys.argv[3]


files = sys.argv[4:]

tfile = '/hdpdata.train.txt' #training file

command = "--algorithm train --data {} --directory {}  --max_iter {} --save_lag -1 --gamma_b {} --alpha_b {}"

for f in files:
    print command.format(f+tfile, f, max_iter, gamma_b, alpha_b)
