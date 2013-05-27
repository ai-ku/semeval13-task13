#!/usr/bin/env python

import re
import sys

add = int(sys.argv[1])

for line in sys.stdin:
    line = line.split()
    for i in xrange(2, len(line)):
        m = re.search("^([^/]+/)([^/]+)$", line[i])
        line[i] = m.group(1) + str(int(m.group(2)) + add)
    print ' '.join(line)
