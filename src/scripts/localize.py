#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


""" Two type of localization:

    1- By POS tags
    2- By Words

"""

import gzip
import sys
from collections import defaultdict

#PATH = '../../run/'
DATASET = sys.argv[1] # dataset name

subs = gzip.open(DATASET + '.sub.gz').readlines()
target = gzip.open(DATASET + '.target.gz').readlines()
gold = gzip.open(DATASET + '.gold.gz').readlines()


def divide_by_pos():
    OUT = DATASET + '/pos/'
    pos = gzip.open(DATASET + '.pos.gz').readlines()
    
    posd = defaultdict(list)
    goldd = defaultdict(list)
    presub = defaultdict(list)

    for i, line in enumerate(pos):
        inst = line.strip()
        posd[inst].append(subs[i])
        goldd[inst].append(gold[i])
        line = subs[i].replace('__XX__', target[i].strip())
        presub[inst].append(line)


    g = gzip.open(DATASET + '.pos.k.gz', 'w')
    for inst in posd.keys():
        n = len(set([line.split()[-1] for line in goldd[inst]]))
        g.write("{}\t{}\n".format(inst, n))
        h = gzip.open(OUT + 'subs/' + inst, 'w')
        h.write(''.join(presub[inst]))
        h.close()

        f = open(OUT + 'raw/' + inst, 'w')
        f.write(''.join(posd[inst]))
        f.close()

        f = open(OUT + 'gold/' + inst + '.gold', 'w')
        f.write(''.join(goldd[inst]))
        f.close()

    g.close()


def divide_by_words():

    """ This method divides the dataset into files. For each target word,
        a file will be created in DATASET directory. """
    
    
    OUT = DATASET + '/word/'
    words = gzip.open(DATASET + '.word.gz').readlines()

    wordd = defaultdict(list)
    goldd = defaultdict(list)
    presub = defaultdict(list)

    for i, line in enumerate(words):
        inst = line.strip()
        wordd[inst].append(subs[i])
        goldd[inst].append(gold[i])
        line = subs[i].replace('__XX__', target[i].strip())
        presub[inst].append(line)


    g = gzip.open(DATASET + '.word.k.gz', 'w')
    for inst in wordd.keys():
        n = len(set([line.split()[-1] for line in goldd[inst]]))
        g.write("{}\t{}\n".format(inst, n))

        h = gzip.open(OUT + 'subs/' + inst, 'w')
        h.write(''.join(presub[inst]))
        h.close()

        f = open(OUT + 'raw/' + inst, 'w')
        f.write(''.join(wordd[inst]))
        f.close()
        f = open(OUT + 'gold/' + inst + '.gold', 'w')
        f.write(''.join(goldd[inst]))
        f.close()
    g.close()


def main():
    divide_by_words()
    divide_by_pos()



if __name__ == '__main__':
    main()

