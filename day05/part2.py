#!/usr/bin/env python

import sys
import re

INST = re.compile(r"move (\d+) from (\d+) to (\d+)")

first = True
for ln, l in enumerate(sys.stdin):
    if first:
        N = len(l)//4
        stacks = [[] for _ in range(N)]
        first = False
    m = INST.match(l)
    if m is None:
        if not (l.strip() == "" or l[1] == '1'):
            s = 0
            for i in range(1,N*3+(N-1),4):
                if l[i] != ' ':
                    stacks[s].append(l[i])
                s += 1
    else:
        n, f, t = m.groups()
        n = int(n)
        f = int(f)-1
        t = int(t)-1
        for i in range(n):
            stacks[t].insert(i, stacks[f].pop(0))


print("".join([x[0] if len(x) > 0 else " " for x in stacks]))
    
    
