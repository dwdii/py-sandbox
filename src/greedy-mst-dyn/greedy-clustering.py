from __future__ import division
#
# Author: Daniel Dittenhafer
#
#     Created: May 20, 2019
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
from src.utillib.unionfind import union_find
from src.utillib.graph import graph
"""
There is one edge (i,j)(i,j) for each choice of 1≤i<j≤n, where nn is the number
of nodes.

For example, the third line of the file is "1 3 5250", indicating that the
distance between nodes 1 and 3 (equivalently, the cost of the edge (1,3))
is 5250. You can assume that distances are positive, but you should NOT assume
that they are distinct.

Your task in this problem is to run the clustering algorithm from lecture on
this data set, where the target number k of clusters is set to 4. What is the
maximum spacing of a 4-clustering?
"""

class greedy_clustering:

    def __init__(self):
        pass

    def run(self, g, k):
        uf = union_find(g.vertices.keys())
        se = g.edges.sort(key=lambda x: x.weight)

        T = []

        for i in g.edges:
            c1 = uf.find(i[0].id)
            c2 = uf.find(i[1].id)

            if c1.id != c2.id:
                # not a cycle
                T.append(i)
                uf.union(c1.id, c2.id)
                if uf.clusters == k:
                    break

        return -1




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

    load_test_cases = True
    tests_correct = 0
    if load_test_cases:
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course3\\assignment2Clustering\\question1")

    # The real problem
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\greedy_clustering1.txt", []))

    # iterate over the test cases
    for t in tests[10:11]:
        # load the graph data (while timing it)
        start = timer()
        g = graph()
        g.load_data2(t[0], verbose=True, delim=" ")
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        m = greedy_clustering()

        start = timer()
        res = m.run(g, 4)
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
