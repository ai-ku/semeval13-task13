#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import os
from optparse import OptionParser
from utils import get_files, read2sparse, get_uniq_field
#from scipy.sparse.linalg import svds
#from cluster_analysis import calc_perp_from_arr
# CONSTANTS
from constants import NCPU, SEED, MATLAB_PATH
import gzip
import glob



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


func_list = ['calc_dists', 'run_wkmeans', 'run_spectral']

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


    dest = input_dir.replace(data, data+'_knn/')

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

def spectral():
    """
    %.spectral: %.knn.gz
        ${MATLAB_PATH} < ../bin/runsc.m > $*.spectral 2> $*.spectral.err
        gzip $*.spectral.c*

        # ayni klasorde calisabiliyor o yuzden cd
        ${MATLAB_PATH} -r "runiso fname"> $*.spectral 2> $*.spectral.err
    """
    
    input_dir = opts.inpath.replace('.', '/')
    regex = opts.regex
    # dataset: trial/test, approach type: word/pos/global, data: raw/iso/svd
    dataset, app_type, data = opts.inpath.split('.')

    out_dir = os.path.join(PATH, 'run', input_dir + '_spect')
    full_in_dir = os.path.join(PATH, 'run', input_dir + '_knn')

    os.chdir('../src/spectral/')
    command = '{} -r "runspectral {} {}"'
    command = command.format(MATLAB_PATH, full_in_dir, out_dir)
    print command
    os.system(command)

    # matlab call for each word
    #for fn in files:
        ##print >> sys.stderr, fn
        #fulln = os.path.join(PATH, 'run', input_dir, fn)
        #command = '{} -r "runspectral {} {}"'
        #command = command.format(MATLAB_PATH, fulln, out_dir)
        ##print command
        #os.system(command)


    pass

def run_spectral():
    spectral()

def _wkmeans(files, input_dir, k=None):
    # OUTPUT

    if k is None:
        k = [5] * len(files)

    for i, fulln in enumerate(files):
        fn = fulln.replace(input_dir, '') # weed out the filename
        print >> sys.stderr, fn
        #command = 'cat {} | ../bin/wkmeans -k {} -r 5 -s {} -v'
        command = 'cat {} | ../bin/wkmeans -k {} -r 5 -s {} -v > {}'
        command = command.format(fulln, k[i], SEED, 'ans/' + fn + '.ans')
        os.system(command)
    
def wkmeans():
    """ 
    trial.c%.kmeans.gz: trial.spectral.c%.gz
        zcat $< | ../bin/wkmeans -k $* -r 5 -s ${SEED} -v | gzip > $@
    """
    input_dir = opts.inpath.replace('.', '/') 
    
    # dataset: trial/test, approach type: word/pos/global, data: raw/iso/svd
    dataset, app_type, data = opts.inpath.split('.')

    if 'spect' in input_dir:
        clusters = get_uniq_field(input_dir, ind=-1)
        distances = get_uniq_field(input_dir, ind=3)
        from itertools import product
        for d, c in product(distances, clusters):
            pattern = input_dir + "/*" + d + "*" + c
            files = glob.glob(pattern)
            _wkmeans(files, input_dir)

    else:
        input_dir = input_dir + '_knn'
        distances = get_uniq_field(input_dir, ind=3)

        for d in distances:
            #files = get_files(input_dir, "*" + str(d))
            pattern = input_dir + "*" + str(d)
            files = glob.glob(pattern)
            _wkmeans(files, input_dir)


def run_wkmeans():
    wkmeans()

def main():
    input_check()
    func = globals()[opts.func_name]
    func()



if __name__ == '__main__':
    main()

