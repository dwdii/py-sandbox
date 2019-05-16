#
# Author: Daniel Dittenhafer
#
#     Created: May 15, 2019
#
# Description: Coursera Algorithms Greedy Algos, MST and Dynamic Programming
#
__author__ = 'Daniel Dittenhafer'
import collections
import graph
import heapq
import itertools
import myheap
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
        pass

    def run(self, data, verbose=False):
        pass


def load_stanford_algs_test_cases(tests, test_cases_folder):
    
    for filename in os.listdir(test_cases_folder):
        if filename[:5] != 'input':
            continue

        outputfile = filename.replace("input_", "output_")
        with open(test_cases_folder + "\\" + outputfile) as fp:
            expected_out = fp.read().split(",")

        output = []
        for p in expected_out:
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
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\greedy-jobs.txt", []))

    # iterate over the test cases
    for t in tests:
        # load the graph (while timing it)
        start = timer()
        data = load_int_array(t[0])
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        start = timer()
        s = job_scheduler()
        res, found = s.run(data, verbose=False)
        end = timer()
        print "twosum of {0} in {1} secs = {2}/sec".format(len(data), end - start, len(data) / (end - start))
        print res

        expected = t[1]
        ok = len(expected) == 0 or res == expected[0] 
        if not ok:
            print "ERROR! Expected {0}".format(expected[0])
            c = collections.defaultdict(int)
            for k in found:
                c[k] += 1
                c[found[k]] += 1
                
            
            for k in c:
                print "{0}: {1}".format(k, c[k])

            print ""

            
        else:
            print "OK"
            tests_correct += 1
    
    print "{0} of {1} tests passed".format(tests_correct, len(tests))


if __name__ == "__main__":
    main()
