#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import os
import fnmatch
from optparse import OptionParser
import shutil
from scipy.sparse import coo_matrix
#from scipy.sparse.linalg import svds
import numpy as np
#from cluster_analysis import calc_perp_from_arr
import gzip

CWD = os.getcwd()


### PATH ###
filepath = os.path.dirname(os.path.realpath(__file__))
idx = filepath.find('src')
PATH = filepath[:idx]
del filepath, idx


### Input Parsing ###
parser = OptionParser()
parser.add_option("-f", "--function", dest="func_name", default=None,
                  help="function you would like to call", metavar="FUNC_NAME")
parser.add_option("-i", "--inpath", dest="inpath", default=None,
                  help="input path", metavar="INPATH")
parser.add_option("-o", "--outpath", dest="outpath", default=None,
                  help="output path", metavar="OUTPATH")
parser.add_option("-r", "--regex", dest="regex", default=None,
                  help="regex for input files", metavar="REGEX")
parser.add_option("-d", "--distances", dest="distances", default='all',
                  help="distance metric(s)", metavar="DISTANCES")
#parser.add_option("-k", "--nfactor", dest="nfactor", default=10,
                  #help="number of factor for svd: default 10", metavar="NFACTOR")
#parser.add_option("-n", "--n_folds", dest="n_folds", default=5,
                  #help="number of folds for classifiers: default 10", metavar="NFOLDS")

(opts, args) = parser.parse_args() 
mandatories = ['func_name', 'inpath', 'regex']


def input_check():
    """ Making sure all mandatory options appeared. """ 
    run = True
    for m in mandatories:
        if not opts.__dict__[m]:
            print "mandatory option is missing: %s" % m
            run = False
    if not run:
        print
        parser.print_help()
        exit(-1)

### Auxiliary functions ###

def get_files(path, regex):
    return [f for f in os.listdir(path) if fnmatch.fnmatch(f, regex)]

def get_goldtag(fname):
    gold_path = PATH + 'run/gold/'
    lines = gzip.open(gold_path + fname).readlines()
    return [line.split()[1] for line in lines]

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

### Important Functions ###


func_list = ['calc_dists',]

def calc_dists():
    """../bin/calcdists.py -f calc_dists -i 
        /home/tyr/playground/task13/run/isolocal -r "*" -d 4 
        2>/home/tyr/calc.err"""
    
    # infile, outfile, d (

    if opts.distances == 'all':
        distances = range(0,5) # make calc for all distances
    else:
        distances = [int(opts.distances)]

    dest = opts.outpath
    
    #check_dest(dest) # prepare destination directory

    files = get_files(opts.inpath, opts.regex)

    for fn in files:
        print >> sys.stderr, fn
        fulln = os.path.join(opts.inpath, fn)
        #command = "cat %s | ../src/scripts/preinput.py > /home/tyr/Desktop/a.rm" \
                        #% (fn)
        for d in distances:
            #command = "..bin/dists -d %d < %s > %s.dist.%d" % (d, fn, fn, d)
            command = "../bin/dists -d %d < %s > %s/%s.dist.%d" % (d, fulln, dest, fn, d)
            print command
            exit()
            os.system(command)


def wkmeans():
    pass

def run_wkmeans():
    pass

def main():
    input_check()
    func = globals()[opts.func_name]
    func()



if __name__ == '__main__':
    main()

