#!/usr/bin/env pypy3

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

from collections import deque


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


def main(part=1):
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

    plot(elves)

    stay = set()     
    no_move = set() 
    fe = {}

    def add(p, op):
        if p in fe:
            #debug("clash in pos", p, "op", op)
            no_move.add(p) 
            stay.add(fe[p])
            del fe[p]
        if p not in no_move:
            fe[p] = op
        else:
            stay.add(op)

    def north(e):
        er, ec = e
        if free([(er-1, ec-1), (er-1, ec), (er-1, ec+1)]):
            # debug("move north")
            add((er-1, ec), (er, ec))
            return True
        return False
    
    def south(e):
        er, ec = e
        if free([(er+1, ec-1), (er+1, ec), (er+1, ec+1)]):
            # debug("move south")
            add((er+1, ec), (er, ec))
            return True
        return False

    def west(e):
        er, ec = e
        if free([(er+1, ec-1), (er, ec-1), (er-1, ec-1)]):
            # debug("move west")
            add((er, ec-1), (er, ec))
            return True
        return False
    
    def east(e):
        er, ec = e
        if free([(er+1, ec+1), (er, ec+1), (er-1, ec+1)]):
            # debug("move east")
            add((er, ec+1), (er, ec))
            return True
        return False

    q = deque([north, south, west, east])
    round = 0
    while True:
        round += 1
        stay.clear()
        no_move.clear()
        fe.clear()
        term = True
        for er,ec in elves:
            # debug("ELF", er,ec)
            if free([(er+1, ec+1), (er, ec+1), (er-1, ec+1), (er+1, ec-1), (er, ec-1), (er-1, ec-1), (er-1, ec), (er+1, ec)]):
                stay.add((er,ec))
            else:
                success = False
                for d in q:
                    success = d((er,ec))
                    if success:
                        break
                if not success:
                    stay.add((er,ec))
                term = False
        if term or part==1 and round==11:
            break
        q.rotate(-1)

        elves = set(fe.keys()).union(stay)
        plot(elves)

    brs, bre, bcs, bce = bbox(elves)
    if part==1:
        print((bre-brs)*(bce-bcs)-len(elves))
    else:
        print(round)

if __name__ == "__main__":
    main()