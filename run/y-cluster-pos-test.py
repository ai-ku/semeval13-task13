#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import os, shutil
import tempfile

if len(sys.argv) < 3:
    print "Usage: {} seed kvals".format(sys.argv[0])
    exit(1)

seed = sys.argv[1]
kvals = sys.argv[2:]


pos = ['adj', 'verb', 'noun']
pairs_base = "zcat {}.pairs.100.gz"

#scode = "../bin/scode -i 50 -a -r 1 -d 25 -z 0.166 -p 50 -u 0.2 -s {} -v ".format(seed)
#scode_out_base = "gzip > {}.scode.pos.gz & \n"

column = "perl -ne 'print if s/^1://'";

kmeans_input_base= "zcat {}.scode.pos.gz"
kmeans_base = "wkmeans -r 128 -l -w -v -s {} -k {}";
kmeans_out_base = "gzip > {}/{}.{}.kmeans.gz & \n"

word_filter = "grep -P '^<\w+\.\w+\.\d+>'"
sense_find = "./pos-find-sense.py {}/{}.{}.kmeans.gz > eval/{}.{}.ans & \n"

path = tempfile.mkdtemp(dir='.')


# SCODE 
#process = ""
#for p in pos:
    #inp = pairs_base.format(p)
    #out = scode_out_base.format(p)
    #process += ' | '.join([inp, scode, out])

#print process + " wait "

process = ""
for k in kvals:
    for p in pos:
        inp = kmeans_input_base.format(p)
        kmeans = kmeans_base.format(seed, k)
        out = kmeans_out_base.format(path, p, k)
        process += ' | '.join([inp, column, kmeans, out])

#print process + " wait "
os.system(process + "wait")


process = ""
for k in kvals:
    for p in pos:
        inp = pairs_base.format(p)
        script = sense_find.format(path, p, k, p, k)
        process += ' | '.join([inp, word_filter, script])

#print process + "wait"
os.system(process + "wait")

for k in kvals:
    for p in pos:
        process = "make eval/{}.{}.scores".format(p, k)
        #print process
        os.system(process)

# remove the temp file and files in it.
shutil.rmtree(path)
