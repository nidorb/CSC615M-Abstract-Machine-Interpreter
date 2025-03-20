class Stack():
    def __init__(self):
        self.stack = []
        
    def is_empty(self):
        return len(self.stack) == 0

    def push(self, item):
        self.stack.append(item)
        
    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.stack[-1]

    def __len__(self):
        return len(self.stack)

    def __str__(self):
        return str(self.stack)

class Queue():
    def __init__(self):
        self.queue = []
        
    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, item):
        self.queue.append(item)
        
    def dequeue(self):
        if self.is_empty():
            return None
        else:
            return self.queue.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.queue[0]

    def __len__(self):
        return len(self.queue)

    def __str__(self):
        return str(self.queue)
    
class Tape():
    def __init__(self):
        self.tape = [0]
        self.position = 0

class Tape():
    def __init__(self):
        self.tape = [[0]]
        self.position = (0, 0)