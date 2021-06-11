#!/usr/bin/env python3

import json
from itertools import combinations


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
    votes = dict(map(lambda itm: (itm["body"]["voter_id"], itm["body"]["votes"]), votes))
    votes = votes.values()
    votes = filter_votes(votes, lambda candidate: candidate in valid_candidates)
    votes = filter(lambda vote: len(vote) > 0, votes)
    return list(votes)


def main():
    valid_candidates = get_list("list.txt")
    print("%d valid candidates" % len(valid_candidates))

    votes = get_votes("output.json", valid_candidates)
    total_voters = len(votes)
    print("%d valid votes" % total_voters)

    with open("votes.graph.csv", "w") as f:
        for vote in votes:
            for edge in combinations(vote, 2):
                print(",".join(edge), file=f)


if __name__ == '__main__':
    main()
