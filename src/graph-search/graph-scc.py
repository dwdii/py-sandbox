#
# Author: Daniel Dittenhafer
#
#     Created: April 22, 2019
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
Your task is to code up the algorithm from the video lectures for computing
strongly connected components (SCCs), and to run this algorithm on the given 
graph.

Output Format: You should output the sizes of the 5 largest SCCs in the given 
graph, in decreasing order of sizes, separated by commas (avoid any spaces). 
So if your algorithm computes the sizes of the five largest SCCs to be 500, 
400, 300, 200 and 100, then your answer should be "500,400,300,200,100" 
(without the quotes). If your algorithm finds less than 5 SCCs, then write 0 
for the remaining terms. Thus, if your algorithm computes only 3 SCCs whose 
sizes are 400, 300, and 100, then your answer should be "400,300,100,0,0" 
(without the quotes). (Note also that your answer should not have any spaces in
it.)
"""

class scc:

    def __init__(self):
        self.reset()

    def reset(self):
        self.t = 0
        self.f = []
        self.leaders = {}

    def scc_explore(self, g, verbose=False):

        self.reset()

        g.reset_explored()
        self.dfs_loop(g)
        if verbose:
            print "finishing times: " + str(self.f)

        g.reset_explored()
        self.dfs_loop2(g)
        if verbose:
            print "leaders: " + str(self.leaders)

        self.counts = collections.defaultdict(int)
        for k in self.leaders:
            self.counts[self.leaders[k]] += 1

    def dfs_loop(self, g):

        self.t = 0

        for i in xrange(len(g.vertices), 0, -1):
            if i % 100 == 0:
                print "dfs_loop[{0}]".format(i)

            if g.vertices.has_key(i) and not g.vertices[i].explored:
                #s = i
                self.dfs_reverse(g, i)

    def dfs_loop2(self, g):

        self.s = None

        for k in reversed(self.f):
            i = k[0]
            if not g.vertices[i].explored:
                self.s = i
                self.dfs(g, i)


    def dfs(self, g, i):
        """Walk the graph forward order for second pass of Kosaraju using iterative approach"""

        dfs_stack = [i]

        while dfs_stack:
            j = dfs_stack.pop()

            g.vertices[j].explored = True
            self.leaders[j] = self.s

            for e in g.vertices[j].edges:
                if not e[1].explored:
                    dfs_stack.append(e[1].id)


    def dfs_reverse(self, g, i):
        """Walk the graph in edge reverse order for the first pass of Kosaraju using iterative approach"""

        dfs_stack = [(i,0)]

        while dfs_stack:
            j = dfs_stack.pop()

            if j[1] is None:
                self.t += 1
                self.f.append((j[0], self.t))
            else:
                g.vertices[j[0]].explored = True

                dfs_stack.append((j[0], None))
                for e in reversed(g.vertices[j[0]].incoming):
                    if not e[0].explored:
                        dfs_stack.append((e[0].id, e[1].id))

def main():

    tests = [
        # path to graph file, finishing times dict, leaders dict
        #("D:\Code\Python\py-sandbox\data\graph-small-SCC.txt", {1: 7, 2: 3, 3: 1, 4: 8, 5: 2, 6: 5, 7: 9, 8: 4, 9: 6}, {1: 7, 2: 8, 3: 3, 4: 7, 5: 8, 6: 3, 7: 7, 8: 8, 9: 3})
        #("D:\\Code\\Python\\py-sandbox\\data\\graph-small-SCC.txt", [(3, 1), (5, 2), (2, 3), (8, 4), (6, 5), (9, 6), (1, 7), (4, 8), (7, 9)], {1: 7, 2: 8, 3: 9, 4: 7, 5: 8, 6: 9, 7: 7, 8: 8, 9: 9}, [3,3,3])
        #,("D:\\Code\\Python\\py-sandbox\\data\\graph-small2-SCC.txt", [(3, 1), (1, 2), (2, 3), (6, 4), (7, 5), (8, 6), (4, 7), (5, 8)],{1: 2, 2: 2, 3: 2, 4: 5, 5: 5, 6: 8, 7: 8, 8: 8}, [3,3,2])
        #,("D:\\Code\\Python\\py-sandbox\\data\\graph-small3-SCC.txt", [(6, 1), (7, 2), (8, 3), (5, 4), (1, 5), (2, 6), (3, 7), (4, 8)],{1: 3, 2: 3, 3: 3, 4: 4, 5: 5, 6: 8, 7: 8, 8: 8}, [3,3,1,1])
        #,("D:\\Code\\Python\\py-sandbox\\data\\graph-small4-SCC.txt", [],{}, [7,1])
        #,("D:\\Code\\Python\\py-sandbox\\data\\graph-small5-SCC.txt", [],{}, [6,3,2,1])
        #("D:\\Code\\Python\\py-sandbox\\data\\graph-small6-scc.txt", [],{}, [11,10,5,4])
        ("D:\\Code\\Python\\py-sandbox\\data\\graphs-SCC.txt", {}, {}, [434821, 968, 459, 313, 211])
    ]

    load_test_cases = False
    if load_test_cases:
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


    print "Old recurse list: {0}".format(sys.getrecursionlimit())
    sys.setrecursionlimit(1000)
    print "New recurse list: {0}".format(sys.getrecursionlimit())

    for t in tests:

        g = graph.graph()
        start = timer()
        g.load_data(t[0], verbose=True, delim=' ', directed=True)
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        s = scc()
        s.scc_explore(g, verbose=False)

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