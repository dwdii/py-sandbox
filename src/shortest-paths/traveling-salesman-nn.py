from __future__ import division
#
# Author: Daniel Dittenhafer
#
#     Created: July 2, 2019
#
# Description: Coursera Algorithms Shortest Paths, NP Complete, etc.
#
__author__ = 'Daniel Dittenhafer'
import collections
import copy
import decimal
import src.utillib.myheap
import itertools
import math
import os
import sys
from timeit import default_timer as timer
"""
You should implement the nearest neighbor heuristic:

Start the tour at the first city.

Repeatedly visit the closest city that the tour hasn't visited yet.

In case of a tie, go to the closest city with the lowest index. For example,
if both the third and fifth cities have the same distance from the first city
(and are closer than any other city), then the tour should begin by going from
the first city to the third city.

Once every city has been visited exactly once, return to the first city to
complete the tour.
"""

class traveling_salesman_nn:

    def __init__(self):
        self.infinity = 18446744073709551615

    def run(self, P, D, s, verbose=False):

        total = 0

        visited = {}
        visited[s] = 1

        ci = s

        remaining = set(P.keys())
        remaining.remove(s)

        done = False
        while not done:

            nd = self.infinity
            ni = 0
            #start = timer()
            #for p in remaining:
            #    if visited.has_key(p):
            #        continue
            #    else:
            #        cd = D[ci][p]
            #        if cd < nd:
            #            ni = p
            #            nd = cd
            found = False
            while not found:
                cd, p = D[ci].pop()
                if visited.has_key(p):
                    continue
                else:
                    ni = p
                    nd = math.sqrt(cd)
                    found = True

            total += nd
            visited[ni] = 1
            remaining.remove(ni)
            ci = ni
            if len(remaining) == 0:
                done = True

            #end = timer()
            #print "Visited: {0} in {1} secs".format(len(visited), end - start)

        # Go back to source
        #cd = D[ci][s]
        cd = D[ci].remove(s)
        total += math.sqrt(cd)

        return int(round(total-0.5))

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
                    P[v] = (float(parts[1]), float(parts[2]))
                    v += 1


        for p in P:
            #D[p] = {}
            D[p] = src.utillib.myheap.heapqplus()
            p1 = P[p]
            #start = timer()
            for d in P:
                ed = None
                if D.has_key(d):
                    ed = D[d].get(p)

                if ed is None:
                    p2 = P[d]
                    #ed = math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))
                    ed = math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2)

                D[p].add(d, ed)
                #D[p][d] =

            #end = timer()
            #print "Distances for {0} computed in {1} secs".format(p, end - start)


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
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course4\\assignment3TSPHeuristic")

    # The real problem
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\shortest-path-nn.txt", ['NULL']))

    # iterate over the test cases
    it = 0
    for t in tests[0:]: # passed 50 (56_4000)
        m = traveling_salesman_nn()

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
