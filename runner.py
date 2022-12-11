# modified version of https://github.com/exoji2e/aoc22/blob/main/runner.py, courtesy of exoji2e on GitHub

import time, os, sys
from datetime import datetime, timezone, timedelta
import progressbar
import requests

DATEFMT = r"%Y-%m-%d %H:%M:%S %Z"

def dl(fname, day, year):
    from secret import session
    jar = requests.cookies.RequestsCookieJar()
    jar.set('session', session)
    url = 'https://adventofcode.com/{}/day/{}/input'.format(year, day)
    r = requests.get(url, cookies=jar)
    if 'Puzzle inputs' in r.text:
        print('ERROR: Session cookie expired?', file=sys.stderr)
        return r.text
    if "Please don't repeatedly request this endpoint before it unlocks!" in r.text:
        print('ERROR: Output not available yet', file=sys.stderr)
        return r.text
    if r.status_code != 200:
        print('ERROR: Not 200 as status code', file=sys.stderr)
        return r.text
    with open(fname,'w') as f:
        f.write(r.text)
    return 0


def wait_until(date_time):
    now = datetime.now().astimezone()
    tE = date_time.timestamp()
    t0 = now.timestamp()
    t_diff = int(tE - t0)

    if tE < t0: 
        return

    widgets=[
        ' [', progressbar.CurrentTime(), '] ',
        progressbar.Bar(),
        ' (', progressbar.ETA(), ') ',
    ]
    print(f'Waiting from {now.strftime(DATEFMT)} until {date_time.strftime(DATEFMT)}')
    bar = progressbar.ProgressBar(max_value=int(tE-t0), widgets=widgets)
    while time.time() < tE:
        cT = time.time()
        bar.update(min(t_diff, int(cT - t0)))
        time.sleep(1)
    bar.finish()


def fetch(year, day, force=False):
    filename = f"day{day:02d}/inputs/input.in"
    exists = os.path.isfile(filename)
    wait_until_date = release_time(year, day)
    if not exists or force:
        if wait_until_date > datetime.now().astimezone():
            wait_until(wait_until_date)

        out = dl(filename, day, year)
        if out != 0:
            return out
    return open(filename, 'r').read().strip('\n')


def release_time(year, day):
    target = datetime(year, 12, day, 5, tzinfo=timezone.utc).astimezone()
    return target + timedelta(milliseconds=200)


def create_day(day):
    path = os.path.dirname(os.path.realpath(__file__))
    folder = f'day{day:02d}'
    # copy templates folder to day
    try:
        os.system(f'cp -r -i {path}/template {path}/{folder}')
    except FileExistsError:
        print(f'Folder {folder} already exists, continue? (y/n)')
        resp = input()
        if resp.lower() != 'y':
            return False
    return True
