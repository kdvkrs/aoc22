#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv
#VERBOSE = True

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

import re

EXP = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

# actual input:
DIST = 4000000
# sample input:
#DIST = 20 

def dist(x1, y1, x2, y2): return abs(x1-x2) + abs(y1-y2)

def main():
    sensors = []
    for _, l in enumerate(sys.stdin):
        sx, sy, bx, by = map(int, EXP.match(l).groups())
        sd = dist(sx, sy, bx, by)
        sensors.append((sx,sy, sd))

    for y in range(0,DIST):
        x = -1
        while (x := x+1) < DIST: 
            found = True
            for sx, sy, sd in sensors:
                if dist(x,y,sx,sy) <= sd:
                    # skip forward
                    x = sx + sd-abs(sy - y)
                    found = False 
                    break
            if found:
                print(x*4000000+y)
                break


if __name__ == "__main__":
    main()