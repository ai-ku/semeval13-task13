#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import re
import gzip
import random


test_pairs = gzip.open(sys.argv[1]).read()
seed = int(sys.argv[2])
random.seed(seed)
nsample = int(sys.argv[3])
target_words = sys.argv[4:]
out = 'input-hdp-test/'

files = map(lambda x: open(out + x + '.lemma', 'w'), target_words)
regex = '<{}\.{}>\t(.*)'
limit = 100
docs = gzip.open('pairs.100.gz').read()

# for test instances
for f, t in zip(files, target_words):
    for j in range(1, limit+1): #1 .. 100
        r = regex.format(t, j)
        wordsubs = re.findall(r, test_pairs)
        #with some instids this returns 0 because they were removed from the test set.
        nw = len(wordsubs)
        if nw != 0: 
            if nw != 100: # 100 subs for instance / since pairs.100.gz
                print >> sys.stderr, "Problem: #of subs:{} {}.{}".format(nw, t, j)
            else:
                f.write(' '.join(wordsubs))
                f.write('\n')

print >> sys.stderr, "Sampling started"
#FIXME: Slow: 1000 regex search
# pairs.1000.gz yerine sub.gz kullanilip, 1000 vector secilip, o secilenlerden
# wordsub tekrar calistirilip birlestirme islemi yapilabilir. temp dosyaya
# system(command) ile vs.
regex = '<%s\.\d{4,}>\t.*'
for f, t in zip(files, target_words):
    print >> sys.stderr, "%s processing" % t,
    r = regex % t
    #lines = re.findall('<important.j.\d{4,}>\t.*', docs)
    lines = re.findall(r, docs) 
    ids = set([line.split('\t')[0] for line in lines])
    ids = random.sample(ids, min(nsample, len(ids)))
    print >> sys.stderr, "Sample size:", len(ids)
    ff = '\n'.join(lines)
    for w in ids:
        r = w + '\t(.*)'
        wordsubs = re.findall(r, ff)
        nw = len(wordsubs)
        if nw != 0: 
            if nw != 100: # 100 subs for instance / since pairs.100.gz
                print >> sys.stderr, "Problem: #of subs:{} {}.{}".format(nw, t, j)
            else:
                f.write(' '.join(wordsubs))
                f.write('\n')

map(lambda f: f.close(), files)

