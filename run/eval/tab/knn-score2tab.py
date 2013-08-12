#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys

# from .scores file
#metrics = {'ji': 2, 'pt': 6, 'ssp': 10, 'wndcg': 14, 'fb': 18, 'fnmi': 22}
metrics = [10, 2, 6, 14, 18, 22]

#from .dist file (topic distribution)
#distr = {'avgs': 52, 'avgsinst': 53, 'avgperp': 54}
distr = [52, 53, 54]


print_arr = []

for fn in sys.stdin: # ls *.scores
    fn = fn.strip()
    exp = fn.replace('.scores', '')
    print >> sys.stderr, fn
    scores = open(fn).readlines()
    if exp.startswith('scode'):
        k, d = exp.replace('scode.knn', '').split('.')
    else:
        k, d = exp.replace('fastsub.knn', '').split('.')
    line = "%s\t%s\t" % (k, d)
    line += "\t".join([scores[m-1].split()[-1] for m in metrics])
    print_arr.append(line)

print_arr.sort(key=lambda x: float(x.split()[0]))
print '\n'.join(print_arr)

