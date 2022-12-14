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
    while px >= 0 and px < len(grid[0]) and py < len(grid)-1:
        if grid[py+1][px] in ["o", '#']:
            if grid[py+1][px-1] == ".":
                px -= 1
            elif grid[py+1][px+1] == ".":
                px += 1
            else:
                grid[py][px] = 'o'
                return True
        else:
            py += 1 


def main():
    paths = []
    for i, l in enumerate(sys.stdin):
        paths.append(list(map(lambda x: list(map(int,x.split(","))), l.strip().split(" -> "))))
    
    debug(paths)
    x_rng = (min(map(lambda x: min(x, key=lambda y: y[0])[0], paths)), max(map(lambda x: max(x, key=lambda y: y[0])[0], paths)))
    y_rng = (min(map(lambda x: min(x, key=lambda y: y[1])[1], paths)), max(map(lambda x: max(x, key=lambda y: y[1])[1], paths)))
    debug(x_rng, y_rng)

    grid = [["." for _ in range(0, x_rng[1]+100)] for _ in range(0, y_rng[1]+2)]

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

    debug("\n".join(map(lambda x: "".join(x[400:]), grid)))

    i = 0
    while sand(grid):
        i += 1
        debug("\n".join(map(lambda x: "".join(x[400:]), grid)))
    
    print(i)
    

if __name__ == "__main__":
    main()