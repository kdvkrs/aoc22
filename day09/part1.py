#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

def add(p1,p2): return (p1[0]+p2[0],p1[1]+p2[1])

def sub(p1,p2): return (p1[0]-p2[0],p1[1]-p2[1])

def dsq(p1,p2): return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2

def sgn(x): return x/abs(x) if x else 0

def tupsgn(t): return tuple(sgn(x) for x in t)

MV = {
    "R": (1,0),
    "L": (-1,0),
    "U": (0,1),
    "D": (0,-1)
}

hp = (0,0)
tp = (0,0)

tps = set([tp])

for _, l in enumerate(sys.stdin):
    d, m = l.strip().split()
    debug(d,m)
    debug(hp,MV[d])
    for _ in range(int(m)):
        hp = add(hp,MV[d])
        if dsq(hp,tp) >= 4:
            tp = add(tp, tupsgn(sub(hp,tp)))
            tps.add(tp)

    debug("hp after move:",hp)

print(len(tps))