#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys

""" During evaluation, organizers decided to remove some instances and they have not
provided new test data (they only gave clean key files) so in order to correspond test 
dataand the key files we need to remove the same instances that are removed. """

#old_data = 4806
new_data = 4664

key_file = sys.argv[1]

s = set()
# create instance set
for line in open(key_file).readlines():
    instance_id = line.split()[1]
    s.add(instance_id)

assert len(s) == new_data, "Does not match: {} with key file length".format(len(s))

counts = [0, 0]
for line in sys.stdin:
    inst = line.split()[0][1:-1]
    if inst in s:
        print line
        counts[0] += 1
    else:
        print >> sys.stderr, "{} removed".format(inst)
        counts[1] += 1

assert counts[0] == new_data
