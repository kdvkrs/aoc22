#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

from itertools import product

SO = [(0.5,0,0), (-0.5,0,0), (0,0.5,0), (0,-0.5,0), (0,0,0.5), (0,0,-0.5)]

def main():
    l = sys.stdin.read().strip().splitlines()
    cubes = [tuple(map(int, x.split(","))) for x in l]
    sides = set()

    rem = set() 
    for x,y,z in cubes:
        for so in SO:
            cso = (x+so[0], y+so[1], z+so[2])
            if cso in sides:
                rem.add(cso)
            else:
                sides.add(cso)
    
    print(len(sides-rem))

if __name__ == "__main__":
    main()