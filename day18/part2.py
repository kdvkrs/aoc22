#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

CO = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]

def main():
    l = sys.stdin.read().strip().splitlines()
    cubes = [tuple(map(int, x.split(","))) for x in l]

    xmax = xmin = cubes[0][0]
    ymax = ymin = cubes[0][1]
    zmax = zmin = cubes[0][2]

    for c in cubes:
        xmax, xmin = max(xmax, c[0]), min(xmin, c[0])
        ymax, ymin = max(ymax, c[1]), min(ymin, c[1])
        zmax, zmin = max(zmax, c[2]), min(zmin, c[2])

    # make ("outer") bounding box for search slightly larger
    bbox = (xmax+1, xmin-1, ymax+1, ymin-1, zmax+1, zmin-1)

    # threshold is difference between "outer" and proper bounding box 
    TH = (bbox[0]-bbox[1])*(bbox[2]-bbox[3])*(bbox[4]-bbox[5])-(xmax-xmin)*(ymax-ymin)*(zmax-zmin)

    # fast lookup
    cubes = set(cubes)

    # points outside/inside droplet
    extr = set()
    intr = set()

    def exterior(x,y,z):
        vis = set()
        q = [(x,y,z)] 
        is_extr = False
        while q:
            x,y,z = q.pop(0)
            if (x,y,z) in vis or (x,y,z) in cubes:
                continue
            vis.add((x,y,z))
            if len(vis) > TH or (x,y,z) in extr:
                is_extr = True 
                break
            if (x,y,z) in intr:
                break
            for so in CO:
                nc = x+so[0], y+so[1], z+so[2]
                # only search relevant area (bounding box + 1 in each direction)
                if nc[0] > bbox[0] or nc[0] < bbox[1] or \
                    nc[1] > bbox[2] or nc[1] < bbox[3] or \
                    nc[2] > bbox[4] or nc[2] < bbox[5]:
                    continue
                q.append(nc)
        if is_extr:
            for v in vis:
                extr.add(v)
        else:
            for v in vis:
                intr.add(v)
        return is_extr

    outsides = 0
    for x,y,z in cubes:
        for co in CO:
            nc = x+co[0], y+co[1], z+co[2]
            if nc not in cubes:
                if exterior(*nc):
                    outsides += 1
            
    print(outsides)

if __name__ == "__main__":
    main()