#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import re
import gzip
from itertools import cycle
import random


pairs = gzip.open(sys.argv[1]).read()
seed = int(sys.argv[2])
random.seed(seed)
nsample = int(sys.argv[3])
target_words = sys.argv[4:]
out = 'hdp_input_test/'

files = map(lambda x: open(out + x + '.lemma', 'w'), target_words)
regex = '<{}\.{}>\t(.*)'
limit = 100
inst_id = cycle(range(1, limit + 1))


# for test instances
for f, t in zip(files, target_words):
    for j in range(1, limit+1):
        r = regex.format(t, j)
        wordsubs = re.findall(r, pairs)
        if len(wordsubs) == 0:
            break
        if len(wordsubs) != 100 and len(wordsubs) != 0:
            print >> sys.stderr, "Problem: #of subs:{} {}.{}".format(len(wordsubs), t, j)
        f.write(' '.join(wordsubs))
        f.write('\n')

print >> sys.stderr, "Sampling started"
regex = '<%s\.\d{4,}>\t.*'
docs = gzip.open('pairs.100.gz').read()
#docs = gzip.open('noksan.pairs.100.gz').read()
#docs = gzip.open('dummy.gz').read()
for f, t in zip(files, target_words):
    print >> sys.stderr, "%s processing" % t,
    r = regex % t
    #lines = re.findall('<important.j.\d{4,}>\t.*', docs)
    lines = re.findall(r, docs)
    ids = [line.split('\t')[0] for line in lines]
    ids = random.sample(ids, min(nsample, len(ids)))
    print >> sys.stderr, "Sample size:", len(ids)
    ff = '\n'.join(lines)
    for w in ids:
        r = w + '\t(.*)'
        wordsubs = re.findall(r, ff)
        if len(wordsubs) == 0:
            break
        if len(wordsubs) != 100 and len(wordsubs) != 0:
            print >> sys.stderr, "Problem: #of subs:{} {}.{}".format(len(wordsubs), t, w)
        f.write(' '.join(wordsubs))
        f.write('\n')



map(lambda f: f.close(), files)





#files = [1,2,3]
#regex = '^<%s\.\d{4,}>'
#docs = gzip.open('dummy.gz')
#words_files = dict(zip(target_words, files))
#words_count = dd(int)

#for line in docs:
    #line = line.split()
    #wid = line[0]






