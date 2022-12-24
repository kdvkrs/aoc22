#!/usr/bin/env pypy3

import sys

VERBOSE = "-v" in sys.argv

# ==================================================================== #

import math
from collections import deque
from bisect import insort


def plot(b, z):
    if VERBOSE:
        bb = [[x for x in l] for l in b] 
        for i,r in enumerate(z):
            for j,c in enumerate(r):
                if len(c) == 1:
                    bb[i][j] = c[0]
                elif len(c) > 1:
                    bb[i][j] = str(len(c))
        print("\n".join(["".join(x) for x in bb]))


def step(b, zz):
    zn = [[[] for _ in l] for l in zz]
    for r, zr in enumerate(zz):
        for c, zc in enumerate(zr):
            for z in zc:
                if z == ">":
                    if b[r][c+1] == "#":
                        zn[r][1].append(z)
                    else:
                        zn[r][c+1].append(z)
                elif z == "<":
                    if b[r][c-1] == "#":
                        zn[r][-2].append(z)
                    else:
                        zn[r][c-1].append(z)
                elif z == "^":
                    if b[r-1][c] == "#":
                        zn[-2][c].append(z)
                    else:
                        zn[r-1][c].append(z)
                elif z == "v":
                    if b[r+1][c] == "#":
                        zn[1][c].append(z)
                    else:
                        zn[r+1][c].append(z)
    return zn


def main(part=1):
    lines = sys.stdin.read().splitlines()
    # b...board z...bliZZard
    b = [l.replace(">",".").replace("<",".").replace("v",".").replace("^",".") for l in lines]
    z = [[[x] if x in "<>^v" else [] for x in l] for l in lines]

    NC = len(b[0])
    NR = len(b)
    NZ = (NR-2)*(NC-2)//math.gcd(NR-2, NC-2) # no lcm in python 3.8, lol
    Z = []
    Z.append(z)
    for _ in range(NZ-1):
        z = step(b,z)
        Z.append(z)

    def bfs(start, end, startmin):
        sr, sc = start
        er, ec = end
        seen = set() 
        q = deque([(startmin, sr, sc)]) 
        while q:
            m, pr, pc = q.popleft()
            if (pr, pc) == (er, ec):
                return m
            if (m%NZ, pr, pc) in seen:
                continue
            else:
                seen.add((m%NZ, pr, pc))
            nm = (m+1)%NZ
            nz = Z[nm]
            for offr, offc in [(1,0),(0,1),(0,-1),(-1,0),(0,0)]:
                nr, nc = pr+offr, pc+offc
                if 0 <= nr < NR and 1 <= nc < NC-1 and b[nr][nc] != "#":
                    if (nm, nr, nc) not in seen and not nz[nr][nc]:
                        insort(q, (m+1,nr,nc)) 

    m1 = bfs((0,1), (NR-1, NC-2),0)
    if part == 1:
        print(m1)
    else:
        m2 = bfs((NR-1, NC-2), (0,1), m1)
        m3 = bfs((0,1), (NR-1, NC-2), m2)
        print(m3)


if __name__ == "__main__":
    main(part=1)