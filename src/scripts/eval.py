#! /usr/bin/python
# -*- coding: utf-8 -*-


__author__ = "Osman Baskaya"

# ../bin/eval.py trial/word/ans 3 
# ../bin/eval.py trial/word/ans 3 5


from utils import get_uniq_field
import glob
import os
import sys
from itertools import product


#gold_dir = 'trial/word/ungraded_gold/'



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

    counter = 0 
    for t in product(*parameters):
        pattern = pattern.format(*t)
        files = glob.glob(ans_dir + '/' + pattern)
        nlines = []
        for filename in files:
            f = open(filename)
            fn = '.'.join(os.path.basename(filename).split('.')[:2])
            goldfile = os.path.join(goldpath, fn + '.gold')
            print >> sys.stderr, fn, goldfile
            glines = open(goldfile).readlines()
            for i, line in enumerate(f.readlines()):
                gold_line = glines[i].split()[:2]
                nlines.append(' '.join(gold_line) + ' ' + line)
        new = open('eval/'+bpath.replace('/', '.')+ '.'+ '.'.join(t) + '.ans','w')
        counter += 1
        new.write(''.join(nlines))
        new.close()



#def spect_score_eval():
    
    #input_dir = 'ans/'
    #clusters = get_uniq_field(input_dir, ind=5)
    #distances = get_uniq_field(input_dir, ind=3)
    #from itertools import product
    #for d, c in product(distances, clusters):
        #os.chdir(input_dir)
        #pattern = "*" + d + "*" + c + '.ans'
        #files = glob.glob(pattern)
        #print d, c
        #os.chdir('../')
        #for fname in files:
            #ff = fname.split('.')
            #word = '.'.join(ff[:2])
            #command = "../bin/eval.pl < {} -v -g {}"
            #command = command.format('ans/'+fname, gold_dir+word+'.gold.gz')
            #os.system(command)

#def score_eval():
    #input_dir = 'ans1/'
    #distances = sorted(get_uniq_field(input_dir, ind=3))
    #for d in distances:
        #os.chdir(input_dir)
        #pattern = "*" + d + '.ans'
        #files = glob.glob(pattern)
        #print d
        #os.chdir('../')
        #for fname in files:
            #ff = fname.split('.')
            #word = '.'.join(ff[:2])
            #command = "../bin/eval.pl < {} -v -g {}"
            #command = command.format(input_dir+fname, gold_dir+word+'.gold.gz')
            #os.system(command)



def main():
    #spect_score_eval()
    #score_eval()

    ans_dir = sys.argv[1]
    ids = sys.argv[2:]
    merge_ans_files(ans_dir, ids)

if __name__ == '__main__':
    main()

