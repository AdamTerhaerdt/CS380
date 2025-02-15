class Stack:
    def __init__(self):
        self.items = []
        
    def push(self, item, priority = None):
        self.items.append(item)
        
    def pop(self):
        if len(self.items) == 0:
            return None
        return self.items.pop()
        
    def is_empty(self):
        return len(self.items) == 0
        
    def size(self):
        return len(self.items)