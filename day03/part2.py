#!/usr/bin/env python

import sys

score = 0

def char_prio(c):
    if ord(c) > ord('Z'):
        return ord(c)-ord('a')+1
    else:
        return ord(c)-ord('A')+27

def elf_set(c):
    return {p for p in c}


sets = []
for i, l in enumerate(sys.stdin):
    c = l.strip()
    sets.append(elf_set(c))
    if i % 3 == 2:
        inters = set.intersection(*sets)
        score += sum(map(char_prio, inters))
        sets = []

print(score)
