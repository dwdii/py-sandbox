#
# Author: Daniel Dittenhafer
#
#     Created: April 29, 2019
#
# Description: Coursera Algorithms Graph Search and Data Structures
#
__author__ = 'Daniel Dittenhafer'
import graph
import collections
import os
import sys
from timeit import default_timer as timer
from colorama import Fore, Back, Style 
"""
Your task is to run Dijkstra's shortest-path algorithm on this graph, using 1 
(the first vertex) as the source vertex, and to compute the shortest-path 
distances between 1 and every other vertex of the graph. If there is no path
between a vertex vv and vertex 1, we'll define the shortest-path distance 
between 1 and vv to be 1000000.

You should report the shortest-path distances to the following ten vertices, 
in order: 7,37,59,82,99,115,133,165,188,197. You should encode the distances 
as a comma-separated string of integers. So if you find that all ten of these 
vertices except 115 are at distance 1000 away from vertex 1 and 115 is 2000 
distance away, then your answer should be 1000,1000,1000,1000,1000,2000,1000,
1000,1000,1000. Remember the order of reporting DOES MATTER, and the string 
should be in the same order in which the above ten vertices are given. The 
string should not contain any spaces. Please type your answer in the space 
provided.
"""
import heapq

class dijkstra:

    def __init__(self):
        pass

    def run(self, g, s, verbose=False):
        h = []
        done = False
        infin = 1000000

        for n in g.vertices:
            dgs = infin
            if n == s:
                dgs = 0
            heapq.heappush(h, (dgs, n))

        while not done:
            wi = heapq.heappop(h)
            w = g.vertices[wi[1]]

            
            
            done = True
            pass





def load_stanford_algs_test_cases(tests):
    test_cases_folder = "D:\\Code\\other\\stanford-algs\\testcases\\course2\\assignment1SCC"
    for filename in os.listdir(test_cases_folder):
        if filename[:5] != 'input':
            continue

        outputfile = filename.replace("input_", "output_")
        with open(test_cases_folder + "\\" + outputfile) as fp:
            parts = fp.read().split(",")

        output = []
        for p in parts:
            op = int(p)
            if op > 0:
                output.append(op)

        tests.append((test_cases_folder + "\\" + filename, [],{}, output))


def main():

    tests = [
        # path to graph file, finishing times dict, leaders dict
        ("D:\Code\Python\py-sandbox\data\graphs-dijkstraData.txt", {}, {})
    ]

    load_test_cases = False
    if load_test_cases:
        load_stanford_algs_test_cases(tests)

    # iterate over the test cases
    for t in tests:
        # load the graph (while timing it)
        g = graph.graph()
        start = timer()
        g.load_data(t[0], verbose=True, delim='\t', directed=False, has_edge_weights=True)
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        s = dijkstra()
        s.run(g, 1, verbose=True)

        ok = len(t[1]) == 0 or (t[1] == s.f)
        ok &= len(t[1]) == 0 or t[2] == s.leaders
        if not ok:
            if len(s.f) < 100:
                print s.f
                print s.leaders
            print "ERROR!"
        else:
            print "OK"

        print s.counts
        res = sorted(s.counts.values(), reverse=True)[0:5]
        print res
        if res == t[3]:
            print "GOOD!"
        elif res == [434821, 968, 459, 314, 211]:
            print "NOPE"
        else:
            print "NOPE"

    
if __name__ == "__main__":
    main()