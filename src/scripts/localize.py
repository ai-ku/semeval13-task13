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

#PATH = '../../run/'
DATASET = sys.argv[1] # dataset name


def divide_by_pos():
    OUT = DATASET + '/pos/'
    pos = gzip.open(DATASET + '.pos.gz').readlines()
    subs = gzip.open(DATASET + '.sub.gz').readlines()
    if DATASET == 'trial':
        gold = gzip.open(DATASET + '.gold.gz').readlines()

    filename = ""
    f = None
    g = None
    for i, line in enumerate(pos):
        inst = line.strip()
        if filename == inst:
            f.write(subs[i])
            if DATASET == 'trial':
                g.write(gold[i])
        else:
            if f is not None:
                f.close()
                if DATASET == 'trial':
                    g.close()
            filename = inst
            f = open(OUT + 'raw/' + filename, 'a+')
            f.write(subs[i])
            if DATASET == 'trial':
                g = gzip.open(OUT + 'gold/' + filename + '.gold.gz', 'a+')
                g.write(gold[i])


def divide_by_words():

    """ This method divides the dataset into files. For each target word,
        a file will be created in DATASET directory. """
    
    
    OUT = DATASET + '/word/'
    words = gzip.open(DATASET + '.word.gz').readlines()
    subs = gzip.open(DATASET + '.sub.gz').readlines()
    if DATASET == 'trial':
        gold = gzip.open(DATASET + '.gold.gz').readlines()

    filename = ""
    f = None
    g = None
    for i, line in enumerate(words):
        inst = line.strip()
        if filename == inst:
            f.write(subs[i])
            if DATASET == 'trial':
                g.write(gold[i])
        else:
            if f is not None:
                f.close()
                if DATASET == 'trial':
                    g.close()
            filename = inst
            f = open(OUT + 'raw/' + filename, 'a+')
            f.write(subs[i])
            if DATASET == 'trial':
                g = gzip.open(OUT + 'gold/' + filename + '.gold.gz', 'a+')
                g.write(gold[i])

def main():
    #divide_by_words()
    divide_by_pos()



if __name__ == '__main__':
    main()

