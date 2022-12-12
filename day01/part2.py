#!/usr/bin/env python

from part1 import *


def main():
    print(sum(sorted(elves, reverse=True)[:3]))

# ==================================================================== #

if __name__ == '__main__':
    main()
