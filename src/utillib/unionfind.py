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
            self.rank = 0
            self.parent = None
            self.id = id

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
            done = p is None or p == i
            if not done:
                i = p
            elif p == 1:
                e.parent = None


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

if __name__ == "__main__":
    main()


