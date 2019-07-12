from __future__ import division
#
# Author: Daniel Dittenhafer
#
#     Created: July 9, 2019
#
# Description: Coursera Algorithms Shortest Paths, NP Complete, etc.
#
__author__ = 'Daniel Dittenhafer'
import collections
import copy
import datetime
import decimal
#import src.utillib.myheap
import itertools
import math
import multiprocessing
import os
import random
import sys
import time
from timeit import default_timer as timer
"""
The file format is as follows. In each instance, the number of variables and
the number of clauses is the same, and this number is specified on the first
 line of the file. Each subsequent line specifies a clause via its two
 literals, with a number denoting the variable and a "-" sign denoting logical
 "not". For example, the second line of the first data file is "-16808 75250",
 which indicates the clause x_16808 V x_75250.

Your task is to determine which of the 6 instances are satisfiable, and which
are unsatisfiable. In the box below, enter a 6-bit string, where the ith bit
should be 1 if the ith instance is satisfiable, and 0 otherwise. For example,
if you think that the first 3 instances are satisfiable and the last 3 are not,
then you should enter the string 111000 in the box below.
"""

class papadimitrious :

    def __init__(self):
        self.infinity = 18446744073709551615
        self.bits = []

    def run(self, n, P, verbose=False):

        nminus1 = n - 1
        bitlist = [1, 3]
        log2N = int(math.log(n, 2))
        twoN2 = long(2 * math.pow(n, 2))
        for i in xrange(log2N):
            # create a random starting point
            num = random.getrandbits(n)
            self._bits = [True if num & (1 << (n-1-b)) else False for b in range(n)]

            # iterate from the random starting point
            for j in self.custom_range(twoN2):
                is_sat, unsats = self.is_satisfied(P)
                if is_sat:
                    return True
                else:
                    # pick a clause to make true
                    cmt = random.sample(unsats, 1)[0]

                    clause = P[cmt]
                    ntf = random.sample(bitlist,1)[0]
                    self._bits[clause[ntf]] = not self._bits[clause[ntf]]

        return False

    def custom_range(self, start=0,stop=None,step=1):
        """xrange in python 2.7 fails on numbers larger than C longs.
        we write a custom version
        https://stackoverflow.com/a/20008924/2604144
        """
        if stop is None:
            #handle single argument case. ugly...
            stop = start
            start = 0
        i = start
        while i < stop:
            yield i
            i += step

    def is_clause_satisfied(self, clause):
        ndx1 = clause[1]# - 1
        ndx2 = clause[3]# - 1
        if clause[0]:
            # not
            x1 = not self._bits[ndx1]
        else:
            x1 = self._bits[ndx1]

        if clause[2]:
            # not
            x2 = not self._bits[ndx2]
        else:
            x2 = self._bits[ndx2]

        return x1 or x2


    def is_satisfied(self, P):

        is_sat = True
        unsats = []
        i = 0
        for i in xrange(len(P)):
            ics = self.is_clause_satisfied(P[i])
            is_sat = is_sat and ics
            if not ics:
                unsats.append(i)


        return is_sat, unsats


    def load_data(self, f, compute_distances = False):
        """Loads the graph from the file f.

        Returns:
            P list of clauses (x_n,y_m) tuples where negative values mean "not"
        """
        P = []
        with open(f) as fp:
            lines = fp.read().split("\n")
            c = int(lines[0])
            for line in lines[1:]:
                if(len(line.strip()) > 0):
                    parts = line.split(" ")
                    p1 = int(parts[0])
                    n1 = False
                    if p1 < 0:
                        n1 = True
                    p2 = int(parts[1])
                    n2 = False
                    if p2 < 0:
                        n2 = True

                    P.append( (n1, abs(p1) - 1, n2, abs(p2) - 1 ) )

        return c, P

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
                output.append(p == '1')

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
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course4\\assignment4TwoSat")

    # The real problem
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat1.txt", []))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat2.txt", []))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat3.txt", []))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat4.txt", []))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat5.txt", []))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat6.txt", []))

    # iterate over the test cases
    it = 0
    for t in tests[it:]:
        m = papadimitrious()

        # load the graph data (while timing it)
        start = timer()
        ts = time.time()
        c, P = m.load_data(t[0])
        end = timer()
        print "loaded {0} in {1} secs at {2}".format(t[0], end - start, datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

        start = timer()
        res = m.run(c, P, True)
        end = timer()

        print "[{3}] satisfied = {0} in {1} secs = {2}/sec".format(res, end - start, len(P) / (end - start), it)
        print res
        if res is None:
            res = "NULL"

        expected = t[1]
        ok = len(expected) == 0 or (str(res) == str(expected[0]))
        if not ok:
            print "ERROR! Expected {0}".format(expected[0])
        else:
            print "OK"
            tests_correct += 1

        it += 1

    print "{0} of {1} tests passed = {2}%".format(tests_correct, len(tests), (tests_correct / (len(tests))) * 100)


if __name__ == "__main__":
    main()
