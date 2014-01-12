#!/usr/bin/env python

import sys

new_line = True
for line in sys.stdin:
    line = line.strip().split("\t")
    if line[0] != "</s>":
        if not new_line:
            line[0] = " " + line[0]
        sys.stdout.write(line[0])
        new_line = False
    else:
        sys.stdout.write("\n")
        new_line = True
