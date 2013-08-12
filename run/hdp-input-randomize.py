#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from nlp_utils import fopen
from collections import defaultdict as dd
from random import randint


if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: {} vocab_file".format(sys.argv[0])
    exit(1)

vocab = list(set(fopen(sys.argv[1]).readlines())) # for uniqueness

d = dd(lambda: None)

# random 1
#replacement = False
#for line in sys.stdin:
    #line = line.split()
    #newline = []
    ##if replacement: # process restarts in every new line
        ##d = dd(lambda: None)
    #for word in line:
        #if d[word] is None:
            #r = randint(0, len(vocab) - 1)
            #d[word] = vocab.pop(r).strip()
        #newline.append(d[word])
    #print ' '.join(newline)


# random 2: 
replacement = True
for line in sys.stdin:
    line = line.split()
    newline = []
    if replacement: # process restarts in every new line
        d = dd(lambda: None)
    for word in line:
        if d[word] is None:
            r = randint(0, len(vocab) - 1)
            d[word] = vocab[r].strip()
        newline.append(d[word])
    print ' '.join(newline)


# random 3: everything is random
#for line in sys.stdin:
    #line = line.split()
    #newline = []
    #for word in line:
        #r = randint(0, len(vocab) - 1)
        #word = vocab[r].strip()
        #newline.append(word)
    #print ' '.join(newline)
