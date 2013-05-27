#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import os
from utils import get_files
import gzip

def convert_ungraded():

    """ This method converts whole data to trial.ungraded.gold 
        ../ung_gold.py > trial.ungraded.gold
    """

    lines = gzip.open('trial.gold.gz').readlines()

    for line in lines:
        line = line.split()
        max_sense_id = ''; max_rating = -1.0
        for sense in line[2:]:
            sense_tup= sense.split('/')
            sense_id, rating = sense_tup[0], float(sense_tup[1])
            if rating > max_rating:
                max_sense_id, max_rating = sense_id, rating
        print ' '.join(line[:2]), max_sense_id



def max_grade(input_dir, out_dir=None):

    if out_dir is None:
        aa = input_dir.split('/')
        out_dir = '/'.join(aa[:2]) + '/ungraded_gold/'

    files = get_files(input_dir, '*')

    for fn in files:
        fname = os.path.join(input_dir, fn)
        if fn.endswith('.gz'):
            f = gzip.open(fname)
        else:
            f = open(fname)

        out_fn = out_dir + fn
        g = gzip.open(out_fn, 'w')
        for line in f.readlines():
            line = line.split()
            max_sense_id = ''; max_rating = -1.0
            for sense in line[2:]:
                sense_tup= sense.split('/')
                sense_id, rating = sense_tup[0], float(sense_tup[1])
                if rating > max_rating:
                    max_sense_id, max_rating = sense_id, rating

            g.write(max_sense_id)
            g.write('\n')
        g.close()


    

def main():
    #input_dir = sys.argv[1]
    #max_grade(input_dir)
    convert_ungraded()

if __name__ == '__main__':
    main()

