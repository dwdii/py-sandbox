import heapq
import itertools

class heapqplus:

    def __init__(self):
        self._heap = []
        self._entry_finder = {}
        self._counter = itertools.count()
        self.REMOVED = '<removed-task>'      # placeholder for a removed task

    def __len__(self):
        return len(self._heap)

    def add(self, item, priority):
        'Add a new task or update the priority of an existing task'
        if item in self._entry_finder:
            self.remove(item)
        count = next(self._counter)
        entry = [priority, count, item]
        self._entry_finder[item] = entry
        heapq.heappush(self._heap, entry)

    def add_if_priority_lower(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self._entry_finder:
            ee = self._entry_finder[task]
            if ee[0] <= priority:
                return False
            else:
                self.remove(task)

        count = next(self._counter)
        entry = [priority, count, task]
        self._entry_finder[task] = entry
        heapq.heappush(self._heap, entry)
        return True


    def remove(self, task):
        """Mark an existing task as REMOVED.  
           Raise KeyError if not found.
           Remove it from the entry_finder dictionary too."""

        entry = self._entry_finder.pop(task)
        entry[-1] = self.REMOVED
        return entry[0]

    def get(self, task):
        if task in self._entry_finder:
            return self._entry_finder[task][0]
        else:
            return None

    def pop(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self._heap:
            priority, count, task = heapq.heappop(self._heap)
            if task is not self.REMOVED:
                del self._entry_finder[task]
                return priority, task
        raise KeyError('pop from an empty priority queue')
