#
# Author: Daniel Dittenhafer
#
#     Created: Feb 21, 2019
#
# Description: Hash table toy implementation
#
__author__ = 'Daniel Dittenhafer'

class MyHashTable:
    def __init__(self, size=100):
        self._data = self.allocArray(size)

    @property
    def data(self):
        return self._data

    def allocArray(self, size):
        d = []
        for _ in xrange(size):
            d.append(None)
        return d


    def add(self, key, value):
        m = self.compute_index(key)

        if self._data[m] == None:
            self._data[m] = (key, value)
        elif type(self._data[m]) is list:
            self._data[m].append((key, value))
        else:

            if(self._data[0] == key):
                # Same key, update value
                self._data[1] = value
            else:
                chain = []
                chain.append(self._data[m])
                chain.append((key, value))
                self._data[m] = chain
    
    def compute_index(self, key):
        h = hash(key)
        return h % len(self._data)


    def get(self, key):
        m = self.compute_index(key)

        v = self._data[m]
        if type(v) is list:
            for x in v:
                if x[0] == key:
                    # Found, return the chained item value
                    return x[1]

            # If we reach here then the key wasn't found in the chained list
            return None
        
        # Return the non-chained value... maybe None, maybe the value.
        return v

def main():
    t = MyHashTable(size=5)
    testData = [("first", 1),("second", 2),("third", 3), ("forth", 4), ("fifth", 5) ,("sixth", 6), ("seventh", 7), ("eighth", 8)]

    for p in testData:
        t.add(p[0], p[1])

    print t.data

    r = t.get("third")
    validate_result(r, 3)

    r = t.get("unknown")
    validate_result(r, None)
    print "done"
    
def validate_result(res, expected):
    if res == expected:
        ok = "SUCCESS"    
    else:
        ok = "FAIL"
    print "{0} {1}".format(res, ok)


if __name__ == "__main__":
    main()