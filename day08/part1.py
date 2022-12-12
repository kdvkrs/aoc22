#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

tm = []

vis = 0

for i, l in enumerate(sys.stdin):
    tm.append([int(x) for x in l.strip()])

vis = len(tm)*4-4

vis_map = [[0 for x in y] for y in tm]
# print(vis_map)

for i, r in enumerate(vis_map):
    if i == 0 or i == len(vis_map)-1:
        for i in range(len(r)):
            r[i] = 1
    else:
        r[0] = 1
        r[-1] = 1

n = len(tm)
tm_rot = [[tm[j][i] for j in range(len(tm))] for i in range(len(tm[0]))]

debug("\n".join([str(t) for t in tm_rot]))
debug()
debug("\n".join([str(t) for t in tm]))
debug()

for i in range(1,len(vis_map)-1):
    for j in range(1,len(vis_map[i])-1):
        debug(i,j,"tm =", tm[i][j])
        debug("l",tm[i][:j])
        debug("r",tm[i][j+1:])
        debug("u",tm_rot[j][:i])
        debug("d",tm_rot[j][i+1:])
        debug()
        if max(tm[i][:j]) < tm[i][j]:
            vis_map[i][j] = 1
        elif max(tm[i][j+1:]) < tm[i][j]:
            vis_map[i][j] = 1
        elif max(tm_rot[j][:i]) < tm[i][j]:
            vis_map[i][j] = 1
        elif max(tm_rot[j][i+1:]) < tm[i][j]:
            vis_map[i][j] = 1


debug()
debug("\n".join([str(t) for t in vis_map]))
debug()
print(sum([sum(x) for x in vis_map]))
