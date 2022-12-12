#!/usr/bin/env python

import sys
import functools

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
sm = [[-1 for x in y] for y in tm]
max_score = 0
max_score_views = []

for i in range(len(vis_map)):
    for j in range(len(vis_map[i])):
        v = tm[i][j]
        l = tm[i][:j][::-1]
        r = tm[i][j+1:]
        u  = tm_rot[j][:i][::-1]
        d = tm_rot[j][i+1:]
        s = 1
        scores = []
        for d in [l,r,u,d]:
            ti = 0
            for t in d:
                ti += 1
                if t >= v:
                    break
            scores.append(ti)
        debug(i,j,"tm =", tm[i][j])
        debug(f"{l=}")
        debug(f"{r=}")
        debug(f"{u=}")
        debug(f"{d=}")
        debug(i,j,v,scores)
        debug()
        sm[i][j] = functools.reduce(lambda x,y: x*y, scores,1)
        if sm[i][j] > max_score:
            max_score_views = ((i,j), scores)
            max_score = sm[i][j]

debug(max_score_views)
debug("\n".join([str(t) for t in sm]))
print(max_score)
