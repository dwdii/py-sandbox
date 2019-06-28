from __future__ import division
#
# Author: Daniel Dittenhafer
#
#     Created: June 19, 2019
#
# Description: Coursera Algorithms Shortest Paths, NP Complete, etc.
#
__author__ = 'Daniel Dittenhafer'
import collections
import copy
import decimal
import itertools
import math
import os
import sys
from timeit import default_timer as timer
from src.utillib.graph import graph, vertex, edge

"""
In this assignment you will implement one or more algorithms for the traveling
salesman problem, such as the dynamic programming algorithm covered in the
video lectures. Here is a data file describing a TSP instance.

tsp.txt

The first line indicates the number of cities. Each city is a point in the
plane, and each subsequent line indicates the x- and y-coordinates of a
single city.

The distance between two cities is defined as the Euclidean distance --- that
is, two cities at locations (x,y) and (z,w) have distance \sqrt{(x-z)^2 + (y-w)^2}
between them.

In the box below, type in the minimum cost of a traveling salesman tour for
this instance, rounded down to the nearest integer.

https://www.youtube.com/watch?v=-JjA4BLQyqE
"""



class traveling_salesman:

    def __init__(self):
        pass

    def run(self, P, D, s, verbose=False):
        A = {}
        n = len(P)
        for m in xrange(2, n):
            mSets = list(itertools.permutations(P.keys(), m))
            for S in mSets:
                if not S.contains(s):
                    continue

                A[S] = {}
                for j in S:
                    if j == s:
                        continue

                    candidates = [0] #[A[S-j][k] + Ckj]
                    A[S][j] = min(candidates)
        pass

    def recurrence(self, A):
        pass


    def load_data(self, f):
        D = {}
        P = {}
        v = 1
        with open(f) as fp:
            lines = fp.read().split("\n")
            for line in lines[1:]:
                if(len(line.strip()) > 0):
                    parts = line.split(" ")
                    P[v] = (decimal.Decimal(parts[0]), decimal.Decimal(parts[1]))
                    v += 1


        for p in P:
            D[p] = {}
            p1 = P[p]
            for d in P:
                #if d == p:
                #    continue
                #else:
                p2 = P[d]
                D[p][d] = math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))

        return P, D

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
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course4\\assignment2TSP")

    # The real problem
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\shortest-path-tsp.txt", ['NULL']))

    # iterate over the test cases
    it = 0
    for t in tests[0:1]:
        m = traveling_salesman()

        # load the graph data (while timing it)
        start = timer()
        P, D = m.load_data(t[0])
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        start = timer()
        res, res2 = m.run(P, D, 1, True)
        end = timer()

        print "[{3}] bellman ford sp = {0} in {1} secs = {2}/sec".format(res, end - start, len(g.vertices) / (end - start), it)
        print res, res2
        if res is None:
            res = "NULL"

        expected = t[1]
        ok = len(expected) == 0 or (str(res) == expected[0])
        if not ok:
            print "ERROR! Expected {0}".format(expected[0])
        else:
            print "OK"
            tests_correct += 1

    print "{0} of {1} tests passed = {2}%".format(tests_correct, len(tests), (tests_correct / (len(tests))) * 100)


if __name__ == "__main__":
    main()
