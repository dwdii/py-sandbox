#
# Author: Daniel Dittenhafer
#
#     Created: April 29, 2019
#
# Description: Coursera Algorithms Graph Search and Data Structures
#
__author__ = 'Daniel Dittenhafer'
import collections
import graph
import myheap
import itertools
import os
import sys
from timeit import default_timer as timer
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
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count

    def run(self, g, s, verbose=False):
        h = myheap.heapqplus()
        X = {} # vertices processed so far
        A = {} # shortest paths
        B = {}
        done = False
        infin = 1000000

        """for n in g.vertices:
            dgs = infin
            if n == s:
                dgs = 0
            heapq.heappush(h, (dgs, n))"""

        # distance to source is zero
        A[s] = 0 
        X[s] = None
        B[s] = [1]
        for n in g.vertices:
            if n != s:
                A[n] = infin
                
            h.add(n, priority=A[n])

        # Populate heap with current estimates for source's neighbors
        #for e in g.vertices[s].edges:
        #    dgs = A[s] + e.weight
        #    h.add_if_priority_lower(e.head.id, priority=dgs)

        while not done:
            dgs, wi = h.pop()
            w = g.vertices[wi]

            # Store final shortest path value for w.id vertex
            A[w.id] = dgs
            X[w.id] = 1
            if verbose:
                if w.id in B:
                    print "{0} ({1}) => {2}".format(w.id, dgs, B[w.id])
                else:
                    print "{0} ({1}) => {2}".format(w.id, dgs, "***missing path***")


            # loop to 
            
            for e in w.edges:
                other_id = e.get_other_side(w.id)
                if ((e.tail.id == w.id and e.head.id in X) or 
                    (e.head.id == w.id and e.tail.id in X)):

                    if A[other_id] + e.weight < A[w.id]:
                        A[w.id] = A[other_id] + e.weight
                        B[w.id] = B[other_id][:]
                        B[w.id].append(w.id)

                    pass # Already determined this one
                else:
                    dgs = A[w.id] + e.weight
                    
                    if(h.add_if_priority_lower(other_id, priority=dgs)):
                        B[other_id] = B[w.id][:]
                        B[other_id].append(other_id)

            
            done = len(X) == len(g.vertices)

        return A, B



def load_stanford_algs_test_cases(tests, outndx):
    test_cases_folder = "D:\\Code\\other\\stanford-algs\\testcases\\course2\\assignment2Dijkstra"
    for filename in os.listdir(test_cases_folder):
        if filename[:5] != 'input':
            continue

        outputfile = filename.replace("input_", "output_")
        with open(test_cases_folder + "\\" + outputfile) as fp:
            expected_out = fp.read().split(",")

        output = []
        for p in expected_out:
            op = int(p)
            if op > 0:
                output.append(op)

        tests.append((test_cases_folder + "\\" + filename, outndx,{}, output))


def main():

    tests_correct = 0
    tests = [
        # path to graph file, finishing times dict, leaders dict
        #("D:\Code\Python\py-sandbox\data\graphs-dijkstraData.txt", [7,37,59,82,99,115,133,165,188,197], {}, [])
        #("D:\\Code\\Python\\py-sandbox\\data\\graph-small-dijkstra.txt", [1,2,3,4], {}, [0,3,2,7]),
        ("D:\\Code\\Python\\py-sandbox\\data\\graph-small2-dijkstra.txt", [1,2,3,4,5,6,7], {}, [0,5,3,4,5,6,6])
    ]

    load_test_cases = True
    if load_test_cases:
        load_stanford_algs_test_cases(tests, [7,37,59,82,99,115,133,165,188,197])

    # The real problem
    tests.append(("D:\Code\Python\py-sandbox\data\graphs-dijkstraData.txt", [7,37,59,82,99,115,133,165,188,197], {}, [2599,2610,2947,2052,2367,2399,2029,2442,2505,3068]))

    # iterate over the test cases
    for t in tests:
        # load the graph (while timing it)
        g = graph.graph()
        start = timer()
        g.load_data(t[0], verbose=True, delim='\t', directed=False, has_edge_weights=True)
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        s = dijkstra()
        A, B = s.run(g, 1, verbose=True)

        res = ""
        outNdx = t[1]
        output = []
        for i in outNdx:
            if len(A) >= i:
                if len(res) > 0:
                    res += ","
                res += "{0}".format(A[i])
                output.append(A[i])

        print res
        ok = output == t[3] #not res == "13374,2610,6094,10341,6765,16786,2029,2442,2505,9831"
        #ok |= not res == ""
        if not ok:
            print "ERROR!"
            c = 0
            for i in xrange(len(output)):
                if len(t[3]) > i and output[i] == t[3][i]:
                    c += 1
            print "{0} of {1}".format(c, len(output))

        else:
            print "OK"
            tests_correct += 1
    
    print "{0} of {1} tests passed".format(tests_correct, len(tests))
if __name__ == "__main__":
    main()