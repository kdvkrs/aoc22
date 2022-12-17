#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

from functools import lru_cache
import copy

WIDTH = 7

PATTERNS = [
    ["####"],
    [".#.", "###", ".#."],
    ["..#", "..#", "###"],
    ["#", "#", "#", '#'],
    ["##", "##"]
]

NP = len(PATTERNS)

PY = [len(p) for p in PATTERNS]
PX = [len(p[0]) for p in PATTERNS]

@lru_cache(maxsize=None)
def slice(pi, x):
    p = PATTERNS[pi]
    s = [["." for _ in range(WIDTH)] for _ in range(PY[pi])]
    for y in range(PY[pi]):
        for xx in range(x, x+PX[pi]):
            if p[y][xx-x] == "#":
                s[y][xx] = "#"
    return s

class Rock:
    def __init__(self, x, y, p):
        self.x = x
        self.y = y
        self.pat = p
        self.x_span = PX[p]
        self.y_span = PY[p]
    
    def mvx(self, b, dx):
        if 0 <= self.x + dx and self.x + dx + self.x_span <= WIDTH:
            self.x += dx
            if self.collides(b):
                self.x -= dx

    def d(self, b):
        if self.y < len(b):
            self.y += 1
            if self.collides(b):
                self.y -= 1
                return True
            return False
        else:
            return True
    
    def slice(self):
        return slice(self.pat, self.x)
    
    def collides(self, b):
        s = self.slice()
        bs = b[self.y:self.y+self.y_span]
        for y in range(len(s)):
            for x in range(len(s[y])):
                if s[y][x] == "#":
                    if bs[y][x] == "#":
                        return True
        return False


def db_slice(s):
    if VERBOSE:
        print("\n".join(map(lambda x: "".join(x), s)))


def merge_inplace(s1,s2, at=False):
    for y in range(len(s2)):
        for x in range(len(s2[y])):
            if s2[y][x] == "#":
                if s1[y][x] == "#":
                    # overlap (debug)
                    s1[y][x] == "X"
                if at:
                    s1[y][x] = "@"
                else:
                    s1[y][x] = "#"


def merge(s1, s2, at=False):
    s = copy.deepcopy(s1)
    merge_inplace(s,s2,at)
    return s


def main():
    JP = sys.stdin.read().strip()
    ROCKS = 2022
    
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
    for ri in range(ROCKS):
        debug("====================", "ROCK #", ri, "====================")
        pi = ri%NP

        # potentially append new rows
        while top - PY[pi] < 3:
            B.insert(0, ["." for _ in range(WIDTH)])
            by += 1
            top += 1

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

    print(by-top) 


if __name__ == "__main__":
    main()