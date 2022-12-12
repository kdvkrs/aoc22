#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

path = []
files = {}
dir_sizes = []

def mkdir(p, name):
    f = files
    for d in p:
        f = f[d]
    if not name in f:
        f[name] = {} 

def touch(p, name, size):
    f = files
    for d in p:
        f = f[d]
    f[name] = size

for i, l in enumerate(sys.stdin):
    l = l.strip()
    if l.startswith("$"):
        if l[2:].startswith("cd"):
            p = l[2:].split(" ")[1].strip()
            if p == "/":
                path.clear()
            elif p == "..":
                path.pop()
            else:
                path.append(p)
            debug("CD to", p)
        elif l[2:].startswith("ls"):
            pass
            debug("LS", p)
        debug("PATH: ", "/"+"/".join(path))
    else:
        sz, name = l.split(" ")
        if sz == "dir":
            mkdir(path, name)
            debug("DIR", name)
        else:
            touch(path, name, int(sz))
            debug("FILE {} with size {}".format(name, sz))

size = 0
sizes = {}
dir_sizes = []

def fs(f: dict) -> int:
    global size, dir_sizes
    sz = 0
    for k, v in f.items():
        if isinstance(v, dict):
            x = fs(v)
            sizes[k] = x
            sz += x
        else:
            sz += v
    if sz <= 100000:
        size += sz
    dir_sizes.append(sz)
    return sz

avail = 70000000 - fs(files)
debug(f"{avail=}")
needed = 30000000 - avail
debug(f"{needed=}")

for d in sorted(dir_sizes):
    if d > needed:
        print(d)
        break
    