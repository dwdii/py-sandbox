#
# Author: Daniel Dittenhafer
#
#     Created: Feb 25, 2019
#
# Description: Sorting algorithms toy implementations
#
__author__ = 'Daniel Dittenhafer'

class Sorting:
    def __init__(self):
        pass

    def quicksort(self, data, s, e):

        if s < e:
            p = self.paritionHoare(data, s, e)
            self.quicksort(data, s, p)
            self.quicksort(data, p + 1, e)


    def partitionLomuto (self, data, s, e):
        pivot = data[e]
        i = s
        for j in xrange(s, e):
            if data[j] < pivot:
                data[i], data[j] = data[j], data[i]
                i = i + 1

        data[i], data[e] = data[e], data[i]

        return i

    def paritionHoare(self, data, s, e):
        pivot = data[(s + e) / 2]
        i = s - 1
        j = e + 1

        while True:

            while True:
                i = i + 1
                if data[i] >= pivot:
                    break

            while True:
                j = j - 1
                if data[j] <= pivot:
                    break

            if i >= j:
                return j

            data[i], data[j] = data[j], data[i]


def main():
    t = Sorting()
    #testData = ['b','z','t','r','d','e']
    testData = ['z','b','z','t','r','d','e','y']
    t.quicksort(testData, 0, len(testData) - 1)
    print testData
    


if __name__ == "__main__":
    main()