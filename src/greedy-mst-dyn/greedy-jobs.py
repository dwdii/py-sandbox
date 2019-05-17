from __future__ import division
#
# Author: Daniel Dittenhafer
#
#     Created: May 15, 2019
#
# Description: Coursera Algorithms Greedy Algos, MST and Dynamic Programming
#
__author__ = 'Daniel Dittenhafer'
import collections
import copy
import heapq
import itertools
import os
import sys
from timeit import default_timer as timer
"""
You should NOT assume that edge weights or lengths are distinct.

Your task in this problem is to run the greedy algorithm that schedules jobs
in decreasing order of the difference (weight - length). Recall from lecture
that this algorithm is not always optimal. IMPORTANT: if two jobs have equal
difference (weight - length), you should schedule the job with higher weight
first. Beware: if you break ties in a different way, you are likely to get 
the wrong answer. You should report the sum of weighted completion times of 
the resulting schedule --- a positive integer --- in the box below.
"""

class job_scheduler:

    def __init__(self):
        self.WEIGHT = 0
        self.LENGTH = 1
        self.GREEDY = 2
        pass

    def run(self, data, fnscore, verbose=False):

        scores = []

        # compute greedy scores
        for d in data:
            d.append(fnscore(d[self.WEIGHT], d[self.LENGTH]))
            scores.append(d)
        
        # Sort the jobs by score
        scores.sort(self.job_cmp, reverse=True)

        # Compute weighted completion times
        ct = 0
        wct = 0
        swct = 0
        for d in scores:
            ct += d[self.LENGTH]
            wct = ct * d[self.WEIGHT]
            d.append(wct)
            swct += wct

        return swct, scores

    def job_cmp(self, a, b):

        if a[self.GREEDY] < b[self.GREEDY]:
            return -1
        elif a[self.GREEDY] > b[self.GREEDY]:
            return 1
        else:
            # need to add tie breaker based on weight...? ???
            if a[self.WEIGHT] > b[self.WEIGHT]:
                return 1
            elif a[self.WEIGHT] < b[self.WEIGHT]:
                return -1
            else:
                return 0


def job_greedy_score_difference(weight, length):
    return weight - length

def job_greedy_score_ratio(weight, length):
    return weight / length

def load_job_data(path):

    arr = []
    with open(path) as fp:
        lines = fp.read().split("\n")
        for l in lines[1:]:
            if len(l) > 0:
                w, l = l.split(" ")
                arr.append([int(w), int(l)])

    return arr

def load_stanford_algs_test_cases(tests, test_cases_folder):
    
    for filename in os.listdir(test_cases_folder):
        if filename[:5] != 'input':
            continue

        outputfile = filename.replace("input_", "output_")
        with open(test_cases_folder + "\\" + outputfile) as fp:
            expected_out = fp.read().split("\n")

        output = []
        for p in expected_out:
            if len(p) > 0:
                op = int(p)
                if op > 0:
                    output.append(op)

        tests.append((test_cases_folder + "\\" + filename, output))


def main():

    tests_correct = 0
    tests = [
        # path to graph file, finishing times dict, leaders dict
        #("D:\\Code\\Python\\py-sandbox\\data\\graph-small2-dijkstra.txt", [1,2,3,4,5,6,7], {}, [0,5,3,4,5,6,6])
    ]

    load_test_cases = False
    if load_test_cases:
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course3\\assignment1SchedulingAndMST\\questions1And2")

    # The real problem
    tests.append(("D:\\Code\\Python\\py-sandbox\\data\\greedy-jobs.txt", [69119377652, 67311454237]))

    # iterate over the test cases
    for t in tests:
        # load the job data (while timing it)
        start = timer()
        data = load_job_data(t[0])
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        s = job_scheduler()
        # First pass is using greedy difference score
        dc1 = copy.deepcopy(data)
        start = timer()
        res, scores = s.run(dc1, job_greedy_score_difference, verbose=False)
        end = timer()
        print "jobs DIFF swct of {0} in {1} secs = {2}/sec".format(res, end - start, len(scores) / (end - start))
        print res

        expected = t[1]
        ok = len(expected) == 0 or res == expected[0] 
        if not ok:
            print "ERROR! Expected {0}".format(expected[0])
        else:
            print "OK"
            tests_correct += 1

        # Second pass is using greedy ratio score
        dc2 = copy.deepcopy(data)
        start = timer()
        res, scores = s.run(dc2, job_greedy_score_ratio, verbose=False)
        end = timer()
        print "jobs RATIO swct of {0} in {1} secs = {2}/sec".format(res, end - start, len(scores) / (end - start))
        print res

        expected = t[1]
        ok = len(expected) == 0 or res == expected[1] 
        if not ok:
            print "ERROR! Expected {0}".format(expected[1])
        else:
            print "OK"
            tests_correct += 1

    
    print "{0} of {1} tests passed = {2}%".format(tests_correct, len(tests) * 2, (tests_correct / (len(tests) * 2)) * 100)


if __name__ == "__main__":
    main()
