#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import os
from optparse import OptionParser
from utils import get_files, get_uniq_field#, read2sparse
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
parser.add_option("-n", "--nsubs", dest="nsubs", default='12',
                  help="Number of substitition", metavar="NUMBER_OF_SUBS")
#parser.add_option("-k", "--nfactor", dest="nfactor", default=10,
                  #help="number of factor for svd: default 10", metavar="NFACTOR")

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


func_list = ['calc_dists', 'run_wkmeans', 'run_spectral', 'run_wordsub']

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

def _wkmeans(files, input_dir, head_com='', k=None):


    dataset, app_type = input_dir.split('/')[:2]
    path = os.path.join(dataset, app_type, 'ans') + '/'

    if k is None:
        k = [5] * len(files)
    elif isinstance(k, int):
        k = [k] * len(files)
    for i, fulln in enumerate(files):
        fn = fulln.replace(input_dir, '') # weed out the filename
        fn = fn.replace('.gz', '')

        #command = 'cat {} | ../bin/wkmeans -k {} -r 5 -s {} -v'
        if head_com != '':
            command = head_com + ' ../bin/wkmeans -k {} -r 5 -s {} -v > {} '
            command = command.format(fulln, k[i], SEED, path + fn + '.ans')
        else:
            command = 'cat {} | ../bin/wkmeans -k {} -r 5 -s {} -v > {}'
            command = command.format(fulln, k[i], SEED, path + fn + '.ans')
        
        
        
        print >> sys.stderr, fn
        os.system(command)
        
    
def wkmeans():

    """ make trial.word.spectral.wkmeans """

    
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
            k = int(c.replace('c', ''))
            _wkmeans(files, input_dir, k=k)

    elif 'raw' in input_dir:
        input_dir = input_dir + '_knn/'
        distances = get_uniq_field(input_dir, ind=3)
        for d in distances:
            #files = get_files(input_dir, "*" + str(d))
            pattern = input_dir + "*" + str(d)
            files = glob.glob(pattern)
            _wkmeans(files, input_dir)

    elif 'scode' in input_dir:
        head_com = "zcat {} | perl -ne 'print if s/^1://' | cut -f3- | "
        files = [input_dir + '/' + f for f in os.listdir(input_dir)]
        _wkmeans(files, input_dir + '/', head_com=head_com)



def run_wkmeans():
    wkmeans()


def wordsub():
    
    """ Call Example: make trial.word.subs.wordsub

    """

    input_dir = opts.inpath.replace('.', '/') 
    # dataset: trial/test, approach type: word/pos/global, data: raw/iso/svd
    dataset, app_type, data = opts.inpath.split('.')

    nsubs = int(opts.nsubs)

    seed = SEED
    files = os.listdir(input_dir)
    for fname in files:
        fn = '.'.join(fname.split('.')[:2])
        fulln = os.path.join(input_dir, fname)
        outfn = dataset + '/' + app_type + '/wordsubs/' + fn + '.pairs.gz'
        #open(outfn, 'w') # for >> below 
        for i in xrange(nsubs):
            command = """ zcat {} | grep -v '^</s>' | \
                   ../bin/wordsub.py -n {} -u 1 -s {} | gzip > {} """
            #command = """zcat {} | grep -v '^</s>' | ../bin/wordsub.py -s {} | 
                                            #gzip >> {} """
            command = command.format(fulln, nsubs, seed, outfn)
            print >> sys.stderr, command
            os.system(command)

def run_wordsub():
    wordsub()

def scode():


    """ call exp in make: make trial.word.wordsubs.scode.gz""" 

    """ WSC_OPTIONS=-r 1 -i 9 -d 25 -z 0.166 -p 50 -u 0.2 -s ${SEED} -v 
    wordsub.%.scode.gz: wordsub.%.pairs.gz 
        zcat $< | scode ${WSC_OPTIONS} | gzip > $@ """


    #awk_com = ""
    #uniq = True    
    #if uniq:
        #awk_com = """awk 'BEGIN {count=1} {print $1 count "\\t" $2; count=count+1}'"""


    WSC_OPTIONS = "-r 1 -i 9 -d 25 -z 0.166 -p 50 -u 0.2 -s {} -v -a".format(SEED)

    # trial.word.wordsub
    input_dir = opts.inpath.replace('.', '/')

    # dataset: trial/test, approach type: word/pos/global, data: raw/iso/svd
    dataset, app_type, data = opts.inpath.split('.')

    OUT = os.path.join(dataset, app_type) + '/scode/'

    files = os.listdir(input_dir)
    for fname in files:
        fulln = os.path.join(input_dir, fname)
        fn = '.'.join(fname.split('.')[:2])
        #command = "zcat %s | " + awk_com + " | " + "../bin/scode " + WSC_OPTIONS + \
                                                                    #" | gzip > %s"
        command = "zcat %s  | ../bin/scode " + WSC_OPTIONS + " | gzip > %s"
        command = command % (fulln, OUT + fn + '.scode.gz')
        os.system(command)


def run_scode():
    scode()
    

def main():
    input_check()
    func = globals()[opts.func_name]
    func()



if __name__ == '__main__':
    main()
