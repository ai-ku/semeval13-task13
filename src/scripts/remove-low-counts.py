#!/usr/bin/env python

import sys

limit = int(sys.argv[1])

for line in sys.stdin:
    line = line.split()
    out = [line[0], line[1]]
    for sense in line[2:]:
        count = int(sense.split('/')[1])
        if count > limit:
            out.append(sense)
    print ' '.join(out)
