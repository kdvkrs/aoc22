#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

def bbox(elves):
    rmin = min(elves, key=lambda x: x[0])[0]
    rmax = max(elves, key=lambda x: x[0])[0]+1
    cmin = min(elves, key=lambda x: x[1])[1]
    cmax = max(elves, key=lambda x: x[1])[1]+1
    return rmin, rmax, cmin, cmax

def plot(elves):
    if VERBOSE:
        rmin, rmax, cmin, cmax = bbox(elves)
        rmin -= 1
        cmin -= 1
        rmax += 1
        cmax += 1
        plt = [["." for _ in range(cmax-cmin)] for _ in range(rmax-rmin)]
        debug(rmin, rmax, cmin, cmax)
        for er, ec in elves:
            plt[er-rmin][ec-cmin] = "#"
        print("\n".join(["".join(p) for p in plt]))
    


def main():
    l = sys.stdin.read().splitlines()

    elves = set()
    for r, _ in enumerate(l):
        for c, x in enumerate(l[r]):
            if x == "#":
                elves.add((r,c))
    
    def free(pos: list):
        for p in pos:
            if p in elves:
                return False
        return True


    move = set()     
    no_move = set() 
    next = set()

    plot(elves)

    def add(p, op):
        if p in no_move:
            next.add(op)
        elif p in move:
            no_move.add(p)
            move.remove(p)
        else:
            move.add(p)

    # two passes 
    for _ in range(2):
        for er,ec in elves:
            if free([(er-1, ec-1), (er-1, ec), (er-1, ec+1)]):
                add((er-1, ec), (er, ec))
            elif free([(er+1, ec-1), (er+1, ec), (er+1, ec+1)]):
                add((er+1, ec), (er, ec))
            elif free([(er+1, ec-1), (er, ec-1), (er-1, ec-1)]):
                add((er, ec-1), (er, ec))
            elif free([(er+1, ec+1), (er, ec+1), (er-1, ec+1)]):
                add((er, ec+1), (er, ec))

    next = next.union(move)
    elves = next
    debug(next)
    plot(elves)

if __name__ == "__main__":
    main()