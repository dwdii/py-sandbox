from __future__ import division
#
# Author: Daniel Dittenhafer
#
#     Created: May 20, 2019
#
# Description: Coursera Algorithms Greedy Algos, MST and Dynamic Programming
#
__author__ = 'Daniel Dittenhafer'
#import collections
#import copy
#import heapq
#import itertools
import os
#import sys
from timeit import default_timer as timer
from src.utillib.unionfind import union_find
from src.utillib.graph import graph, edge
#from bitarray import bitarray
"""
The distance between two nodes u and v in this problem is defined as the
Hamming distance--- the number of differing bits --- between the two nodes'
labels. For example, the Hamming distance between the 24-bit label of node
#2 above and the label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is
3 (since they differ in the 3rd, 7th, and 21st bits).

The question is: what is the largest value of k such that there is a
k-clustering with spacing at least 3? That is, how many clusters are needed to
ensure that no pair of nodes with all but 2 bits in common get split into
different clusters?

NOTE: The graph implicitly defined by the data file is so big that you probably
can't write it out explicitly, let alone sort the edges by cost. So you will
have to be a little creative to complete this part of the question. For
example, is there some way you can identify the smallest distances without
explicitly looking at every pair of nodes?
"""

class greedy_clustering_hamming:

    def __init__(self):
        pass

    def run(self, g, min_spacing = 3, verbose = True):
        uf = union_find(g.vertices.keys())

        # first need to compute the edge costs for all vertices...
        start = timer()
        gvi = g.vertices.items()
        lgv = len(g.vertices)
        for v1 in xrange(lgv):
            vo1 = gvi[v1][1]
            for v2 in xrange(v1, lgv):
                vo2 = gvi[v2][1]
                weight = self.hamming_distance_bitwise(vo1.tag, vo2.tag)
                if weight > min_spacing:
                    continue

                e = edge(vo1, vo2, weight)
                g.edges.append(e)
                #vo1.edges.append(e)
                #vo2.edges.append(e)
        end = timer()
        if verbose:
            print "edges created in {0} secs".format(end - start)

        # then sort ascending
        g.edges.sort(key=lambda x: x.weight)

        # does everything else just work?
        T = []
        for i in xrange(len(g.edges)):
            e = g.edges[i]
            c1 = uf.find(e[0].id)
            c2 = uf.find(e[1].id)

            if c1.id != c2.id:
                # not a cycle
                #
                # if check if we are get max cluster count
                if e.weight >= min_spacing:
                    # yes, break
                    break
                else:
                    # other wise merge and proceed
                    #T.append(e)
                    uf.union(c1.id, c2.id)

        # next
        eNext = g.edges[i]
        max_spacing = eNext.weight

        return max_spacing, uf

    def hamming_distance(self, s1, s2):
        """
        https://pythonadventures.wordpress.com/2010/10/19/hamming-distance/
        """
        #assert len(s1) == len(s2)
        return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

    def hamming_distance_bitwise(self, s1, s2):
        """
        Bitwise version
        """
        #assert len(s1) == len(s2)
        return sum(s1 ^ s2)

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
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course3\\assignment2Clustering\\question2")



    # The real problem
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\greedy_clustering_big.txt", [106]))

    # iterate over the test cases
    for t in tests:
        # load the graph data (while timing it)
        start = timer()
        g = graph()
        g.load_data3(t[0], verbose=True, delim=" ")
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        m = greedy_clustering_hamming()
        #hdb = m.hamming_distance_bitwise(bitarray("1010"), bitarray("1001"))

        start = timer()
        ms, cl = m.run(g, 3)
        res = cl.clusters
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

    print "{0} of {1} tests passed = {2}%".format(tests_correct, len(tests), (tests_correct / (len(tests))) * 100)


if __name__ == "__main__":
    main()
