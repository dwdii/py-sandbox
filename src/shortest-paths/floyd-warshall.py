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
from src.utillib.myheap import heapqplus

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

class floyd_warshall:

    def __init__(self):
        pass
    
    def run(self, verbose=False):
        pass

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
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course4\\assignment1AllPairsShortestPath")

    # The real problem
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\shortest-g1.txt", []))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\shortest-g2.txt", []))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\shortest-g3.txt", []))

    # iterate over the test cases
    for t in tests:
        m = floyd_warshall()

        # load the graph data (while timing it)
        start = timer()
        m.load_data(t[0])
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)


        start = timer()
        res, res2, g = m.run(True)
        end = timer()

        print "huffman code max bits of {0} / min bits of {3} in {1} secs = {2}/sec".format(res, end - start, len(g.vertices) / (end - start), res2)
        print res, res2
        #print tree

        expected = t[1]
        ok = len(expected) == 0 or (res == expected[0] and res2 == expected[1])
        if not ok:
            print "ERROR! Expected {0}".format(expected[0])
        else:
            print "OK"
            tests_correct += 1

    print "{0} of {1} tests passed = {2}%".format(tests_correct, len(tests), (tests_correct / (len(tests))) * 100)


if __name__ == "__main__":
    main()
