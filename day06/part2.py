#!/usr/bin/env python

import sys
import re


def find_marker(l, ms):
    for i in range(len(l) - ms + 1):
        if len(set(l[i:i+ms])) == ms:
            return i+ms

for ln, l in enumerate(sys.stdin):
    l = l.strip()
    print(find_marker(l, 14))
    