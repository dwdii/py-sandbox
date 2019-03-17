#
# Author: Daniel Dittenhafer
#
#     Created: Feb 21, 2019
#
# Description: Hash table toy implementation
#
__author__ = 'Daniel Dittenhafer'

class MyHashTable:
    def __init__(self):
        self.data = self.allocArray(10)

    def allocArray(self, size):
        d = []
        for x in xrange(size):
            d.append(None)
        return d


    def add(self, key, value):
        h = hash(key)
        m = h % len(self.data)

        if self.data[m] == None:
            self.data[m] = (key, value)
        elif type(self.data[m]) is list:
            self.data[m].append((key, value))
        else:

            if(self.data[0] == key):
                # Same key, update value
                self.data[1] = value
            else:
                chain = []
                chain.append(self.data[m])
                chain.append((key, value))
                self.data[m] = chain

    def get(self, key):
        h = hash(key)
        m = h % len(self.data)

        v = self.data[m]
        if type(v) is list:
            for x in v:
                if x[0] == key:
                    return x[1]
        
        return v

def main():
    t = MyHashTable()
    testData = [("first", 1),("second", 2),("third", 3), ("forth", 4), ("fifth", 5) ,("sixth", 6)]

    for p in testData:
        t.add(p[0], p[1])

    print t.data

    print t.get("third")
    print t.get("unknown")
    print "done"
    


if __name__ == "__main__":
    main()