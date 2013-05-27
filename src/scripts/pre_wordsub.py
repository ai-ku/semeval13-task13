#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import gzip
from collections import defaultdict

fastsub_file = sys.argv[1]
DATASET = fastsub_file.split('.')[0] 
OUT_PATH = DATASET + '/%s/subs/' % sys.argv[3]
targetword_file = sys.argv[2]
wordfile = DATASET + '.word.gz'



def pre_wordsub():
    """call_exp: trial.word.prewordsub.gz """   

    wlines = gzip.open(wordfile).readlines()
    fastd = defaultdict(list)
    with gzip.open(fastsub_file) as f, gzip.open(targetword_file) as t:
        fast_lines = f.readlines()
        for i, line in enumerate(t.readlines()):
            ll = fast_lines[i].replace('__XX__', line.strip()).strip()
            print ll
            key = wlines[i].strip()
            fastd[key].append(ll)

    for word in fastd.keys():
        f = gzip.open(OUT_PATH + word + '.sub.gz', 'w')
        f.write('\n'.join(fastd[word]))
        f.close()

def main():
    pre_wordsub()

if __name__ == '__main__':
    main()

