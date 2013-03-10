#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import fnmatch
import os
import shutil
import numpy as np
from scipy.sparse import coo_matrix
import gzip
import sys

# ask.v.knn.3.spectral.c2
# argument.n.knn.2

def get_files(path, regex):
    return [f for f in os.listdir(path) if fnmatch.fnmatch(f, regex)]

def get_uniq_field(path, ind=-1):

    files = os.listdir(path)
    return set([f.split('.')[ind] for f in files])

def get_trial_k(k_file):

    k_lines = gzip.open(k_file).readlines()
    return [int(line.split()[1]) for line in k_lines]


def refresh_temp():
    temp = 'temp'
    if os.path.isdir(temp):
        shutil.rmtree(temp)
    os.mkdir(temp)

def read2sparse(filename, start=1):

    #TODO: Comment ekle ne zaman 1 ne zaman 0 verilmeli
    
    lines = open(filename).readlines()
    col = []
    row = []
    data = []
    for i, line in enumerate(lines):
        line = line.split()
        c = line[1::2]
        col.extend(c)
        row.extend([i] * len(c))
        data.extend(line[2::2])

    data = map(float, data)
    col = map(int, col)
    if start == 1:
        col = map(lambda x: x-1, col) # substract 1 from all indexes
    return coo_matrix((data, (row, col)))


def create_arff(fname, mat, gold):


    """ create files for Weka input format """
    
    gold = [int(g.split('.')[-1]) for g in gold]
    
    g = set(gold)

    gold = np.matrix(gold)
    
    c = np.concatenate((mat.todense(), gold.T), axis=1)

    ncol = mat.shape[1]
    #FIXME: pathi relative yap
    out = "/home/tyr/Desktop/local.weka/" + fname + '.arff'
    f = open(out, 'w')
    f.write("@relation %s\n\n" % fname)
    for i in xrange(ncol):
        f.write("@attribute a%d numeric\n" % i)
    s = ','.join(map(str, g))
    f.write("@attribute class {%s}\n\n" % s)
    f.write("@data\n")
    #FIXME: Avoid writing two times
    np.savetxt(f, c, delimiter=',', fmt='%5f')
    f.close()
    lines = open(out).readlines()
    f = open(out, 'w')
    for line in lines:
        if line[0] != '@' and len(line) != 1:
            line = line.split(',')
            tag = line[-1].strip()
            tag = str(int(float(tag))) + '\n'
            line[-1] = tag
            f.write(','.join(line))
            f.write('\n')
        else:
            f.write(line)
    f.close()


def writedense(filename, mat):

    # matrix should be dense and it forms: [ [], [], ... ] 
    f = open(filename, 'w')
    for row in mat:
        f.write(' '.join(map(str, row)))
        f.write('\n')
    f.close()

def check_dest(dest):
    
    n = dest+"_remove"
    if os.path.isdir(n):
        shutil.rmtree(n)
   
    if os.path.isdir(dest):
        shutil.move(dest, n)
    os.mkdir(dest)


# for debug messages etc.
class ColorLogger(object):
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
    def __init__(self, mode=None):
        if mode is None:
            self.disable()
        self.mode = mode.lower()


    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

    def debug(self, message):
        if self.mode == "debug":
            print >> sys.stderr, self.FAIL, "DEBUG:", message, self.ENDC
        else:
            print >> sys.stderr, message

def main():
    pass

if __name__ == '__main__':
    main()

