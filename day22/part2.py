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

def main(part=2):
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

    SAMPLE = ml % 50 != 0

    if SAMPLE:
        FACELEN = 4
    else:
        FACELEN = 50

    faces = []
    fc = 0
    faceoffs = {}
    for y in range(0,len(b)//FACELEN):
        fr = []
        for x in range(0, ml//FACELEN):
            if b[y*FACELEN][x*FACELEN] != EC:
                fc += 1
                fr.append(fc)
                faceoffs[fc] = (y*FACELEN,x*FACELEN)
            else:
                fr.append(0)
        faces.append(fr)
    
    # face adjacencies
    adj = {c: [None,None,None,None] for c in range(1,fc+1)}
    
    if part == 1:
        def scanx(yy, start, right=True):
            fml = len(faces[0])
            for x in range(1,fml+1):
                if right:
                    xx = (x + start) % fml
                else:
                    xx = (start - x) % fml
                if faces[yy][xx] != 0:
                    return faces[yy][xx] 

        def scany(xx, start, down=True):
            for y in range(1,ml+1):
                if down: yy = (y + start) % len(faces)
                else: yy = (start - y) % len(faces)
                if faces[yy][xx] != 0:
                    return faces[yy][xx]

        for r, fy in enumerate(faces):
            for c, f in enumerate(fy):
                if f != 0:
                    adj[f][0] = (scany(c,r,False),0)
                    adj[f][1] = (scanx(r,c,True),1)
                    adj[f][2] = (scany(c,r,True),2)
                    adj[f][3] = (scanx(r,c,False),3)

        debug(adj)

    else:
        # "easy" adjacencies (base)
        for y, fy in enumerate(faces):
            for x, f in enumerate(fy):
                if f != 0:
                    if y-1 >= 0 and faces[y-1][x] != 0:
                        adj[f][0] = (faces[y-1][x],0)
                    if x+1 < len(fy) and fy[x+1] != 0:
                        adj[f][1] = (fy[x+1],1)
                    if y+1 < len(faces) and faces[y+1][x] != 0:
                        adj[f][2] = (faces[y+1][x],2)
                    if x-1 >= 0 and fy[x-1] != 0:
                        adj[f][3] = (fy[x-1],3)

        # build transitive adjacencies
        while any(any(x is None for x in c) for c in adj.values()):
            for f,a in adj.items():
                for i, af in enumerate(a):
                    if af is not None:
                        ff, r = af
                        for j, aaf in enumerate(adj[ff]):
                            if aaf is not None:
                                fff, rr = aaf
                                if fff != f:
                                    # d... direction from f -> aaf
                                    d = (j - (r-i))%4
                                    # safeguards overwriting previous dirs 
                                    if a[d] is None:
                                        # direction is: 
                                        # opposite of (+2) relative rotation (rr-r) + transitive direction (j)
                                        adj[f][d] = (fff, (rr-r+j+2)%4)

    def face(y,x):
        if 0 <= y < len(b) and 0 <= x < ml:
            return faces[y//FACELEN][x//FACELEN]
        else:
            return 0

    def next(y,x,dir):
        nx,ny = y,x

        # direction increment, 0=up, 1=right, 2=down, 3=left
        if dir == 0: nx -= 1
        elif dir == 1: ny += 1
        elif dir == 2: nx += 1
        elif dir == 3: ny -= 1

        f = face(y,x)
        ff = face(nx,ny)

        if f != ff:
            # moved off face
            move, rot = adj[f][dir]
            fpy, fpx = faceoffs[f]
            fy, fx = y - fpy, x - fpx

            if dir % 2 == 0:
                hold = fx
            else:
                hold = fy

            if (dir ^ rot) in [2,3]:
                hold = FACELEN - hold - 1
            
            wrap = FACELEN - 1 if rot in [0,3] else 0
            if rot % 2 == 0:
                fy, fx = wrap, hold
            else:
                fy, fx = hold, wrap

            nx, ny = faceoffs[move][0] + fy, faceoffs[move][1] + fx
            dir = rot

        return nx, ny, dir
    
    y = 0 
    x = bs[y]
    dir = 0
    for rot, dis in ins:
        dir = (dir + (1 if rot == "R" else -1)) % 4
        for _ in range(dis):
            py, px, pd = next(y, x, dir)
            if b[py][px] == "#": break
            else:
                y, x, dir = py, px, pd
    
    # dirs in whole program are off by one (mod 4) from description, whoops
    print(1000*(y+1)+(x+1)*4+(dir-1)%4)


if __name__ == "__main__":
    main(part=2)