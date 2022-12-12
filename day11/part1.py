#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ======================================================================

import re
from functools import reduce
M_EXP = re.compile(r"Monkey (\d+):\n\s*Starting items: (.*)\n\s*Operation: new = (.*)\n\s*Test: divisible by (\d+)\n\s*If true: throw to monkey (\d+)\n\s*If false: throw to monkey (\d+)")

M = []
M_INSP = []

def move(m):
    global M, M_INSP
    debug(f"Monkey {m['id']}:")
    while m["items"]:
        M_INSP[m["id"]] += 1
        item = m["items"].pop(0)
        debug("\tinspects", item)
        new_val = eval(m["op"], {"old": item})
        debug("\titem", item,  "evaluates to", new_val)
        bored_val = new_val//3
        debug("\titem", new_val, "divided by 3 is", bored_val)
        if bored_val % m["div_test"] == 0:
            debug("\tCurrent worry level is divisible by", m["div_test"])
            debug("\tthrows", bored_val, "to monkey", m["true_target"])
            M[m["true_target"]]["items"].append(bored_val) 
        else:
            debug("\tCurrent worry level is NOT divisible by", m["div_test"])
            debug("\tthrows", bored_val, "to monkey", m["false_target"])
            M[m["false_target"]]["items"].append(bored_val)
        debug()


def main():
    global M, M_INSP
    input = sys.stdin.read()
    matches = M_EXP.findall(input)
    debug("Matched", len(matches), "monkeys")
    for i, m in enumerate(matches):
        M.append({
            "id": i,
            "items": list(map(int, m[1].split(", "))),
            "op": m[2],
            "div_test": int(m[3]),
            "true_target": int(m[4]),
            "false_target": int(m[5])
        })
    
    M_INSP = [0 for _ in M]
    debug(M)

    for _ in range(20):
        for m in M:
            move(m)
    
    debug(M)
    print(reduce(lambda a,b:a*b, sorted(M_INSP, reverse=True)[:2], 1))
    

# ======================================================================

if __name__ == "__main__":
    main()