#!/usr/bin/env python

import sys
MD = {m: exp for m,exp in map(lambda x: x.split(": "), sys.stdin.read().splitlines())}
def mn(m):
    exp = MD[m].split(" ")
    return int(eval("".join(exp), {exp[i]:mn(exp[i]) for i in [0,2]} if len(exp)==3 else {}))
print(mn("root"))
