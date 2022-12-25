#!/usr/bin/env python

import sys

S = ["=","-","0","1","2"]


def decimal(sn: str):
    return sum([(S.index(s)-2)*5**i for i,s in enumerate(reversed(sn))])


def snafu(dec: int):
    sn, c = "", 0
    while dec > 0:
        v = dec%5+c
        sn = S[(v+2)%5] + sn
        c = 1 if v > 2 else 0
        dec //= 5
    return "1"+sn if c else sn


if __name__ == "__main__":
    print(snafu(sum([decimal(l) for l in sys.stdin.read().splitlines()])))