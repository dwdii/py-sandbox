from __future__ import division
#
# Author: Daniel Dittenhafer
#
#     Created: May 28, 2019
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
Your task in this problem is to run the Huffman coding algorithm from
lecture on this data set. What is the maximum length of a codeword in
the resulting Huffman code?

The data file describes an instance of the problem. It has the following format:

[number_of_symbols]

[weight of symbol #1]

[weight of symbol #2]

For example, the third line of the file is "6852892," indicating that the
weight of the second symbol of the alphabet is 6852892. (We're using weights
instead of frequencies, like in the "A More Complex Example" video.)
"""

class huffman_coder:

    def __init__(self):
        pass

    def run(self, verbose=False):
        # First sort to get lowest weight (least frequent first)
        self._alphabet.sort(key=lambda a: a[1])
        g = graph()

        # create the n leaves
        roots = heapqplus()
        for a in self._alphabet:
            v = vertex(a[0])
            v.tag = a[1]
            roots.add(v, v.tag)
            g.vertices[v.id] = v

        i = 0
        while len(roots) > 1:
            _, v = roots.pop()
            _, v2 = roots.pop()
            nr = vertex(str(v.id) + '^' + str(v2.id))

            e0 = edge(v2, nr, 0)
            e1 = edge(v, nr, 1)

            v2.edges.append(e0)
            nr.edges.append(e0)

            v.edges.append(e1)
            nr.edges.append(e1)
            nr.tag = v.tag + v2.tag

            #roots.remove(v)
            #roots.remove(v2)
            roots.add(nr, nr.tag)

            #roots.sort(key=lambda a: a.tag)


        # Walk up from lowest to root to count depth
        # Need to do the same for highest weigth node also...
        lp = self._alphabet[0][0]
        n = g.vertices[lp]
        max_depth = self.get_depth(n)

        hp = self._alphabet[-1][0]
        n = g.vertices[hp]
        min_depth = self.get_depth(n)


        return max_depth, min_depth, g

    def get_depth(self, n):
        done = False
        depth = 0
        while not done:

            if len(n.edges) == 2:
                done = True
            else:
                for e in n.edges:
                    if e.head.tag > n.tag:
                        n = e.head
                        depth += 1
        return depth

    def load_data(self, path):

        self._alphabet = []

        with open(path) as fp:
            lines = fp.read().split("\n")

            i = 0
            for line in lines[1:]:
                # Skip blank lines
                if len(line.strip()) > 0:

                    # Add to the array
                    i += 1
                    self._alphabet.append( (i, int(line)) )




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
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course3\\assignment3HuffmanAndMWIS\\question1And2")

    # The real problem
    tests.append(("D:\\Code\\Python\\py-sandbox\\data\\dyn-huffman.txt", [19,9]))

    # iterate over the test cases
    for t in tests:
        m = huffman_coder()

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
