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
import itertools
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
        h = []
        X = {} # vertices processed so far
        A = {} # shortest paths
        done = False
        infin = 1000000

        """for n in g.vertices:
            dgs = infin
            if n == s:
                dgs = 0
            heapq.heappush(h, (dgs, n))"""

        A[s] = 0
        for e in g.vertices[s].edges:
            dgs = A[s] + e.weight
            self.heap_add(h, e.head.id, priority=dgs)

        while not done:
            dgs, wi = self.heap_pop(h)
            w = g.vertices[wi]

            # Store final shortest path value for w.id vertex
            A[w.id] = dgs

            # loop to 
            for e in w.edges:
                if ((e.tail.id == w.id and e.head.id in A) or 
                    (e.head.id == w.id and e.tail.id in A)):
                    pass # Already determined this one
                else:
                    dgs = A[w.id] + e.weight
                    self.heap_add(h, e.get_other_side(w.id), priority=dgs)

            
            done = len(A) == len(g.vertices)

        return A

    def heap_add(self, h, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.heap_remove(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(h, entry)

    def heap_remove(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def heap_pop(self, h):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while h:
            priority, count, task = heapq.heappop(h)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return priority, task
        raise KeyError('pop from an empty priority queue')


def load_stanford_algs_test_cases(tests):
    test_cases_folder = "D:\\Code\\other\\stanford-algs\\testcases\\course2\\assignment2Dijkstra"
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
        #("D:\Code\Python\py-sandbox\data\graphs-dijkstraData.txt", [], {}, [])
    ]

    load_test_cases = True
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
        A = s.run(g, 1, verbose=True)

        res = ""
        outNdx = [7,37,59,82,99,115,133,165,188,197]
        for i in outNdx:
            if len(res) > 0:
                res += ","
            res += "{0}".format(A[i])

        print res
        ok = res == t[3] #not res == "13374,2610,6094,10341,6765,16786,2029,2442,2505,9831"
        #ok |= not res == ""
        if not ok:
            print "ERROR!"
        else:
            print "OK"
    
if __name__ == "__main__":
    main()