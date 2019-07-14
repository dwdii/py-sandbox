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

loaded D:\Code\Python\py-sandbox\data\2sat1.txt in 189.184909484 secs at 2019-07-13 09:43:57
Clauses: 7
Vars: 8
[0] satisfied = True in 0.191360947569 secs = 36.5800864227/sec
True
OK

loading D:\Code\Python\py-sandbox\data\2sat2.txt started at 2019-07-13 10:27:53
Original Clauses: 200000
loaded D:\Code\Python\py-sandbox\data\2sat2.txt in 841.01747567 secs at 2019-07-13 10:27:53
Clauses: 58
Vars: 56
[0] satisfied = False in 3.9025398202 secs = 14.8621161275/sec
False
OK

loading D:\Code\Python\py-sandbox\data\2sat3.txt started at 2019-07-13 11:58:02
Original Clauses: 400000
loaded D:\Code\Python\py-sandbox\data\2sat3.txt in 3678.22998486 secs at 2019-07-13 11:58:02
Clauses: 296
Vars: 290
[0] satisfied = True in 3.55349344117 secs = 83.2983104936/sec
True
OK

loading D:\Code\Python\py-sandbox\data\2sat4.txt started at 2019-07-13 15:15:57
Original Clauses: 600000
loaded D:\Code\Python\py-sandbox\data\2sat4.txt in 8686.8853016 secs at 2019-07-13 15:15:57
Clauses: 12
Vars: 13
[0] satisfied = True in 5.42684793774 secs = 2.21122834796/sec
True
OK
"""

class papadimitrious :

    def __init__(self):
        self.infinity = 18446744073709551615
        self.bits = []

    def run(self, n, P, mi, verbose=False):

        print "Clauses: {0}".format(len(P))
        print "Vars: {0}".format(n)

        if len(P) == 0:
            return True

        bitlist = [1, 3]
        log2N = int(math.log(n, 2))
        twoN2 = long(2 * math.pow(n, 2))
        for i in xrange(log2N):
            # create a random starting point
            num = random.getrandbits(mi)
            self._bits = [True if num & (1 << (mi-1-b)) else False for b in range(mi)]

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

    def is_clause_satisfied_ex(self, clause):
        return clause[4](clause)

    def is_satisfied(self, P):

        is_sat = True
        unsats = []
        i = 0
        for i in xrange(len(P)):
            ics = self.is_clause_satisfied_ex(P[i])
            is_sat = is_sat and ics
            if not ics:
                unsats.append(i)


        return is_sat, unsats

    def not_x_or_y(self, clause):
        return not self._bits[clause[1]] or self._bits[clause[3]]

    def x_or_not_y(self, clause):
        return self._bits[clause[1]] or not self._bits[clause[3]]

    def not_x_or_not_y(self, clause):
        return not self._bits[clause[1]] or not self._bits[clause[3]]

    def x_or_y(self, clause):
        return self._bits[clause[1]] or self._bits[clause[3]]

    def load_data(self, f, compute_distances = False):
        """Loads the graph from the file f.

        Returns:
            P list of clauses (x_n,y_m) tuples where negative values mean "not"
        """
        P = []
        with open(f) as fp:
            lines = fp.read().split("\n")
            c = int(lines[0])
            print "Original Clauses: {0}".format(c)
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

                    P.append( [n1, abs(p1) - 1, n2, abs(p2) - 1] )

        i = len(P) + 1
        while i > len(P):
            i = len(P)
            P = reduce_problem(P)

        v = set()
        for p in P:
            # Count unique vars
            v.add(p[1])
            v.add(p[3])
            # and append eval function pointer
            fn = None
            if p[0] and p[2]:
                # not not
                fn = self.not_x_or_not_y
            elif p[0] and not p[2]:
                fn = self.not_x_or_y
            elif not p[0] and p[2]:
                fn = self.x_or_not_y
            else:
                fn = self.x_or_y

            p.append(fn)

        return len(v), P, c

def reduce_problem(P):

    notX = set()
    X = set()
    for p in P:
        if p[0]:
            notX.add(p[1])
        else:
            X.add(p[1])

        if p[2]:
            notX.add(p[3])
        else:
            X.add(p[3])

    symDif = X.symmetric_difference(notX)

    for i in xrange(len(P) - 1, 0, -1):
        p = P[i]
        if p[1] in symDif:
            P.remove(p)

        if p[3] in symDif and p in P:
            P.remove(p)

        if i == 0:
            break

    return P

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

    load_test_cases = False
    tests_correct = 0
    if load_test_cases:
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course4\\assignment4TwoSat")

    # The real problem
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat1.txt", [True]))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat2.txt", [False]))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat3.txt", [True]))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat4.txt", [True]))
    tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat5.txt", []))
    #tests.append(("D:\\Code\\Python\\py-sandbox\\data\\2sat6.txt", []))

    # iterate over the test cases
    it = 0
    for t in tests[it:]:
        m = papadimitrious()

        # load the graph data (while timing it)
        start = timer()
        ts = time.time()
        print "loading {0} started at {1}".format(t[0], datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        c, P, mi = m.load_data(t[0])
        end = timer()
        print "loaded {0} in {1} secs at {2}".format(t[0], end - start, datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

        start = timer()
        res = m.run(c, P, mi, True)
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
