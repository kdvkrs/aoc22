#!/usr/bin/env python3

import argparse
from runner import wait_until, release_time, create_day, fetch

YEAR = 2022

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('day', type=int, help='Day of December for which directory should be created')
    args = parser.parse_args()
    day = args.day

    wait_until(release_time(YEAR, day))
    create_day(day)
    fetch(YEAR, day)

    print("Successfully created directory for day {}".format(day))

if __name__ == '__main__':
    main()