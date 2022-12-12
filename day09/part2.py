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

N_KNOTS = 10
K = list(range(N_KNOTS))

P = [(0,0) for _ in K]

tps = set(P[-1])

for _, l in enumerate(sys.stdin):
    d, m = l.strip().split()
    m = int(m)
    debug(d,m)
    debug(P[0],MV[d])
    for _ in range(m):
        P[0] = add(P[0],MV[d])
        for k in range(1,N_KNOTS):
            if dsq(P[k-1],P[k]) >= 4:
                P[k] = add(P[k], tupsgn(sub(P[k-1],P[k])))
                if k == N_KNOTS-1:
                    tps.add(P[k])

    debug("hp after move:",P[0])

print(len(tps))