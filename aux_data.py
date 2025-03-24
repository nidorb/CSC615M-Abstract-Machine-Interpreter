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
            
    def view_ds(self):
        return self.stack
    
class Queue():
    def __init__(self):
        self.queue = []
        
    def is_empty(self):
        return len(self.queue) == 0

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.queue.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.queue[0]
        
    def view_ds(self):
        return self.queue
    
class Tape():
    def __init__(self):
        self.tape = [0]
        self.head = 0

class InputTape:
    def __init__(self, input_string: str):
        self.name = None
        self.tape = ['#'] + list(input_string) + ['#']
        self.head = 0
        
    def __repr__(self):
        return "".join(self.tape)
    
    def get_element(self):
        return self.tape[self.head]
    
    def add_right(self):
        self.tape.append('#')
        
    def add_left(self):
        self.tape.insert(0, '#')
    
    def move_head(self, direction):
        if direction == "LEFT":
            self.head -= 1
        elif direction == "RIGHT":
            self.head += 1
            
    def can_move(self, direction):
        """Returns False if moving out of bounds, True otherwise."""
        if direction == "LEFT" and self.head == 0:
            return False
        if direction == "RIGHT" and self.head == len(self.tape) - 1:
            return False
        return True
