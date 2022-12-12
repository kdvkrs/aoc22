#!/usr/bin/env python

import sys

score = 0

OP = ['A', 'B', 'C']
RE = ['X', 'Y', 'Z']

def get_score(a,b):
    oi, ri = OP.index(a), RE.index(b)
    offs = ((ri-oi+1) % 3)*3
    return offs+ri+1

for i, l in enumerate(sys.stdin):
    a, b = l.strip().split()
    score += get_score(a,b)

print(score)