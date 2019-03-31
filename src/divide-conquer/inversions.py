#
# Author: Daniel Dittenhafer
#
#     Created: Mar 24, 2019
#
# Description: Coursera Algorithms Divide And Conquer Week 2
#
__author__ = 'Daniel Dittenhafer'
"""
Your task is to compute the number of inversions in the file given, where the ith
row of the file indicates the ith entry of an array.
"""

# merge sort extension
def inversions(data):
    n = len(data)
    if n == 1:
        return data, 0
    else:
        nb = n / 2
        B, left = inversions(data[0:nb])
        C, right = inversions(data[nb:])
        D, splits = splitInvers(B, C, n)

    return D, left + right + splits

def splitInvers(B, C, n):
    D = []
    i = 0
    j = 0
    spInv = 0
    for k in xrange(n):
        if i < len(B) and j < len(C) and B[i] < C[j]:
            D.append(B[i])
            i = i + 1
        elif i < len(B) and j < len(C) and C[j] < B[i]:
            D.append(C[j])
            j = j + 1
            spInv = spInv + (len(B) - i)
        elif i < len(B):
            D.append(B[i])
            i = i + 1
        elif j < len(C):
            D.append(C[j])
            j = j + 1

    return D, spInv


def main():

    tests = [
            ([3,1,5,2,4,6], 4),
            ([1,3,5,2,4,6], 3)
    ]

    for t in tests:
        A, r = inversions(t[0])
        assert r == t[1]

    text = []
    with open("D:\Code\Python\py-sandbox\data\IntegerArray.txt") as fp:
        lines = fp.read().split("\n")
        for l in lines:
            if len(l) > 0:
                text.append(int(l))

    A, r = inversions(text)
    print r

    # Wrong: 2397819672
    # Correct: 2407905288 !!!


if __name__ == "__main__":
    main()