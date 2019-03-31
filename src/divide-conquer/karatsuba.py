#
# Author: Daniel Dittenhafer
#
#     Created: Mar 15, 2019
#
# Description: Coursera Algorithms Divide And Conquer Week 1
#
__author__ = 'Daniel Dittenhafer'

import math

""" 
In this programming assignment you will implement one or more of the integer multiplication 
algorithms described in lecture.

To get the most out of this assignment, your program should restrict itself to multiplying 
only pairs of single-digit numbers. You can implement the grade-school algorithm if you 
want, but to get the most out of the assignment you'll want to implement recursive integer
multiplication and/or Karatsuba's algorithm.

So: what's the product of the following two 64-digit numbers?

3141592653589793238462643383279502884197169399375105820974944592

2718281828459045235360287471352662497757247093699959574966967627

[Food for thought: the number of digits in each input number is a power of 2. Does this make 
your life easier? Does it depend on which algorithm you're implementing?]
"""

def karatsuba(snum1, snum2):

    lnum1 = len(snum1)
    lnum2 = len(snum2)
    if lnum1 < 10 or lnum2 < 10:
        return int(snum1) * int(snum2)

    m = min(lnum1, lnum2)
    #m2 = int(math.floor(m/2))
    m2 = m//2
    if (m % 2) != 0:
        m2 += 1    

    high1, low1 = snum1[0:m2], snum1[m2:]
    high2, low2 = snum2[0:m2], snum2[m2:]

    z0 = karatsuba(low1, low2)
    z2 = karatsuba(high1, high2)
    z1 = karatsuba(str(int(low1) + int(high1)), str(int(low2) + int(high2)))
    

    A = (z2 * int(pow(10, (m2*2))))
    B = ((z1 - z2 - z0) * int(pow(10, m2)))

    return A + B + z0

def main():
    tests = [
                ["10", "10", 100],
                ["5678", "1234", 7006652],
                ["2000", "2000", 4000000],
                ["20000000", "20000000", 400000000000000],
                ["9876", "6543", 64618668]
            ]
    
    for t in tests:
        r = karatsuba(t[0], t[1])
        assert r == t[2]
        if r == t[2]:
            print "{0} * {1} = {2} : OK".format(t[0], t[1], t[2])

    a = "3141592653589793238462643383279502884197169399375105820974944592"
    b = "2718281828459045235360287471352662497757247093699959574966967627"
    er = int(a) * int(b)
    r = karatsuba(a, b)
    print r
    print er

    # Wrong:   8539734222754424634652848910090511258579615854677193857951970709776396467716159088650599133108130009238484255292461692164015552
    # Wrong:   8539734222754423994326146834486354552368276653388334248661935298003212654083226261414916360277961348160842908137688846749173184
    # Correct: 8539734222673567065463550869546574495034888535765114961879601127067743044893204848617875072216249073013374895871952806582723184
    # Python Multiply Operator

if __name__ == "__main__":
    main()