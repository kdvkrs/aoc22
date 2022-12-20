#!/usr/bin/env pypy3

import sys
from collections import deque 

def main(part=1):
    DECRYPT = 811589153 if part==2 else 1
    q = deque(enumerate(map(lambda x: DECRYPT*int(x),sys.stdin.read().splitlines())))
    l = len(q)
    for _ in range(10 if part==2 else 1):
        for i in range(l):
            while q[0][0] != i:
                q.rotate(-1)
            ii, v = q.popleft()
            q.rotate(-v)
            q.appendleft((ii,v))
    while q[0][1] != 0:
        q.rotate(-1)
    print(sum([q[i][1] for i in [1000%l, 2000%l, 3000%l]]))


if __name__ == "__main__":
    main()