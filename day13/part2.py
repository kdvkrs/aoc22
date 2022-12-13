#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

from functools import cmp_to_key

def cmp(l,r):
    if type(l) == int and type(r) == int:
        if l < r:
            return 1
        elif l > r:
            return -1
        else:
            return 0
    elif type(l) == list and type(r) == list: 
        i = 0
        while True:
            if i >= len(l) and i < len(r):
                return 1
            elif i < len(l) and i >= len(r):
                return -1
            elif i >= len(l) and i >= len(r):
                return 0

            c = cmp(l[i], r[i])
            if c != 0:
                return c 
            i += 1

    elif type(l) == list and type(r) == int:
        return cmp(l, [r])
    elif type(l) == int and type(r) == list:
        return cmp([l], r)
    else:
        raise Exception("Unknown types: {} and {}".format(type(l), type(r)))

def main():
    packets = []
    for i, line in enumerate(sys.stdin):
        if i % 3 < 2:
            l = eval(line.strip())
            packets.append(l)
        else:
            pass
            
    d1 = [[2]]
    d2 = [[6]]
    packets.append(d1)
    packets.append(d2)

    packets.sort(key=cmp_to_key(cmp), reverse=True)
    debug("\n".join(map(str,packets)))
    print((packets.index(d1)+1)*(packets.index(d2)+1))

if __name__ == "__main__":
    main()