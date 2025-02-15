import heapq

class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.count = 0
        
    def push(self, item, priority):
        heapq.heappush(self.queue, (priority, self.count, item))
        self.count += 1
        
    def pop(self):
        if not self.queue:
            raise Exception("Queue is empty")
        priority, count, item = heapq.heappop(self.queue)
        return (item, priority)
        
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
