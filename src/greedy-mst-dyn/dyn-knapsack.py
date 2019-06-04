from __future__ import division
#
# Author: Daniel Dittenhafer
#
#     Created: May 30, 2019
#
# Description: Coursera Algorithms Greedy Algos, MST and Dynamic Programming
#
__author__ = 'Daniel Dittenhafer'
import collections
import copy
import itertools
import os
import sys
from timeit import default_timer as timer
from src.utillib.graph import graph, vertex, edge
from src.utillib.myheap import heapqplus
"""
In this programming problem and the next you'll code up the knapsack algorithm
from lecture.

Let's start with a warm-up. Download the text file below.

knapsack1.txt
This file describes a knapsack instance, and it has the following format:

[knapsack_size][number_of_items]

[value_1] [weight_1]

[value_2] [weight_2]

...

For example, the third line of the file is "50074 659", indicating that the
second item has value 50074 and size 659, respectively.

You can assume that all numbers are positive. You should assume that item
weights and the knapsack capacity are integers.
"""

class knapsack:

    def __init__(self):
        pass

    def run(self, verbose=False):

        pass


    def load_data(self, path):
        """Load items in tuples of (id, value, weight)"""

        self._items = []

        with open(path) as fp:
            lines = fp.read().split("\n")

            self._knapsackSize = lines[0].split(' ')[0]

            i = 0
            for line in lines[1:]:
                # Skip blank lines
                if len(line.strip()) > 0:

                    parts = line.split(' ')

                    # Add to the array (id, value, weight)
                    i += 1
                    self._items.append( (i, int(parts[0]), int(parts[1])) )

    def get_mwis_vertex(self, S, i):
        if len(S) > i:
            return str(S[i])
        else:
            return "0"



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
                #op = int(p)
                #if op != 0:
                output.append(p)

        tests.append((test_cases_folder + "\\" + filename, output))


def main():

    tests_correct = 0
    tests = [
        # path to graph file, finishing times dict, leaders dict
        #("D:\\Code\\Python\\py-sandbox\\data\\graph-small2-dijkstra.txt", [1,2,3,4,5,6,7], {}, [0,5,3,4,5,6,6])
    ]

    load_test_cases = True
    tests_correct = 0
    if load_test_cases:
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course3\\assignment4Knapsack")

    # The real problem
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\dyn_mwis.txt", [10100110]))

    # iterate over the test cases
    for t in tests[10:11]:
        m = knapsack()

        # load the graph data (while timing it)
        start = timer()
        m.load_data(t[0])
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        start = timer()
        res = m.run(True)
        end = timer()

        print "knapsack value {0} in {1} secs = {2}/sec".format(res, end - start, len(m._items) / (end - start))
        print res
        #print tree

        expected = t[1]
        ok = len(expected) == 0 or (res == expected[0])
        if not ok:
            print "ERROR! Expected {0}".format(expected[0])
        else:
            print "OK"
            tests_correct += 1

    print "{0} of {1} tests passed = {2}%".format(tests_correct, len(tests), (tests_correct / (len(tests))) * 100)



if __name__ == "__main__":
    main()
