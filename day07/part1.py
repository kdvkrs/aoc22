#!/usr/bin/env python

import sys

path = []
files = {}
dirs = []

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
            #print("CD to", p)
        elif l[2:].startswith("ls"):
            pass
            #print("LS", p)
        #print("PATH: ", "/"+"/".join(path))
    else:
        sz, name = l.split(" ")
        if sz == "dir":
            mkdir(path, name)
            #print("DIR", name)
        else:
            touch(path, name, int(sz))
            #print("FILE {} with size {}".format(name, sz))

size = 0
sizes = {}

def fs(f: dict) -> int:
    global size
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
    return sz

fs(files)
print(size)
    
    