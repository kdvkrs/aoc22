#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

import re
from collections import deque

EXP = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)")

CAP = 30
DP = []

def main():
    AL = {}
    V = {}
    VK = {}
    WD = {}
    al = {}
    idx = 0
    keep = []
    for _, l in enumerate(sys.stdin):
        v, r, lead = EXP.match(l.strip()).groups()
        V[v] = idx
        if int(r) > 0:
            WD[len(keep)] = int(r)
            VK[len(keep)] = v
            keep.append(idx)
        ls = lead.split(", ")
        al[v] = ls
        #debug(v, r, lead)

        idx += 1
    
    start = V["AA"]
    nk = len(keep)

    AL = {V[k]: [V[v] for v in vs] for k, vs in al.items()}
    for v in V.values():
        AL[v].append(v)

    debug(VK)
    def keep_lens(i):

        q = deque([(i,0)])

        ald = {}

        while q:
            v, d = q.popleft()
            if v in ald:
                continue
            else:
                ald[v] = d
                for n in AL[v]:
                    q.append((n,d+1))

        ald = {keep.index(k):d for k,d in ald.items() if k in keep}        
        return ald

    ALD = {i:keep_lens(v) for i,v in enumerate(keep)}

    def bv_set(v, i):
        return v | (1 << i)
    
    def bv_get(v, i):
        return (v & (1 << i)) >> i
    
    def bv_debug(v):
        return [VK[i] for i in range(len(keep)) if bv_get(v, i)]
    
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(v: int,t: int,f: int, o: int):
        # current valve, time, flow, open valves

        if VERBOSE:
            debug(f"Arrived at {VK[v]} at minute {t} with flow {f} and open valves {bv_debug(o)}")

        if t >= CAP:
            return f

        # open valve
        o = bv_set(o, v)
        t += 1
        gain = (CAP-t)*WD[v]
        f += gain

        if VERBOSE:
            debug("Opening valve at", VK[v], f"(minute {t})", "gaining", gain, "flow now", f)

        mf = f
        for i in range(nk):
            if bv_get(o, i) == 0 and ALD[v][i] + t < CAP:
                mf = max(mf, dfs(i, ALD[v][i] + t, f, o))
        return mf

    m = []
    for v,t,f,o in [(k,v,0,0) for k,v in keep_lens(start).items()]:
        m.append(dfs(v,t,f,o))

    print(max(m))



if __name__ == "__main__":
    main()