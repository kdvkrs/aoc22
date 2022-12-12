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
    for i, l in enumerate(sys.stdin):
        HEIGHTS.append([])
        for j,s in enumerate(l.strip()):
            if s == 'S':
                start = (i,j)
                HEIGHTS[-1].append(0)
            elif s == 'E':
                END = (i,j)
                HEIGHTS[-1].append(ord('z')-ord('a'))
            else:
                HEIGHTS[-1].append(ord(s)-ord('a'))
            
    debug(start, END) 
    debug("\n".join(map(str, HEIGHTS)))
    prev_l = 0
    Q = deque([(start[0], start[1], 0)])
    VIS = set([(start[0], start[1])])
    while Q:
        i,j,l = Q.popleft()
        r = bfs(i,j,l)
        if l > prev_l:
            debug(l, len(Q), len(VIS))
            prev_l = l
        if r is not None:
            break
    print(r)

if __name__ == "__main__":
    main()