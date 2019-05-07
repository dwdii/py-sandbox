#
# Author: Daniel Dittenhafer
#
#     Created: May 6, 2019
#
# Description: Coursera Algorithms Graph Search and Data Structures
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
The goal of this problem is to implement the "Median Maintenance" algorithm 
(covered in the Week 3 lecture on heap applications). The text file contains
a list of the integers from 1 to 10000 in unsorted order; you should treat 
this as a stream of numbers, arriving one by one.
"""

class streaming_median:

    def __init__(self):
        self._lower = []
        self._upper = []

    @property
    def median(self):
        if (len(self._lower) == len(self._upper) or
            len(self._lower) > len(self._upper)):
            return self._lower[0] * -1
        elif len(self._lower) < len(self._upper):
            return self._upper[0]
        else:
            return self._lower[0] * -1

    def add(self, value, verbose=False):
        if len(self._upper) and value < self._upper[0]:
            heapq.heappush(self._lower, value * -1)
        elif len(self._lower) and value > self._lower[0] * -1:
            heapq.heappush(self._upper, value)
        else:
            heapq.heappush(self._lower, value * -1)

        if len(self._upper) > len(self._lower) + 1:
            # upper bigger, so rebalance
            heapq.heappush(self._lower, heapq.heappop(self._upper) * -1)
        elif len(self._upper) + 1 < len(self._lower):
            # lower bigger, so rebalance
            heapq.heappush(self._upper, heapq.heappop(self._lower) * -1)
            

def load_int_array(path):
    arr = []
    with open(path) as fp:
        lines = fp.read().split("\n")
        for l in lines:
            if len(l) > 0:
                arr.append(int(l))

    return arr


def load_stanford_algs_test_cases(tests):
    test_cases_folder = "D:\\Code\\other\\stanford-algs\\testcases\\course2\\assignment3Median"
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

    load_test_cases = True
    if load_test_cases:
        load_stanford_algs_test_cases(tests)

    # The real problem
    tests.append(("D:\\Code\\Python\\py-sandbox\\data\\graphs-median.txt", [1213]))

    # iterate over the test cases
    for t in tests[0:45]:
        # load the graph (while timing it)
        start = timer()
        data = load_int_array(t[0])
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        start = timer()
        s = streaming_median()
        sum = 0
        for v in data:
            s.add(v, verbose=True)
            sum += s.median

        res = sum % 10000
        end = timer()
        print "mediam streamed in {0} secs".format( end - start)
        print res

        expected = t[1]
        ok = res == expected[0] 
        if not ok:
            print "ERROR!"
        else:
            print "OK"
            tests_correct += 1
    
    print "{0} of {1} tests passed".format(tests_correct, len(tests))

if __name__ == "__main__":
    main()