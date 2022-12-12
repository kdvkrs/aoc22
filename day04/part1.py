#!/usr/bin/env python

import sys

count = 0

def rc(r1, r2):
    r1s, r1e = r1
    r2s, r2e = r2
    return ((r1s <= r2s and r1e >= r2e) or (r2s <= r1s and r2e >= r1e))

def ro(r1, r2):
    r1s, r1e = r1
    r2s, r2e = r2
    # return if ranges overlap
    return (r1s <= r2s and r1e >= r2s) or (r2s <= r1s and r2e >= r1s)


for i, l in enumerate(sys.stdin):
    a,b = [x.split("-") for x in l.strip().split(",")]
    r1 = (int(a[0]),int(a[1]))
    r2 = (int(b[0]),int(b[1]))
    if rc(r1,r2):
        count += 1
    
print(count)
