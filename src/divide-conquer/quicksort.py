#
# Author: Daniel Dittenhafer
#
#     Created: Mar 24, 2019
#
# Description: Coursera Algorithms Divide And Conquer Week 3
#
import math
__author__ = 'Daniel Dittenhafer'
"""
The file contains all of the integers between 1 and 10,000 (inclusive, with no repeats) in 
unsorted order. The integer in the ith row of the file gives you the ith entry of an input array.

Your task is to compute the total number of comparisons used to sort the given input file 
by QuickSort. As you know, the number of comparisons depends on which elements are chosen 
as pivots, so we'll ask you to explore three different pivoting rules.

You should not count comparisons one-by-one. Rather, when there is a recursive call on a 
subarray of length mmm, you should simply add m, minus, 1m-1m−1 to your running total of
comparisons. (This is because the pivot element is compared to each of the other m, minus, 
1m-1m−1 elements in the subarray in this recursive call.)

WARNING: The Partition subroutine can be implemented in several different ways, and different 
implementations can give you differing numbers of comparisons. For this problem, you should 
implement the Partition subroutine exactly as it is described in the video lectures 
(otherwise you might get the wrong answer).
"""
class quicksort:
    _comparison_count = 0
    _comparisons = []
    _pivotAlg = 0

    def __init__(self, pivotAlg):
        self._pivotAlg = pivotAlg

    def sort(self, data):
        # Reset the comparison counter
        self._comparison_count = 0
        del self._comparisons[:]
        # Recursively call partition
        ldata = len(data)
        self.partition(data, 0, ldata)
        
        return data

    def choosePivot(self, data, l, r):
        if self._pivotAlg == 0:
            return l
        elif self._pivotAlg == 1:
            return r - 1
        else:
            mndx = int(math.ceil((r - l - 1) / 2))
            fst = data[l]
            m = data[l + mndx]
            lst = data[r - 1]

            triple = [fst, m, lst]
            triple.sort()

            if triple[1] == m:
                return l + mndx
            elif triple[1] == fst:
                return l
            else:
                return r - 1

    def partition(self, data, l, r):
        if r - l <= 1:
            return
        else:
            # New Pivot and swap
            p = self.choosePivot(data, l, r)
            data[l], data[p] = data[p], data[l]

            # Increment comparison counte
            cm = r - l - 1
            self._comparison_count = self._comparison_count + (cm)
            self._comparisons.append(cm)

            # Pull pivot value out
            pv = data[l]
            # Initialize i
            i = l + 1
            # Loop
            for j in xrange(l + 1, r):
                if data[j] < pv:
                    data[i], data[j] = data[j], data[i]
                    i = i + 1

            data[l], data[i-1] = data[i-1], data[l]

            self.partition(data, l, i - 1)
            self.partition(data, i, r)

    @property
    def comparison_count(self):
        return self._comparison_count

    @property
    def comparisons(self):
        return self._comparisons

def load_data():
    qsdata = []
    with open("D:\Code\Python\py-sandbox\data\QuickSort.txt") as fp:
        lines = fp.read().split("\n")
        for l in lines:
            if len(l) > 0:
                qsdata.append(int(l))

    return qsdata

def check_result(qs, exp):
        print qs.comparison_count
        #print qs.comparisons
        if qs.comparison_count == exp:
            print "CORRECT!"
        else:
            print "WRONG!"


def main():

    tests = [
            ([3,8,2,5,1,4,7,6], 15, 0),
    ]


    for t in tests:
        qs = quicksort(0)
        qs.sort(t[0])
        #assert r == t[1]
        check_result(qs, t[1])

    qsdata = load_data()
    qs0 = quicksort(0)
    qs0.sort(qsdata)
    check_result(qs0, 162085)

    qsdata = load_data()
    qsL = quicksort(1)
    qsL.sort(qsdata)
    check_result(qsL, 164123)

    qsM = quicksort(2)

    qsM.sort([2, 20, 1, 15, 3, 11, 13, 6, 16, 10, 19, 5, 4, 9, 8, 14, 18, 17, 7, 12] )
    check_result(qsM, 55)
    print "Comparisons: " + str(qsM._comparisons) # show the comparison count
    print "Expected:    " + str([19,8,5,2,1,1,9,4,1,1,3,1]) # expected comps

    qsdata = load_data()
    qsM.sort(qsdata)
    check_result(qsM, 138382)

if __name__ == "__main__":
    main()