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
import itertools
import os
import sys
from timeit import default_timer as timer
from src.utillib.graph import graph, vertex, edge
#from src.utillib.myheap import heapqplus

"""
In this assignment you will implement one or more algorithms for the all-pairs
shortest-path problem. Here are data files describing three graphs:

g1.txt
g2.txt
g3.txt

The first line indicates the number of vertices and edges, respectively. Each
subsequent line describes an edge (the first two numbers are its tail and head,
respectively) and its length (the third number). NOTE: some of the edge lengths
are negative. NOTE: These graphs may or may not have negative-cost cycles.

Your task is to compute the "shortest shortest path". Precisely, you must first
identify which, if any, of the three graphs have no negative cycles. For each
such graph, you should compute all-pairs shortest paths and remember the
smallest one (i.e., compute minu,v∈Vd(u,v), where d(u,v)d(u,v) denotes the
shortest-path distance from uu to vv).

If each of the three graphs has a negative-cost cycle, then enter "NULL" in the
box below. If exactly one graph has no negative-cost cycles, then enter the
length of its shortest shortest path in the box below. If two or more of the
graphs have no negative-cost cycles, then enter the smallest of the lengths of
their shortest shortest paths in the box below.
"""

class bellman_ford:

    def __init__(self):
        self.infinity = 18446744073709551615
        pass

    def run(self, g, s, verbose=False):

        L = {}
        lenV = len(g.vertices)

        # Loop over i edge budget
        for i in xrange(lenV + 1):
            L[i] = {}

            # All vertices
            for id in g.vertices:
                v = g.vertices[id]
                if i == 0:
                    if v.id == s.id:
                        L[i][v.id] = 0
                    else:
                        L[i][v.id] = self.infinity
                else:
                    Lwv = []
                    Lim1 = L[i-1]
                    for ine in v.incoming:
                        wid = ine.get_other_side(v.id)
                        Lwv.append(Lim1[wid] + ine.weight)

                    # Always consider the prior edge budget shortest path
                    ch = [
                            Lim1[v.id]
                         ]

                    # and if there are other options, take the min of those
                    if 0 < len(Lwv):
                        ch.append(min(Lwv))

                    L[i][v.id] = min(ch)

        # check for negative cost cycle
        ncc = False
        for id in g.vertices:
            if L[lenV - 1][id] != L[lenV][id]:
                ncc = True
                break

        last = L[lenV - 1]
        if ncc:
            sp = None
        else:
            sp = min(last.values())

        return sp, last

    def add_ghost_vertex(self, g):
        s = vertex(max(g.vertices) + 1)
        g.vertices[s.id] = s
        for vid in g.vertices:
            v = g.vertices[vid]
            e = edge(s, v, 0)
            g.edges.append(e)
            s.edges.append(e)
            v.incoming.append(e)

        return s

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
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course4\\assignment1AllPairsShortestPath")

    # The real problem
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\shortest-g1.txt", []))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\shortest-g2.txt", []))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\shortest-g3.txt", []))

    # iterate over the test cases
    it = 0
    for t in tests:
        m = bellman_ford()

        # load the graph data (while timing it)
        start = timer()
        g = graph()
        g.load_data4(t[0])
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        # make ghost vertex and edges....
        s = m.add_ghost_vertex(g)

        start = timer()
        res, res2 = m.run(g, s, True)
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
