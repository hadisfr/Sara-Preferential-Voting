#!/usr/bin/env python3

import json
from datetime import datetime
from collections import Counter

from matplotlib import rcParams, pyplot as plt

rcParams["svg.fonttype"] = "none"


BANNED_IPS = {
}


def get_list(addr):
    with open(addr) as f:
        return set(map(str.strip, f))


def filter_votes(votes, func):
    return map(lambda vote: list(filter(func, vote)), votes)


def get_votes(addr, valid_candidates):
    with open(addr) as f:
        votes = json.load(f)
    print("read %d votes from source" % len(votes))
    votes = filter(lambda itm: "votes" in itm["body"], votes)
    votes = filter(lambda itm: itm["ip"].split(":")[-1] not in BANNED_IPS, votes)
    votes = map(lambda votes: datetime.fromtimestamp(int(votes["datetime"])/1000), votes)
    votes = map(lambda dt: datetime.strftime(dt, "%d %H"), votes)
    return list(votes)


def main():
    valid_candidates = get_list("list.txt")
    print("%d valid candidates" % len(valid_candidates))

    votes = get_votes("output.json", valid_candidates)
    total_voters = len(votes)
    print("%d valid votes" % total_voters)

    c = Counter(votes)
    xs = ["10 %2d" % h for h in range(12, 24)] + ["11 %2d" % h for h in range(0, 21)]

    fig = plt.figure(figsize=(15, 5))
    plt.plot(xs, [c.get(x, 0) for x in xs])
    plt.xlabel("زمان")
    plt.ylabel("رأی در ساعت")
    fig.autofmt_xdate()
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
