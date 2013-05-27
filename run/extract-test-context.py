#!/usr/bin/env python

import sys
from xml.dom import minidom

for f in sys.argv[1:]:
    with open(f) as f:
        xmldoc = minidom.parse(f)
        for instance in xmldoc.getElementsByTagName('instance'):
            name  = '<' + instance.attributes['id'].value + '>'
            text  = instance.firstChild.nodeValue
            start = int(instance.attributes['tokenStart'].value)
            end   = int(instance.attributes['tokenEnd'].value)
            left  = ' '.join(text[:start].split()[-3:])
            sys.stdout.write(left + ' ' + name + "\n")
            right = ' '.join(text[end:].split()[:3])
            sys.stdout.write(name + ' ' + right + "\n")
