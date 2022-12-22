#!/usr/bin/env python3

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #
import re

EXP = re.compile(r"([LR])(\d+)")
EC = "-"

def main():
    l = sys.stdin.read().splitlines()
    ins_str = "R"+l[-1]
    l = l[:-2]
    ml = len(max(l, key=len))
    b = [x.ljust(ml," ").replace(" ", EC) for x in l] 

    # instruction parsing
    ins = [(dr, int(di)) for dr, di in EXP.findall(ins_str)]

    # board start/end for each row
    bs = [min(l.find("."), l.find("#")) if "#" in l else l.find(".") for l in b]
    be = list(map(lambda x: x if x != -1 else ml, [l.find(EC, s) for l,s in zip(b, bs)]))

    def next(y,x,dir):
        py,px = y,x
        assert b[py][px] == '.'
        if dir == 0:
            # right
            px += 1
            if px >= be[py]:
                px = bs[py]
        elif dir == 2:
            # left
            px -= 1
            if px < bs[py]:
                px = be[py]-1
        elif dir == 3:
            # up
            py = (py - 1) % len(b)
            while not bs[py] <= px < be[py]:
                py = (py - 1) % len(b)
        elif dir == 1:
            # down
            py = (py + 1) % len(b)
            while not bs[py] <= px < be[py]:
                py = (py + 1) % len(b)
        return (py,px)
    
    y = 0 
    x = bs[y]
    dir = 3
    for rot, dis in ins:
        dir = (dir + (1 if rot == "R" else -1)) % 4
        for _ in range(dis):
            py, px = next(y, x, dir)
            if b[py][px] == "#":
                break
            else:
                y, x = py, px
        debug(y,x)
    print(1000*(y+1)+(x+1)*4+dir)


if __name__ == "__main__":
    main()