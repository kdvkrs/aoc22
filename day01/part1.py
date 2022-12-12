#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

elves = []
new_elf = True

for _, l in enumerate(sys.stdin):
    l = l.strip()

    if l == '':
        new_elf = True
        continue

    if new_elf:
        elves.append(int(l))
        new_elf = False
    else:
        elves[-1] += int(l)

def main():
    print(max(elves))


if __name__ == "__main__":
    main()