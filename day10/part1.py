#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


PROBE = [20,60,100,140,180,220]

X = 1
C = 1
Q = []

def addx_del(*args):
    global Q,C,C
    debug("Executing dispatch_addx with args", args, "and X =", X)
    C += 1
    Q.insert(0,(addx, args[0]))

def addx(*args):
    global X,C,Q
    debug("Executing addx with args", args, "and X =", X)
    X += args[0]["x"]
    C += 1

def noop(*args):
    debug("Executing noop")
    global C
    C += 1
    pass


ss = []

for i, l in enumerate(sys.stdin):
    debug(f"Cycle {i+1}", "X =", X)
    #debug("Queue:", q)

    cmd = l.strip().split()

    if cmd[0] == "noop":
        #debug("CMD: noop")
        Q.append((noop, {}))
    elif cmd[0] == "addx":
        #debug("CMD: addx")
        Q.append((addx_del, {"x": int(cmd[1])}))

    # exec
    while Q:
        fn, args = Q.pop(0)
        fn(args)
        if C in PROBE:
            ss.append((X,C))

debug(ss)
print(sum(map(lambda x: x[0]*x[1], ss)))