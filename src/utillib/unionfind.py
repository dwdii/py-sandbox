#
# Author: Daniel Dittenhafer
#
#     Created: May 21, 2019
#
# Description: Coursera Algorithms
#
__author__ = 'Daniel Dittenhafer'
import random
"""
Union-Find Data Structure
"""

class union_find:

    class entry:
        def __init__(self, id):
            self._rank = 0
            self._parent = None
            self._id = id

        @property
        def rank(self):
            return self._rank

        @rank.setter
        def rank(self, r):
            self._rank = r

        @property
        def parent(self):
            return self._parent

        @parent.setter
        def parent(self, p):
            self._parent = p

        @property
        def id(self):
            return self._id

        def __repr__(self):
            return "entry[{0}]: r={1}; p={2}".format(self.id, self.rank, self.parent)

    def __init__(self, keys):
        self.data = {}
        self.clusters = len(keys)

        for k in keys:
            self.data[k] = self.entry(k)

    def find(self, x):

        i = x
        done =  False
        while not done:

            if self.data.has_key(i):
                e = self.data[i]

            p = e.parent
            done = p is None
            if not done:
                i = p


        return e

    def union(self, x, y ):

        s1 = self.find(x)
        s2 = self.find(y)

        if s2.rank > s1.rank:
            s1.parent = s2.id
        elif s1.rank > s2.rank:
            s2.parent = s1.id
        else:
            s2.parent = s1.id
            s1.rank += 1

        self.clusters -= 1

def main():

    tests_correct = 0
    tests = [
        # path to graph file, finishing times dict, leaders dict
        #("D:\\Code\\Python\\py-sandbox\\data\\graph-small2-dijkstra.txt", [1,2,3,4,5,6,7], {}, [0,5,3,4,5,6,6])
    ]

    uf = union_find([1,2,3,4,5,6,7,8,9,0])

    uf.find(1)

    uf.union(1,2)
    uf.union(7,8)
    uf.union(5,6)
    uf.union(3,4)
    uf.union(1,5)



    # iterate over the test cases
    for t in tests:
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


