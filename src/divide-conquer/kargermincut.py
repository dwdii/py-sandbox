#
# Author: Daniel Dittenhafer
#
#     Created: Mar 24, 2019
#
# Description: Coursera Algorithms Divide And Conquer Week 3
#
__author__ = 'Daniel Dittenhafer'
import random
"""
The file contains the adjacency list representation of a simple undirected graph. 
There are 200 vertices labeled 1 to 200. The first column in the file represents 
the vertex label, and the particular row (other entries except the first column) 
tells all the vertices that the vertex is adjacent to. So for example, the 6th
row looks like : "6	155	56	52	120	......". This just means that the vertex with 
label 6 is adjacent to (i.e., shares an edge with) the vertices with labels 155,56,52,120,......,etc

Your task is to code up and run the randomized contraction algorithm for the min 
cut problem and use it on the above graph to compute the min cut. (HINT: Note 
that you'll have to figure out an implementation of edge contractions. Initially, 
you might want to do this naively, creating a new graph from the old every time 
there's an edge contraction. But you should also think about more efficient 
implementations.) (WARNING: As per the video lectures, please make sure to run the 
algorithm many times with different random seeds, and remember the smallest cut 
that you ever find.) Write your numeric answer in the space provided. So e.g., if 
your answer is 5, just type 5 in the space provided.
"""

class vertex:

    def __init__(self, id):
        self._id = id
        self._edges = []

    @property
    def edges(self):
        return self._edges
    
    @property
    def id(self):
        return self._id

    def __str__(self):
        return "vertex " + self.id

    def __repr__(self):
        return str(self)

class edge:

    def __init__(self, tail, head):
        self._vertices = []
        self._vertices.append(tail)
        self._vertices.append(head)

    def __getitem__(self, ndx):
        return self._vertices[ndx]

    @property
    def vertices(self):
        return self._vertices

    def changeVertex(self, fromV, toV):
        # if edge "left" vertex = "left"
        if self.vertices[0].id == fromV.id:
            # update to "right"
            self.vertices[0] = toV

        # if edge "right" vertex = "left"
        if self.vertices[1].id == fromV.id:
            self.vertices[1] = toV

    def __str__(self):
        return "({0},{1})".format(self.vertices[0].id, self.vertices[1].id)


class graph:

    #_adjacencyList = {}

    def __init__(self):
        self._edges = []
        self._nodes = {}
        pass

    @property
    def vertices(self):
        return self._nodes

    def load_data(self, path, verbose = False):
        if verbose:
            print "loading " + path

        with open(path) as fp:
            lines = fp.read().split("\n")
            for l in lines:
                if len(l.strip()) > 0:
                    parts = l.split('\t')
                    v = parts[0]
                
                    #if v not in self._adjacencyList:
                    #    self._adjacencyList[v] = {}

                    if v not in self._nodes:
                        self._nodes[v] = vertex(v)

                    for i in xrange(1, len(parts)):
                        h = parts[i]
                        if len(h.strip()) > 0:
                            #if h not in self._adjacencyList[v]:
                            #    self._adjacencyList[v][h] = 1
                            #    self._edges.append((v, h))

                            if h not in self._nodes:
                                self._nodes[h] = vertex(h)

                            # Look for existing edge to map
                            e = None
                            for eh in self._nodes[h].edges:
                                if ((eh.vertices[0].id == v and eh.vertices[1].id == h) or 
                                    (eh.vertices[0].id == h and eh.vertices[1].id == v)):
                                    e = eh
                                    break

                            # Otherwise, make a new edge
                            if e is not None:
                                # Already there
                                pass
                            else:
                                # Add new edge
                                e = edge(self._nodes[v], self._nodes[h])
                                self._nodes[v].edges.append(e)
                                self._nodes[h].edges.append(e)
                                self._edges.append(e)



    def kargerContraction(self, verbose = False):

        superA = set()
        superB = set()

        while len(self._nodes) > 2:
            endx = random.randint(0, len(self._edges) - 1)
            edge = self._edges[endx] # get edge to contract

            # For each edge in the "left" vertex,
            # contract into the "right" vertex
            tail = edge[0]
            head = edge[1]
            if len(superA) == 0 or tail.id in superA or head.id in superA:
                if ( ( tail.id in superA and head.id in superB) or
                     ( tail.id in superB and head.id in superA)):
                     superA = superA.union(superB)
                     superB.clear()

                superA.add(tail.id)
                superA.add(head.id)
            else:
                superB.add(tail.id)
                superB.add(head.id)

            if verbose:
                print "collapsing " + str(tail) + " into " + str(head)
                print "nodes in graph: " + str(len(self._nodes))

            for e in tail.edges:
                e.changeVertex(tail, head)

            head.edges.extend(tail.edges)

            # Remove the vertex and edges.
            if tail.id in self._nodes:
                del self._nodes[tail.id]

            # Remove the edge from the list
            del self._edges[endx]

            # Remove self loops
            i = 0
            while i < len(head.edges):
                e = head.edges[i]
                if not (e.vertices[0].id == head.id and e.vertices[1].id == head.id):
                    i += 1
                else:
                    del  head.edges[i]
                    if e in self._edges:
                        self._edges.remove(e)

        return self._nodes

def main():

    tests = [
        #("D:\Code\Python\py-sandbox\data\graph1.txt", 2),
        ("D:\Code\Python\py-sandbox\data\kargerMinCut.txt", 2)
    ]

    loopCount = 1000 #10000

    for t in tests:

        minOfMins = 100000
        for i in xrange(loopCount):
            g = graph()
            g.load_data(t[0])
            mc = g.kargerContraction(verbose=False)

            mcEdgeCount = len(mc[mc.keys()[0]].edges)
            print "loop: " + str(i)
            print "min cut: " + str(minOfMins)
            if mcEdgeCount < minOfMins:
                minOfMins = mcEdgeCount

        print "total loop: " + str(loopCount)
        print "final min cut: " + str(minOfMins)

        #g2 = graph()
        #g2.load_data(t[0])
        #for id in mc:
        #    v = g2.vertices[id]
        #    for e in v.edges:
        #        print e

    
if __name__ == "__main__":
    main()