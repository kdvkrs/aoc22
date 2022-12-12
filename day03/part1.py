#!/usr/bin/env python

import sys

score = 0

def char_prio(c):
    if ord(c) > ord('Z'):
        return ord(c)-ord('a')+1
    else:
        return ord(c)-ord('A')+27

def get_prio(c):
    p1 = c[:len(c)//2]
    p2 = c[len(c)//2:]
    i = {p for p in p1}.intersection({p for p in p2})
    return sum(map(char_prio, i))


for i, l in enumerate(sys.stdin):
    c = l.strip()
    score += get_prio(c) 

print(score)