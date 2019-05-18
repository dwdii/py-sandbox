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
from src.utillib.graph import graph
"""
You should NOT assume that edge costs are positive, nor should you assume that
they are distinct.

Your task is to run Prim's minimum spanning tree algorithm on this graph. You
should report the overall cost of a minimum spanning tree --- an integer, which
may or may not be negative.

IMPLEMENTATION NOTES: This graph is small enough that the straightforward O(mn)
time implementation of Prim's algorithm should work fine. OPTIONAL: For those
of you seeking an additional challenge, try implementing a heap-based version.
The simpler approach, which should already give you a healthy speed-up, is to
maintain relevant edges in a heap (with keys = edge costs). The superior
approach stores the unprocessed vertices in the heap, as described in lecture.
Note this requires a heap that supports deletions, and you'll probably need to
maintain some kind of mapping between vertices and their positions in the heap.
"""
class min_spanning_tree:

    def __init__(self):
        pass

    def run(self, g):
        X = {}
        T = []
        avail = []

        # Add the initial vertex
        X[1] = 1

        for e in g.edges:
            avail.append(e)


        done = False
        while not done:

            me = None
            for e in avail:
                if ( (X.has_key(e[0].id) and not X.has_key(e[1].id)) or
                     (X.has_key(e[1].id) and not X.has_key(e[0].id)) ):

                    if me is None:
                         me = e
                    elif me.weight > e.weight:
                        me = e
                #elif (X.has_key(e[0].id) and X.has_key(e[1].id)):
                #    avail.remove(e)


            T.append(me)
            avail.remove(me)
            if me[0].id in X:
                X[me[1].id] = 1
            else:
                X[me[0].id] = 1


            # Are we done yet?
            done = len(X) == len(g.vertices)

        mst_cost = 0
        for e in T:
            mst_cost += e.weight

        return mst_cost, T

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
                if op != 0:
                     output.append(op)

        tests.append((test_cases_folder + "\\" + filename, output))


def main():

    tests_correct = 0
    tests = [
        # path to graph file, finishing times dict, leaders dict
        #("D:\\Code\\Python\\py-sandbox\\data\\graph-small2-dijkstra.txt", [1,2,3,4,5,6,7], {}, [0,5,3,4,5,6,6])
    ]

    load_test_cases = False
    tests_correct = 0
    if load_test_cases:
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course3\\assignment1SchedulingAndMST\\question3")

    # The real problem
    tests.append(("D:\\Code\\Python\\py-sandbox\\data\\mst_edges.txt", [-3612829]))

    # iterate over the test cases
    for t in tests:
        # load the graph data (while timing it)
        start = timer()
        g = graph()
        g.load_data2(t[0], verbose=True, delim=" ")
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        m = min_spanning_tree()

        start = timer()
        res, tree = m.run(g)
        end = timer()

        print "mst of {0} in {1} secs = {2}/sec".format(res, end - start, len(g.vertices) / (end - start))
        print res
        #print tree

        expected = t[1]
        ok = len(expected) == 0 or res == expected[0]
        if not ok:
            print "ERROR! Expected {0}".format(expected[0])
        else:
            print "OK"
            tests_correct += 1

    print "{0} of {1} tests passed = {2}%".format(tests_correct, len(tests) * 2, (tests_correct / (len(tests) * 2)) * 100)


if __name__ == "__main__":
    main()
