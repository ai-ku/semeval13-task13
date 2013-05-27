#!/usr/bin/env python

from collections import defaultdict as dd
import gzip
import re
import sys

cluster = {}
for line in gzip.open(sys.argv[1]):
    line = line.strip().split("\t")
    cluster[line[0]] = line[1]

match = re.compile("<(\w+\.\w+)\.([^>]+)>")
sense_counts = dd(lambda: dd(int))
unk_count = 0
for line in sys.stdin:
    line = line.strip().split("\t")
    m = match.search(line[0])
    try:
        sense_counts[m.group(2)][cluster[line[1]]] += 1
    except:
        unk_count += 1
        sense_counts[m.group(2)]["<UNK>"] += 1

# sys.stderr.write("unk: " + str(unk_count) + "\n")
# sys.stderr.write("sense:" + str(len(set((x for c in sense_counts.itervalues() for x in c.iterkeys())))) + "\n")

word = m.group(1)

for instance, counts in sense_counts.iteritems():
    print "%s %s %s" % (word,
                        instance,
                        ' '.join(("%s%s/%d" % (word, x[0], x[1]) for x in counts.iteritems())))
