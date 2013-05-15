#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import gzip
import random

# INPUT = 'small.tok.gz'
INPUT = '../data/tokenized/ukwac.tok.gz'
TOTAL_TOKEN = 1000000
RAND = 0.001
CHUNKSIZE = 10000


def data_split():
    """ ukWaC data split """

    train = gzip.open('train.ukwac.tok.gz', 'w')
    test = gzip.open('test.ukwac.tok.gz', 'w')
    count = 0
    f = gzip.open(INPUT)
    temp_words = []
    temp_test_words = []
    for line in f:
        if random.random() < 0.01 and count < TOTAL_TOKEN:
            temp_test_words.append(line)
            count += len(line.split())
            if len(temp_test_words) > CHUNKSIZE:
                test.write(''.join(temp_test_words))
                temp_test_words = []
        else:
            temp_words.append(line)
            if len(temp_words) > CHUNKSIZE:
                train.write(''.join(temp_words))
                temp_words = []

    train.write(''.join(temp_words))
    test.write(''.join(temp_test_words))


def main():
    data_split()

if __name__ == '__main__':
    main()
