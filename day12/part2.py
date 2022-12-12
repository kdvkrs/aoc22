#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

HEIGHTS = []
from collections import deque
Q = deque()
END = None

VIS = set()

def bfs(i,j,l):
    global VIS
    global Q, END 
    if (i, j) == END:
        return l

    for x, y in [(i,j+1), (i, j-1), (i+1, j), (i-1, j)]:
        if not (x < 0 or y < 0 or x >= len(HEIGHTS) or y >= len(HEIGHTS[0])):
            if HEIGHTS[x][y] <= HEIGHTS[i][j]+1:
                if (x,y) not in VIS:
                    VIS.add((x,y))
                    Q.append((x,y,l+1))

def main():
    global HEIGHTS, END, Q, VIS
    asq = []
    for i, l in enumerate(sys.stdin):
        HEIGHTS.append([])
        for j,s in enumerate(l.strip()):
            if s == 'S':
                HEIGHTS[-1].append(0)
                asq.append((i,j))
            elif s == 'E':
                END = (i,j)
                HEIGHTS[-1].append(ord('z')-ord('a'))
            else:
                if s == 'a':
                    asq.append((i,j))
                HEIGHTS[-1].append(ord(s)-ord('a'))
            
    debug(asq, END) 
    debug("\n".join(map(str, HEIGHTS)))
    prev_l = 0
    asq_dist = []
    for a in asq:
        Q = deque([(a[0], a[1], 0)])
        VIS = set([(a[0], a[1])])
        while Q:
            i,j,l = Q.popleft()
            r = bfs(i,j,l)
            if l > prev_l:
                debug(l, len(Q), len(VIS))
                prev_l = l
            if r is not None:
                break
        asq_dist.append(r)
    debug(asq_dist)
    print(min(filter(lambda x: x is not None, asq_dist)))

if __name__ == "__main__":
    main()