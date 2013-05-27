#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import gzip
from utils import get_files
import os

IN = '../data/original/'
OUT = '../data/tokenized/'
REGEX = 'UK*'
TEMPFILE = 'ukwac.temp'


def tokenize(files, field=1):
    """ ukWaC tokenizer """



    for filename in files:
        print "Processing {}".format(filename)

        fn = filename.lower().split('.')
        fn = fn[0] + '.tok.gz'
        
        command = "zcat {} | cut -f{} > {}".format(IN+filename, field, TEMPFILE)
        os.system(command)
        newfile = gzip.open(OUT + fn, 'w')
        with open(TEMPFILE) as f:
            words = []
            for line in f:
                line = line.strip()
                if line.startswith('<text id=') or line == '<s>' or line == '</text>':
                    continue
                elif line == '</s>':
                    words.append('\n')
                    #newfile.write('\n')
                else:
                    words.append(line + ' ')
                    #newfile.write(line + ' ')
            newfile.write(''.join(words))
            newfile.close()
    os.remove(TEMPFILE)

def main():
    files = get_files(IN, REGEX)
    print files
    tokenize(files, 1) #1 for words, 2 for pos, 3 for lemmatization

    

if __name__ == '__main__':
    main()

