#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

"""
Reads a substitute file and prints word and a random substitute on each line.
-n <number of substitutes per word>
-s <random seed>
-u <if it is 1 then X pairs will be unique> 
e.g:

-u 1 -n 2

add1 a
add1 c
add2 b
add2 d
add3 k
add3 l
..
.

"""

from optparse import OptionParser
import random
import sys
from itertools import count

parser = OptionParser()
parser.add_option("-n", "--numsub", dest="numsub", default=12,
                  help="number of substitution", metavar="NUM_SUB")
parser.add_option("-s", "--seed", dest="seed", default=None,
                  help="Seed value", metavar="SEED")
parser.add_option("-u", "--uniq", dest="isUniq", default=0,
                  help="uniq target words", metavar="UNIQ_TARGET_WORDS")


(opts, args) = parser.parse_args() 

NUBSUB = int(opts.numsub)
if opts.seed is not None:
    random.seed(int(opts.numsub))


isUniq = False
if int(opts.isUniq) != 0:
    isUniq = True
    
c = count(1)


for line in sys.stdin:
    line = line.split()
    target = line[0]
    if target != '</s>':
        totalp = 0
        sample = [''] * NUBSUB
        for i in xrange(1, len(line), 2):
            p = 10 ** float(line[i+1])
            totalp += p
            for j in xrange(NUBSUB):
                if random.uniform(0, totalp) < p:
                    sample[j] = line[i]


    if isUniq:
        t_id = c.next()
        print '\n'.join(map(lambda y: target + str(t_id) + '\t' + y, sample))
    else:
        print '\n'.join(map(lambda y: target + '\t' + y, sample))
        
