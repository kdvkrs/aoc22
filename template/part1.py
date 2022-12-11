#!/usr/bin/env python

import sys

VERBOSE = "-v" in sys.argv

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ==================================================================== #

def main():
    for i, l in enumerate(sys.stdin):
        pass 

    print(f"Hello World")
    debug(f"Hello Debug")

if __name__ == "__main__":
    main()