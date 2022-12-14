#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

REST = 0

def sand(grid):
    px, py = 500, 0
    first = True
    while px >= 0 and px < len(grid[0]) and py < len(grid)-1:
        if grid[py+1][px] in ["o", '#']:
            if grid[py+1][px-1] == ".":
                px -= 1
            elif grid[py+1][px+1] == ".":
                px += 1
            else:
                grid[py][px] = 'o'
                return True and not first
        else:
            py += 1 
        first = False


def main():
    paths = []
    for i, l in enumerate(sys.stdin):
        paths.append(list(map(lambda x: list(map(int,x.split(","))), l.strip().split(" -> "))))


    debug(paths)
    x_rng = (min(map(lambda x: min(x, key=lambda y: y[0])[0], paths)), max(map(lambda x: max(x, key=lambda y: y[0])[0], paths)))
    y_rng = (min(map(lambda x: min(x, key=lambda y: y[1])[1], paths)), max(map(lambda x: max(x, key=lambda y: y[1])[1], paths)))
    max_x = x_rng[1]+300
    fl = [[0, y_rng[1]+2], [max_x-1, y_rng[1]+2]]
    paths.append(fl)
    debug(paths)
    debug(fl)

    grid = [["." for _ in range(0, max_x)] for _ in range(0, y_rng[1]+3)]

    for p in paths:
        for i in range(len(p)-1):
            x1, y1 = p[i]
            x2, y2 = p[i+1]
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2)+1):
                    grid[y][x1] = "#"
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2)+1):
                    grid[y1][x] = "#"

    if VERBOSE:
        debug("\n".join(map(lambda x: "".join(x[400:600]), grid)))

    i = 0
    while sand(grid):
        i += 1
        if i % 1000 == 0:
            if VERBOSE:
                debug("\n".join(map(lambda x: "".join(x[400:600]), grid)))
    
    print(i+1)
    

if __name__ == "__main__":
    main()