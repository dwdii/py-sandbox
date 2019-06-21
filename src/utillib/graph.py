#
# Author: Daniel Dittenhafer
#
#     Created: April 22, 2019
#
# Description: Coursera Algorithms Graphs and Data Structures
#
__author__ = 'Daniel Dittenhafer'
from bitarray import bitarray
import random
"""
Graph, Edge and Vertex classes
"""

class vertex:

    def __init__(self, id):
        self._id = id
        self._edges = []
        self._explored = False
        self._incoming = []
        self._tag = None

    @property
    def edges(self):
        return self._edges

    @property
    def incoming(self):
        return self._incoming

    @property
    def id(self):
        return self._id

    @property
    def explored(self):
        return self._explored

    @explored.setter
    def explored(self, value):
        self._explored = value

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, v):
        self._tag = v

    def __str__(self):
        return "vertex " + str(self.id)

    def __repr__(self):
        return str(self)

    def get_edge(self, id):
        for e in self.edges:
            if e[0].id == id or e[1].id == id:
                return e

        return None

class edge:

    def __init__(self, tail, head, weight=1):
        self._vertices = []
        self._vertices.append(tail)
        self._vertices.append(head)
        self.head = head
        self.tail = tail
        self._weight = weight

    def __getitem__(self, ndx):
        return self._vertices[ndx]

    @property
    def weight(self):
        return self._weight

    @property
    def vertices(self):
        return self._vertices

    def get_other_side(self, vid):
        if self.head.id == vid:
            return self.tail.id
        else:
            return self.head.id

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

    def __repr__(self):
        return str(self)


class graph:

    #_adjacencyList = {}

    def __init__(self):
        self._edges = []
        self._nodes = {}
        pass

    @property
    def vertices(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges

    def reset_explored(self):
        for n in self._nodes:
            self._nodes[n].explored = False


    def load_data(self, path, verbose = False, delim='\t', directed=False, has_edge_weights=False, has_header=False):
        if verbose:
            print "loading " + path

        with open(path) as fp:
            lines = fp.read().split("\n")

            # We aren't using the header, so strip it off.
            # The header would have a vertices edges pair.
            if has_header:
                lines = lines[1:]

            for l in lines:

                if len(l.strip()) > 0:
                    parts = l.split(delim)
                    v = int(parts[0])

                    #if v not in self._adjacencyList:
                    #    self._adjacencyList[v] = {}

                    if v not in self._nodes:
                        self._nodes[v] = vertex(v)

                    for i in xrange(1, len(parts)):
                        h = parts[i]
                        if len(h.strip()) > 0:

                            if has_edge_weights:
                                hparts = h.split(",")
                                h = int(hparts[0])
                                weight = int(hparts[1])
                            else:
                                h = int(h)
                                weight = 1

                            #if h not in self._adjacencyList[v]:
                            #    self._adjacencyList[v][h] = 1
                            #    self._edges.append((v, h))

                            if h not in self._nodes:
                                self._nodes[h] = vertex(h)

                            # Look for existing edge to map
                            e = None
                            if not directed and not has_edge_weights:
                                # Only non-directed graphs have this need
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
                                e = edge(self._nodes[v], self._nodes[h], weight)
                                self._nodes[v].edges.append(e)
                                if not directed:
                                    self._nodes[h].edges.append(e)
                                else:
                                    self._nodes[h].incoming.append(e)

                                self._edges.append(e)

    def load_data2(self, path, verbose = False, delim='\t'):
        """
            Loads a file describing an undirected graph with integer edge costs, formated as:

            [number_of_nodes] [number_of_edges]
            [one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
            [one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
            ...
        """
        if verbose:
            print "loading " + path

        with open(path) as fp:
            lines = fp.read().split("\n")

            # We aren't using the header, so strip it off.
            # The header would have a vertices edges pair.
            lines = lines[1:]

            for l in lines:

                if len(l.strip()) > 0:
                    parts = l.split(delim)
                    v = int(parts[0])

                    #if v not in self._adjacencyList:
                    #    self._adjacencyList[v] = {}

                    if v not in self._nodes:
                        self._nodes[v] = vertex(v)

                    h = parts[1].strip()
                    if len(h) > 0:
                        h = int(h)
                        weight = int(parts[2])

                        #if h not in self._adjacencyList[v]:
                        #    self._adjacencyList[v][h] = 1
                        #    self._edges.append((v, h))

                        if h not in self._nodes:
                            self._nodes[h] = vertex(h)

                        # Add new edge
                        e = edge(self._nodes[v], self._nodes[h], weight)
                        self._nodes[v].edges.append(e)
                        self._nodes[h].edges.append(e)
                        self._edges.append(e)

    def load_data3(self, path, verbose = False, delim=" "):
        """
            Loads a file describing an undirected graph with Hamming distance edge costs, formated as:

                [# of nodes] [# of bits for each node's label]
                [first bit of node 1] ... [last bit of node 1]
                [first bit of node 2] ... [last bit of node 2]
                ...
        """
        if verbose:
            print "loading " + path

        with open(path) as fp:
            lines = fp.read().split("\n")

            # We aren't using the header, so strip it off.
            # The header would have a vertices edges pair.
            lines = lines[1:]

            v = 0
            for l in lines:
                if len(l.strip()) > 0:
                    v += 1

                    if v not in self._nodes:
                        vo = vertex(v)
                        vo.tag = bitarray(l.strip().replace(" ", ""))
                        self._nodes[v] = vo


    def load_data4(self, path, verbose = False, delim=' '):
        """
            Loads a file describing an directed graph with integer edge costs, formated as:

            [number_of_nodes] [number_of_edges]
            [tail_of_edge_1] [head_of_edge_1] [edge_1_cost]
            [tail_of_edge_2] [head_node_of_edge_2] [edge_2_cost]
            ...
        """
        if verbose:
            print "loading " + path

        with open(path) as fp:
            lines = fp.read().split("\n")

            # We aren't using the header, so strip it off.
            # The header would have a vertices edges pair.
            lines = lines[1:]

            for l in lines:

                if len(l.strip()) > 0:
                    parts = l.split(delim)
                    v = int(parts[0])

                    #if v not in self._adjacencyList:
                    #    self._adjacencyList[v] = {}

                    if v not in self._nodes:
                        self._nodes[v] = vertex(v)

                    h = parts[1].strip()
                    if len(h) > 0:
                        h = int(h)
                        weight = int(parts[2])

                        #if h not in self._adjacencyList[v]:
                        #    self._adjacencyList[v][h] = 1
                        #    self._edges.append((v, h))

                        if h not in self._nodes:
                            self._nodes[h] = vertex(h)

                        # Add new edge
                        e = edge(self._nodes[v], self._nodes[h], weight)
                        self._nodes[v].edges.append(e)
                        self._nodes[h].incoming.append(e)
                        self._edges.append(e)
