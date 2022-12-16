#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

SPACES = 0
def debug(*args, **kwargs):
    if VERBOSE:
        print("    " * SPACES, end="")
        print(*args, **kwargs)

# ==================================================================== #

import re
from collections import deque
import time

EXP = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)")

CAP = 26
DP = []
START = time.perf_counter()

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
    debug(ALD)

    def bv_set(v, i):
        return v | (1 << i)
    
    def bv_get(v, i):
        return (v & (1 << i)) >> i
    
    def bv_debug(v):
        if VERBOSE:
            return [VK[i] for i in range(len(keep)) if bv_get(v, i)]
    
    from functools import lru_cache
    from itertools import product

    # 32 GB are barely enough for this
    @lru_cache(maxsize=45*10**6)
    def dfs(v1: int, v2: int, t1: int, t2: int, f: int, o: int):
        # v1...current valve (human)
        # v2...current valve (elephant)
        # t1...next move (human)
        # t2...next move (elephant)
        # f...current flow
        # o...open valves

        debug(f"Event at minute {min(t1,t2)} with flow {f} and open valves {bv_debug(o)}")
        # moves
        m1 = t1 <= t2
        m2 = t2 <= t1 and not (v1 == v2 and t1 == t2)

        p1 = []
        p2 = []

        if m1 and bv_get(o,v1) == 0:
            # i move
            if VERBOSE:
                debug(f"Human arrived at {VK[v1]} at minute {t1}")

            # open valve
            o = bv_set(o, v1)
            t1 += 1
            gain = (CAP-t1)*WD[v1]
            f += gain

            if VERBOSE:
                debug("Human opens valve at", VK[v1], f"(minute {t1})", "gaining", gain, "flow now", f)

        if m1:
            for i in range(nk):
                if bv_get(o, i) == 0 and ALD[v1][i] + t1 < CAP:
                    p1.append((i, ALD[v1][i] + t1))
        
        if m2 and bv_get(o,v2) == 0:
            # elephant moves
            if VERBOSE:
                debug(f"Elephant arrived at {VK[v2]} at minute {t2}")

            o = bv_set(o, v2)
            t2 += 1
            gain = (CAP-t2)*WD[v2]
            f += gain

            if VERBOSE:
                debug("Elephant opens valve at", VK[v2], f"(minute {t2})", "gaining", gain, "flow now", f)

        if m2:
            for i in range(nk):
                if bv_get(o, i) == 0 and ALD[v2][i] + t2 < CAP:
                    p2.append((i, ALD[v2][i] + t2))

        # base case for one move
        if m2 and not m1:
            p1 = [(v1, t1)]
        if m1 and not m2:
            p2 = [(v2, t2)]

        mf = f

        if VERBOSE:
            debug_pos = lambda y: list(map(lambda x: (VK[x[0]], x[1]), y))
            debug("Possible moves: I: ", debug_pos(p1), "Elefant:", debug_pos(p2))

        for x1, x2 in product(p1,p2):
            v1, t1 = x1
            v2, t2 = x2
            if VERBOSE:
                global SPACES
                SPACES += 1
            if bv_get(o, v1) == 0 and bv_get(o, v2) == 0:
                if VERBOSE:
                    debug((VK[v1], t1), (VK[v2], t2), f)

            mf = max(mf, dfs(v1, v2, t1, t2, f, o))
                
            if VERBOSE:
                debug()
                SPACES -= 1
        return mf

    # sample 
    #print(dfs(5,2,2,1,0,0))

    m = []
    params = keep_lens(start).items()
    for x1,x2 in product(params,params):
        v1,t1 = x1
        v2,t2 = x2
        if v1 != v2:
            m.append(dfs(v1,v2,t1,t2,0,0))

    print(max(m))


if __name__ == "__main__":
    main()