#!/usr/bin/env python

import sys
from xml.dom import minidom

for f in sys.argv[1:]:
    with open(f) as f:
        xmldoc = minidom.parse(f)
        for instance in xmldoc.getElementsByTagName('instance'):
            text = instance.firstChild.nodeValue
            sys.stdout.write(text + "\n")
