#!/usr/bin/env python

import gzip
from itertools import count, izip
import re
import sys

lemma_pos = {}
lemma_count = {}
lemma_set = set()
for arg in sys.argv[4:]:
    match = re.search("(\w+)\.(\w+)\.xml$", arg)
    lemma_pos[match.group(1)] =  match.group(2).upper()
    lemma_count[match.group(1)] =  count(1000)
    lemma_set.add(match.group(1))

f_tok = gzip.open(sys.argv[1])
f_pos = gzip.open(sys.argv[2])
f_lem = gzip.open(sys.argv[3])

for l_tok, l_pos, l_lem, line in izip(f_tok, f_pos, f_lem, count(1)):
    l_tok = l_tok.split()
    l_pos = l_pos.split()
    l_lem = l_lem.split()
    if not (len(l_tok) == len(l_pos) == len(l_lem)):
        sys.stderr.write(str(line) + ': ' + ' '.join(l_tok) + "\n")
        sys.stderr.write(str(line) + ': ' + ' '.join(l_pos) + "\n")
        sys.stderr.write(str(line) + ': ' + ' '.join(l_lem) + "\n")
        continue
    for i in xrange(len(l_lem)):
        if l_lem[i] in lemma_set and l_pos[i].startswith(lemma_pos[l_lem[i]]):
            print "%s <%s.%s.%d> %s" % (' '.join(l_tok[i - 3:i]),
                                        l_lem[i],
                                        l_pos[i][0].lower(),
                                        lemma_count[l_lem[i]].next(),
                                        ' '.join(l_tok[i + 1:i + 4]))
