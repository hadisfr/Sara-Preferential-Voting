#!/usr/bin/env python3

import json
import math
from itertools import chain
from collections import Counter
from os import path


QUORUM_FRACTION = 1/3
ITERATION_MAX_VOTE_COUNT = 21
DST_PATH = "itr"


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


def write_counts(addr, votes_counted, total_voters, names):
    with open(addr, "w") as f:
        print(",".join(["Candidate", "Votes", "Percentage of Original Voters", "Name"]), file=f)
        for itm in votes_counted:
            candidate, votes = itm
            percentage = votes * 100 / total_voters
            print(",".join([candidate, str(votes), "%.3f" % percentage, names[candidate]]), file=f)


def get_names(addr):
    with open(addr) as f:
        names = dict()
        for line in f:
            s = line.split(",")
            assert len(s) == 2
            names[s[0]] = s[1].strip()
    return names


def count(votes, quorum, total_voters, names):
    def count_iter(votes):
        votes_counted = Counter(chain(*map(lambda vote: vote[:ITERATION_MAX_VOTE_COUNT], votes))).most_common()
        elected_candidates = list(map(lambda t: t[0], filter(lambda t: t[1] >= quorum, votes_counted)))
        elected_candidates_count = len(elected_candidates)
        print("%d elected candidates" % elected_candidates_count)

        min_count = min(quorum, votes_counted[-1][1])
        min_candidates = set(map(lambda t: t[0], filter(lambda t: t[1] <= min_count, votes_counted)))
        min_candidates_count = len(min_candidates)
        print("%d removed candidates" % min_candidates_count)

        votes = list(filter_votes(votes, lambda candidate: candidate not in min_candidates))
        
        return votes_counted, elected_candidates_count, min_candidates_count, votes

    elected_candidates_count, min_candidates_count = 0, ITERATION_MAX_VOTE_COUNT
    itr = 0
    while elected_candidates_count < ITERATION_MAX_VOTE_COUNT and min_candidates_count > 0:
        itr += 1
        print("\nIteration %d" % itr)
        votes_counted, elected_candidates_count, min_candidates_count, votes = count_iter(votes)
        write_counts(path.join(DST_PATH, "itr%d.csv" % itr), votes_counted, total_voters, names)


def main():
    valid_candidates = get_list("list.txt")
    print("%d valid candidates" % len(valid_candidates))
    names = get_names("95code.csv")

    votes = get_votes("output.json", valid_candidates)
    total_voters = len(votes)
    print("%d valid votes" % total_voters)
    quorum = math.ceil(total_voters * QUORUM_FRACTION)
    print("quorum = %d" % quorum)

    print("\n")

    count(votes, quorum, total_voters, names)


if __name__ == '__main__':
    main()
