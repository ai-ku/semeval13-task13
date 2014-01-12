#!/usr/bin/env python

from collections import defaultdict as dd
from random import randint
import re
import sys

k = int(sys.argv[1])

match_re = re.compile("<(\w+\.\w)")
selections = dd(lambda: ([], [-1]))

for line in sys.stdin:
    key = match_re.search(line).group(1)
    l, n = selections[key]
    n[0] += 1
    if len(l) < k:
        l.append(line)
    else:
        r = randint(0, n[0])
        if r < k:
            l[r] = line

for value in selections.itervalues():
    l, n = value
    for line in l:
        sys.stdout.write(line)
