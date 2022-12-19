#!/usr/bin/env pypy3

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

import re 

EXP = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")

from functools import reduce

def main():
    bp = EXP.findall(sys.stdin.read())

    END = 32
    # tweak until convergence
    MAXLEN = 3000


    def heur(state):
        t,bal,r = state
        h = [(-r,-b) for b,r in zip(bal,r)][::-1]

        # somehow worse, probably because more focused on balance
        # h = [(-b,-r) for b,r in zip(bal,r)][::-1]
        return (t, *h)


    def bfs(t, bal, rob, cost):
        q = []
        seen = set()

        q.append((t,bal,rob))
        mg = 0

        last_ts = 0
        while q:
            t, bal, rob = q.pop(0)
            seen.add((t,bal,rob))

            if t > last_ts:
                # prune
                q.sort(key=heur)
                q = q[:MAXLEN]
                last_ts = t

            # robots go brrr
            new_bal = (bal[0]+rob[0], bal[1]+rob[1], bal[2]+rob[2], bal[3]+rob[3])
            
            if (t == END):
                mg = max(mg, new_bal[3])
                continue

            constructed = [False for c in cost]
            for i,c in enumerate(cost):
                # I _really_ need a vector class
                if all(cst >= 0 for cst in map(lambda x: x[0]-x[1], zip(bal,c))):
                    cons_bal = tuple([b-cst for b,cst in zip(new_bal, c)])
                    new_robs = list(rob)
                    new_robs[i]+=1
                    q.append((t+1, cons_bal, tuple(new_robs)))
                    constructed[i] = True

            if not all(constructed):
                # when you can construct all robots, it doesn't make sense not to do so
                q.append((t+1, new_bal, rob))
        
        return mg



    res = []
    bp = bp[:min(3,len(bp))]
    for b in bp:
        b = list(map(int, b))
        cost = [(b[1],0,0,0), (b[2],0,0,0), (b[3],b[4],0,0), (b[5],0,b[6],0)]
        x = bfs(1,(0,0,0,0),(1,0,0,0), cost)
        res.append(x)
        debug(f"Blueprint {b[0]}: found result {x}")
    
    print(reduce(lambda a,b: a*b, res ,1))



if __name__ == "__main__":
    main()