#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import os
from optparse import OptionParser
from utils import get_files, read2sparse
#from scipy.sparse.linalg import svds
#from cluster_analysis import calc_perp_from_arr
# CONSTANTS
from constants import NCPU
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
parser.add_option("-l", "--langmodel", dest="lm", default='ukwac.lm.gz',
                  help="language model", metavar="LANGUAGE_MODEL")
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

def get_goldtag(fname):
    gold_path = PATH + 'run/gold/'
    lines = gzip.open(gold_path + fname).readlines()
    return [line.split()[1] for line in lines]


### Important Functions ###


func_list = ['calc_dists',]

def calc_dists():

    """../bin/calcdists.py -f calc_dists -i 
        /home/tyr/playground/task13/run/isolocal -r "*" -d 4 
        2>/home/tyr/calc.err"""
    
    # infile, outfile, d 

    if opts.distances == 'all':
        distances = range(0,5) # make calc for all distances
    else:
        distances = [int(opts.distances)]

    
    #check_dest(dest) # prepare destination directory

    input_dir = opts.inpath.replace('.', '/')
    
    # dataset: trial/test, approach type: word/pos/global, data: raw/iso/svd
    dataset, app_type, data = opts.inpath.split('.')
    files = get_files(input_dir, opts.regex)


    dest = input_dir.replace(data, data+'_dist/')

    for fn in files:
        print >> sys.stderr, fn
        fulln = os.path.join(input_dir, fn)
        #command = "cat %s | ../src/scripts/preinput.py > /home/tyr/Desktop/a.rm" \
                        #% (fn)
        for d in distances:
            command = 'cat %s | ../bin/preinput.py | ../bin/dists -d %d -p %d > %s'
            command = command % (fulln, d, NCPU, dest + fn + '.knn.' + str(d))
            print command
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

