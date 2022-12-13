#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

def cmp(l,r):
    debug("Compare", l, r)
    if type(l) == int and type(r) == int:
        if l < r:
            return True
        elif l > r:
            return False
        else:
            return None
    elif type(l) == list and type(r) == list: 
        i = 0
        while True:
            if i >= len(l) and i < len(r):
                return True
            elif i < len(l) and i >= len(r):
                return False
            elif i >= len(l) and i >= len(r):
                return None

            c = cmp(l[i], r[i])
            if c is not None:
                return c 
            i += 1

    elif type(l) == list and type(r) == int:
        return cmp(l, [r])
    elif type(l) == int and type(r) == list:
        return cmp([l], r)
    else:
        raise Exception("Unknown types: {} and {}".format(type(l), type(r)))


def main():
    index = 0
    true_idx = []
    for i, line in enumerate(sys.stdin):
        if i % 3 == 0:
            l = eval(line.strip())
        elif i % 3 == 1:
            r = eval(line.strip())
        else:
            index += 1
            debug("COMPARE",l,r)
            c = cmp(l,r)
            debug("COMPARE (index {}) YIELDED".format(index), c)
            if c is True:
                true_idx.append(index)

    debug(true_idx)
    print(sum(true_idx))

if __name__ == "__main__":
    main()