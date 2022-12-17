#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

from part1 import *

def main():
    JP = sys.stdin.read().strip()
    ROCKS = 10**12
    
    by = 3
    B = [["." for _ in range(WIDTH)] for _ in range(by)]
    B.append(["#" for _ in range(WIDTH)])
    
    db_slice(B)

    def db_board(b, r):
        if VERBOSE:
            bd = copy.deepcopy(b)
            bd[r.y:r.y+r.y_span] = merge(b[r.y:r.y+r.y_span], r.slice(), at=True)
            bd[-1] = ["-" for _ in range(WIDTH)]
            bd[-1][0] = "+"
            bd[-1][-1] = "+"
            db_slice(bd)

    PROF = {}
    top = 3 
    i = 0
    ri = 0
    while True:
        debug("====================", "ROCK #", ri, "====================")
        pi = ri%NP

        # potentially append new rows
        while top - PY[pi] < 3:
            B.insert(0, ["." for _ in range(WIDTH)])
            by += 1
            top += 1

        # board profile
        bprof = []
        for x in range(WIDTH):
            for y in range(top, by+1):
                if B[y][x] == "#":
                    bprof.append(y)
                    break
        prof = (tuple(bprof), ri%NP, i)

        debug(prof)
        if prof in PROF:
            cs_ri, cs_h = PROF[prof]
            ri_diff = ri - cs_ri

            # break when we have a cycle that matches total length
            if (ROCKS-cs_ri)%ri_diff == 0:
                break
        else:
            PROF[prof] = (ri, by-top)

        r = Rock(2, top-PY[pi]-3, pi)
        
        db_board(B,r)

        coll = False
        while not coll:
            if JP[i] == ">":
                r.mvx(B,1)
            elif JP[i] == "<":
                r.mvx(B,-1)

            coll = r.d(B)

            i = (i + 1) % len(JP)

        merge_inplace(B[r.y:r.y+r.y_span], r.slice())
        top = min(top, r.y)
        debug("TOP IS", top) 

        ri += 1
    
    h_offs = ((ROCKS-cs_ri)//ri_diff-1)*(by-top - cs_h)
    print(by-top+h_offs)


if __name__ == "__main__":
    main()