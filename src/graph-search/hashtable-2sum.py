#
# Author: Daniel Dittenhafer
#
#     Created: May 9, 2019
#
# Description: Coursera Algorithms Graph Search and Data Structures
#
__author__ = 'Daniel Dittenhafer'
import collections
import graph
import heapq
import itertools
import myheap
import os
import sys
from timeit import default_timer as timer
"""
The goal of this problem is to implement a variant of the 2-SUM algorithm 
covered in this week's lectures.

The file contains 1 million integers, both positive and negative (there 
might be some repetitions!).This is your array of integers, with the ith
 row of the file specifying the ith entry of the array.

Your task is to compute the number of target values t in the interval 
[-10000,10000] (inclusive) such that there are distinct numbers x,y 
in the input file that satisfy x+y=t. (NOTE: ensuring distinctness 
requires a one-line addition to the algorithm from lecture.)
"""

class two_sum:

    def __init__(self):
        pass

    def run(self, data, verbose = False):
        sdata = sorted(set(data))
        found = {}
        cnt = 0

        for x in sdata:

            lower = -10000 - x
            upper =  10000  - x

            unx = self.find(sdata, upper) + 1
            lnx = self.find(sdata, lower)
            ss = sdata[lnx:unx]

            for y in ss:
                # do something...
                if lower <= y and y <= upper:
                    t = x + y
                    if found.has_key(t):
                        pass
                    else:
                        cnt += 1
                        found[t] = "{0} + {1}".format(x, y)

        return cnt, found

    def load_hash_table(self, data):
        ht = {}
        for d in data:
            ht[d] = 1

        return ht

    def find(self, a, v):
        
        lower = 0
        upper = len(a)
        mid = len(a) / 2
        done = False

        while not done:
            t = a[mid]
            if t == v:
                done = True
            elif t < v:
                lower = mid
                newmid = lower + (upper - lower) / 2
            elif t > v:
                upper = mid
                newmid = lower + (upper - lower) / 2  

            if newmid == mid:
                done = True
            else:
                mid = newmid

        return mid
        

def load_int_array(path):
    arr = []
    with open(path) as fp:
        lines = fp.read().split("\n")
        for l in lines:
            if len(l) > 0:
                arr.append(int(l))

    return arr

def load_stanford_algs_test_cases(tests, test_cases_folder):
    
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

        tests.append((test_cases_folder + "\\" + filename, output))


def main():

    tests_correct = 0
    tests = [
        # path to graph file, finishing times dict, leaders dict
        #("D:\\Code\\Python\\py-sandbox\\data\\graph-small2-dijkstra.txt", [1,2,3,4,5,6,7], {}, [0,5,3,4,5,6,6])
    ]

    load_test_cases = False
    if load_test_cases:
        load_stanford_algs_test_cases(tests, "D:\\Code\\other\\stanford-algs\\testcases\\course2\\assignment4TwoSum")

    # The real problem
    tests.append(("D:\\Code\\Python\\py-sandbox\\data\\graph-algo1-programming_prob-2sum.txt", []))

    # iterate over the test cases
    for t in tests:
        # load the graph (while timing it)
        start = timer()
        data = load_int_array(t[0])
        end = timer()
        print "loaded {0} in {1} secs".format(t[0], end - start)

        start = timer()
        s = two_sum()
        res, found = s.run(data, verbose=False)
        end = timer()
        print "twosum of {0} in {1} secs = {2}/sec".format(len(data), end - start, len(data) / (end - start))
        print res

        expected = t[1]
        ok = len(expected) == 0 or res == expected[0] 
        if not ok:
            print "ERROR! Expected {0}".format(expected[0])
            c = collections.defaultdict(int)
            for k in found:
                c[k] += 1
                c[found[k]] += 1
                
            
            for k in c:
                print "{0}: {1}".format(k, c[k])

            print ""

            
        else:
            print "OK"
            tests_correct += 1
    
    print "{0} of {1} tests passed".format(tests_correct, len(tests))


if __name__ == "__main__":
    main()