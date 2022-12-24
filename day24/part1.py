#!/usr/bin/env pypy3

import sys
import math
from collections import deque
from bisect import insort


def step(b, zz):
    zn = [[[] for _ in l] for l in zz]

    def checkadd(z,r,c,wr,wc):
        if b[r][c] == '#':
            zn[wr][wc].append(z)
        else:
            zn[r][c].append(z)

    for r, zr in enumerate(zz):
        for c, zc in enumerate(zr):
            for z in zc:
                if z == ">": checkadd(z,r,c+1,r,1)
                elif z == "<": checkadd(z,r,c-1,r,-2)
                elif z == "^": checkadd(z,r-1,c,-2,c)
                elif z == "v": checkadd(z,r+1,c,1,c)
    return zn


def main(part=1):
    # b...board z...bliZZard
    b = sys.stdin.read().splitlines()
    z = [[[x] if x in "<>^v" else [] for x in l] for l in b]

    NC = len(b[0])
    NR = len(b)
    NZ = (NR-2)*(NC-2)//math.gcd(NR-2, NC-2) # no lcm in python 3.8, lol
    Z = []
    Z.append(z)
    for _ in range(NZ-1):
        z = step(b,z)
        Z.append(z)

    def bfs(start, end, startmin):
        seen = set() 
        q = deque([(startmin, *start)]) 
        while q:
            m, pr, pc = q.popleft()
            if (pr, pc) == end:
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

    valley_entrance, valley_exit = (0,1), (NR-1, NC-2)
    m1 = bfs(valley_entrance, valley_exit, 0)
    if part == 1:
        print(m1)
    else:
        m2 = bfs(valley_exit, valley_entrance, m1)
        m3 = bfs(valley_entrance, valley_exit, m2)
        print(m3)


if __name__ == "__main__":
    main(part=1)