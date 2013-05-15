#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import gzip

key = "../test_data/keys/gold/all.key"
data = "test.gz"
sub = "test.sub.gz"


def main():
    keyfile = open(key).readlines()
    data_file = gzip.open(data).readlines()
    sub_file = gzip.open(sub).readlines()

    f = gzip.open("test.gz", 'w')
    g = gzip.open("test.sub.gz", 'w')

    keys = [keyline.split()[1] for keyline in keyfile]
    for i, line in enumerate(data_file):
        dataline = line.split()
        if dataline[0] in keys:
            f.write(line)
            g.write(sub_file[i])
    f.close()
    g.close()

if __name__ == '__main__':
    main()
