#! /usr/bin/python
# -*- coding: utf-8 -*-


__author__ = "Osman Baskaya"

# ../bin/eval.py trial/word/ans 3 
# ../bin/eval.py trial/word/ans 3 5


from utils import get_uniq_field, ColorLogger
import glob
import os
import sys
from itertools import product


#gold_dir = 'trial/word/ungraded_gold/'


logger = ColorLogger('debug')

def merge_ans_files(ans_dir, ids):

    ids = map(int, ids)

    bpath = os.path.dirname(ans_dir)
    goldpath = os.path.join(bpath, "gold")
    nump = len(ids)
    pattern = "*{}" * nump
    pattern = pattern + "*.ans"
    parameters = []
    for p in ids:
        parameters.append(get_uniq_field(ans_dir, p))

    for t in product(*parameters):
        newpat = pattern.format(*t)
        files = glob.glob(ans_dir + '/' + newpat)
        files.sort()
        nlines = []
        for filename in files:
            f = open(filename)
            fn = '.'.join(os.path.basename(filename).split('.')[:2])
            goldfile = os.path.join(goldpath, fn + '.gold')
            logger.debug("{}, {}".format(fn, goldfile))
            glines = open(goldfile).readlines()
            for i, line in enumerate(f.readlines()):
                gold_line = glines[i].split()[:2]
                nlines.append(' '.join(gold_line) + ' ' + line)
        new = open('eval/'+bpath.replace('/', '.')+ '.'+ '.'.join(t) + '.ans','w')
        new.write(''.join(nlines))
        new.close()




def main():
    ans_dir = sys.argv[1]
    ids = sys.argv[2:]
    merge_ans_files(ans_dir, ids)

if __name__ == '__main__':
    main()

