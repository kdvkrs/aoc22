#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

import re

EXP = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

# actual input:
Q_Y = 2000000
# sample input:
# Q_Y = 10

def dist(x1, y1, x2, y2): return abs(x1-x2) + abs(y1-y2)

def main():
    sensors = []
    beacons = set()
    for _, l in enumerate(sys.stdin):
        sx, sy, bx, by = map(int, EXP.match(l).groups())
        sd = dist(sx, sy, bx, by)
        sensors.append((sx,sy, sd))
        beacons.add((bx,by))

    occ_tiles = set()
    for sx, sy, sd in sensors:
        cdiff = sd-abs(sy-Q_Y)
        if cdiff > 0:
            for x in range(sx-cdiff, sx+cdiff+1):
                occ_tiles.add((x, Q_Y))
    
    occ_tiles -= beacons

    print(len(list(filter(lambda x: x[1] == Q_Y, occ_tiles))))


if __name__ == "__main__":
    main()