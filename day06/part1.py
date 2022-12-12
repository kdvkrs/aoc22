#!/usr/bin/env python

import sys
import re

MARKER_SIZE = 4

def find_marker(l):
    for i in range(len(l) - MARKER_SIZE + 1):
        if len(set(l[i:i+MARKER_SIZE])) == MARKER_SIZE:
            return i+MARKER_SIZE

for ln, l in enumerate(sys.stdin):
    l = l.strip()
    print(find_marker(l))

    