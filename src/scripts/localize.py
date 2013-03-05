#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


""" Two type of localization:

    1- By POS tags
    2- By Words

"""


import gzip
import os
import fnmatch
import sys
from collections import defaultdict

#PATH = '../../run/'
DATASET = sys.argv[1] # dataset name


def divide_by_pos():
    OUT = DATASET + '/pos/'
    pos = gzip.open(DATASET + '.pos.gz').readlines()
    subs = gzip.open(DATASET + '.sub.gz').readlines()
    if DATASET == 'trial':
        gold = gzip.open(DATASET + '.gold.gz').readlines()
    
    
    
    posd = defaultdict(list)
    goldd = defaultdict(list)

    for i, line in enumerate(pos):
        inst = line.strip()
        posd[inst].append(subs[i])
        if DATASET == 'trial':
            goldd[inst].append(gold[i])


    for inst in posd.keys():
        f = open(OUT + 'raw/' + inst, 'w')
        f.write(''.join(posd[inst]))
        f.close()
        if DATASET == 'trial':
            f = open(OUT + 'gold/' + inst + '.gold', 'w')
            f.write(''.join(goldd[inst]))
            f.close()


def divide_by_words():

    """ This method divides the dataset into files. For each target word,
        a file will be created in DATASET directory. """
    
    
    OUT = DATASET + '/word/'
    words = gzip.open(DATASET + '.word.gz').readlines()
    subs = gzip.open(DATASET + '.sub.gz').readlines()
    if DATASET == 'trial':
        gold = gzip.open(DATASET + '.gold.gz').readlines()

    wordd = defaultdict(list)
    goldd = defaultdict(list)

    for i, line in enumerate(words):
        inst = line.strip()
        wordd[inst].append(subs[i])
        if DATASET == 'trial':
            goldd[inst].append(gold[i])


    for inst in wordd.keys():
        f = open(OUT + 'raw/' + inst, 'w')
        f.write(''.join(wordd[inst]))
        f.close()
        if DATASET == 'trial':
            f = open(OUT + 'gold/' + inst + '.gold', 'w')
            f.write(''.join(goldd[inst]))
            f.close()


def main():
    divide_by_words()
    divide_by_pos()



if __name__ == '__main__':
    main()

