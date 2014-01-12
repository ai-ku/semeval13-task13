#! /usr/bin/python
# -*- coding: utf-8 -*-


import os

#zcat noun.all.scode.gz | grep -P '^(0:<.*\.\d{1,3}>)|(^1:)' | gzip > noun.variance.scode.gz

pos = 'noun verb adj'.split()
reg1 = "grep -P '(^0:<.*\.\d{1,3}>)|(^1:)'"
reg2 = "grep -P '^<.*\.\d{1,3}>'"
inp1 = "zcat {}.all.scode.gz"
out1 = "gzip > {}.variance.scode.gz"
inp2 = "zcat {}.all.pairs.100.gz"
out2 = "gzip > {}.variance.pairs.100.gz"


for p in pos:
    inp = inp1.format(p)
    out = out1.format(p)
    process = " | ".join([inp, reg1, out])
    #print process
    os.system(process)
    inp = inp2.format(p)
    out = out2.format(p)
    process = " | ".join([inp, reg2, out])
    os.system(process)

    #print process

