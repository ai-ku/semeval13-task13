#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys

# from .scores file
#metrics = {'ji': 2, 'pt': 6, 'ssp': 10, 'wndcg': 14, 'fb': 18, 'fnmi': 22}
metrics = [2, 6, 10, 14, 18, 22]

#from .dist file (topic distribution)
#distr = {'avgs': 52, 'avgsinst': 53, 'avgperp': 54}
distr = [52, 53, 54]

hdp_files = map(lambda x: open("hdp_%s.tab" % x, 'w'), "alpha gamma".split())
fastsub_file = open("fastsub_knn.tab", 'w')
scode_file = open("scode_knn.tab", 'w')

for fn in sys.stdin: # ls *.scores
    fn = fn.strip()
    exp = fn.replace('.scores', '')
    print >> sys.stderr, fn
    scores = open(fn).readlines()
    if exp.startswith('hdp'):
        stats = open(exp + '.dist').readlines()
        param, val =  exp.split('-')[1:]
        if param == 'alpha':
            f = hdp_files[0]
        elif param == 'gamma':
            f = hdp_files[1]
        line = "%s\t" % val
        line += "\t".join([scores[m-1].split()[-1] for m in metrics])
        line += '\t'
        line += "\t".join([stats[s-1].split()[-1] for s in distr])
        f.write(line)
        f.write('\n')
    elif exp.startswith('scode') or exp.startswith('fastsub'):
        if exp.startswith('scode'):
            f = scode_file
            k, d = exp.replace('scode.knn', '').split('.')
        else:
            f = fastsub_file
            k, d = exp.replace('fastsub.knn', '').split('.')
        line = "%s\t%s\t" % (k, d)
        line += "\t".join([scores[m-1].split()[-1] for m in metrics])
        f.write(line)
        f.write('\n')


