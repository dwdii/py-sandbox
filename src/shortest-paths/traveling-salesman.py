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
#from src.utillib.graph import graph, vertex, edge

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

loaded tsp.txt in 0.0170431137085 secs
n: 25
m: 2
m: 3
m: 4
m: 5
m: 6
m: 7
m: 8
m: 9
m: 10
m: 11
m: 12
m: 13
m: 14
m: 15
m: 16
m: 17
m: 18
m: 19
m: 20
m: 21
m: 22
m: 23
m: 24
m: 25
[0] tsp = 26442 in 1313.1338439 secs = 0.0190384248461/sec
26442
OK
1 of 1 tests passed = 100.0%

"""



class traveling_salesman:

    def __init__(self):
        self.infinity = 18446744073709551615


    def run(self, P, D, s, verbose=False):
        A = {}
        n = len(P)
        if verbose:
            print "n: {0}".format(n)

        for p in P:
            S = frozenset([p])
            A[S] = {}
            if p == s:
                A[S][p] = D[s][p]
            else:
                A[S][p] = self.infinity

        for m in xrange(2, n + 1):
            if verbose:
                print "m: {0}".format(m)
            mSets = list(itertools.combinations(P.keys(), m))
            for S in mSets:
                #print "S: {0}".format(S)
                fs = frozenset(S)
                if s not in fs:
                    continue

                A[fs] = {}
                A[fs][1] = self.infinity

                for j in fs:
                    if j == s:
                        continue

                    Sminusj = fs.difference(set([j]))
                    candidates = []
                    for k in fs:
                        if k != j:
                            candidates.append(A[Sminusj][k] + D[k][j])

                    A[fs][j] = min(candidates)

        final = []
        fs = frozenset(P.keys())
        for j in P:
            if j == 1:
                continue

            final.append(A[fs][j] + D[j][1])

        res = min(final)

        return int(round(res-0.5))

    def load_data(self, f):
        """Loads the graph from the file f.

        Returns:
            P dict of points as (x,y) tuples
            D dict of distance dictionaries (matrix) from u to v (1 based)
        """
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

    load_test_cases = False
    tests_correct = 0
    if load_test_cases:
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course4\\assignment2TSP")

    # The real problem
    tests.append(("D:\\Code\\Python\\py-sandbox\\data\\shortest-path-tsp.txt", ['NULL']))

    # iterate over the test cases
    it = 0
    for t in tests:
        m = traveling_salesman()

        # load the graph data (while timing it)
        start = timer()
        P, D = m.load_data(t[0])
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        start = timer()
        res = m.run(P, D, 1, True)
        end = timer()

        print "[{3}] tsp = {0} in {1} secs = {2}/sec".format(res, end - start, len(P) / (end - start), it)
        print res
        if res is None:
            res = "NULL"

        expected = t[1]
        ok = len(expected) == 0 or (str(res) == expected[0])
        if not ok:
            print "ERROR! Expected {0}".format(expected[0])
        else:
            print "OK"
            tests_correct += 1

        it += 1

    print "{0} of {1} tests passed = {2}%".format(tests_correct, len(tests), (tests_correct / (len(tests))) * 100)


if __name__ == "__main__":
    main()
