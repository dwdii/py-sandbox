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
In this programming problem you'll code up the dynamic programming algorithm
for computing a maximum-weight independent set of a path graph.

The data file describes the weights of the vertices in a path graph (with the
weights listed in the order in which vertices appear in the path). It has the
following format:

[number_of_vertices]

[weight of first vertex]

[weight of second vertex]

...

For example, the third line of the file is "6395702," indicating that the
weight of the second vertex of the graph is 6395702.

Your task in this problem is to run the dynamic programming algorithm (and the
reconstruction procedure) from lecture on this data set. The question is: of
the vertices 1, 2, 3, 4, 17, 117, 517, and 997, which ones belong to the
maximum-weight independent set? (By "vertex 1" we mean the first vertex of
the graph---there is no vertex 0.) In the box below, enter a 8-bit string,
where the ith bit should be 1 if the ith of these 8 vertices is in the
maximum-weight independent set, and 0 otherwise. For example, if you think that
the vertices 1, 4, 17, and 517 are in the maximum-weight independent set and
the other four vertices are not, then you should enter the string 10011010 in
the box below.
"""

class max_weight_independent_set:

    def __init__(self):
        pass

    def run(self, verbose=False):

        # Initialize
        #
        # each tuple entry is:
        #  slot 0: max weight of sub problem including the i_th node
        #  slot 1: the case in which the i_th node subproblem lies.
        #
        A = []
        A.append( (0, 0) )
        A.append( (self._pathgraph[0][1], 1) )

        # Loop over all nodes in path, left to right
        for i in xrange(1, len(self._pathgraph)):
            # Get node i+1
            n = self._pathgraph[i]
            # Determine candidate mw value
            a2 = i - 1
            A2_Vn = A[a2][0] + n[1]
            # Get prior candidate mw
            a = i
            n_1 = A[a][0]
            # Compare to the prior
            if n_1 >= A2_Vn:
                A.append( (n_1, 0) )
            else:
                A.append( (A2_Vn, 1) )


        mwis = 0
        if(A[-1][0] >= A[-2][0]):
            mwis = A[-1][0]
            case = A[-1][1]
        else:
            mwis = A[-2][0]
            case = A[-2][1]

        S = {}
        for i in xrange(len(A) - 1 ,0, -1):
            if A[i][1] == 0 or (S.has_key(i+1) and S[i+1]): #A[i-1][0] >= A[i-2][0] + self._pathgraph[i-1][1]:
                # case 1
                S[i] = 0
            else:
                # case 2
                S[i] = 1

        return mwis,  S


    def load_data(self, path):

        self._pathgraph = []

        with open(path) as fp:
            lines = fp.read().split("\n")

            i = 0
            for line in lines[1:]:
                # Skip blank lines
                if len(line.strip()) > 0:

                    # Add to the array
                    i += 1
                    self._pathgraph.append( (i, int(line)) )

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

    load_test_cases = False
    tests_correct = 0
    if load_test_cases:
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course3\\assignment3HuffmanAndMWIS\\question3")

    # The real problem
    tests.append(("D:\\Code\\Python\\py-sandbox\\data\\dyn_mwis.txt", [10100110]))

    # iterate over the test cases
    for t in tests:
        m = max_weight_independent_set()

        # load the graph data (while timing it)
        start = timer()
        m.load_data(t[0])
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        start = timer()
        res, S = m.run(True)
        end = timer()

        # 1, 2, 3, 4, 17, 117, 517, and 997
        res2 = ""
        res2 += m.get_mwis_vertex(S, 1)
        res2 += m.get_mwis_vertex(S, 2)
        res2 += m.get_mwis_vertex(S, 3)
        res2 += m.get_mwis_vertex(S, 4)
        res2 += m.get_mwis_vertex(S, 17)
        res2 += m.get_mwis_vertex(S, 117)
        res2 += m.get_mwis_vertex(S, 517)
        res2 += m.get_mwis_vertex(S, 997)

        print "mwis weight {0}, bitcodes {3} in {1} secs = {2}/sec".format(res, end - start, len(m._pathgraph) / (end - start), res2)
        print res, res2
        #print tree

        expected = t[1]
        ok = len(expected) == 0 or (res2 == expected[0])
        if not ok:
            print "ERROR! Expected {0}".format(expected[0])
        else:
            print "OK"
            tests_correct += 1

    print "{0} of {1} tests passed = {2}%".format(tests_correct, len(tests), (tests_correct / (len(tests))) * 100)



if __name__ == "__main__":
    main()
