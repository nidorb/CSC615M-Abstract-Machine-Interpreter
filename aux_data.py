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
        return "".join(map(str, self.stack))
    
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
        return "".join(map(str, self.queue))
    
    
class Tape():
    def __init__(self):
        self.tape = ['#'] + ['#']
        self.head_x = 0
        self.head_y = None
    
    def __repr__(self):
        return "".join(self.tape)
    
    def get_element(self):
        return self.tape[self.head_x]
    
    def add_right(self):
        self.tape.append('#')
    
    def add_left(self):
        self.tape.insert(0, '#')

    def move_head(self, direction):
        if direction == "LEFT":
            self.head_x = max(0, self.head_x - 1)        
        elif direction == "RIGHT":
            self.head_x += 1
            
    def can_move(self, direction):
        if direction == "LEFT" and self.head_x == 0:
            return False
        if direction == "RIGHT" and self.head_x == len(self.tape) - 1:
            return False
        return True
    
    def replace(self, element):
        self.tape[self.head_x] = element
    
    def get_row(self):
        return self.tape
    
    def view_ds(self):
        return ''.join(self.tape)
    
class InputTape():
    def __init__(self, input_string: str):
        self.name = None
        self.tape = ['#'] + list(input_string) + ['#']
        self.head_x = 0
        self.head_y = None
        
    def __repr__(self):
        return "".join(self.tape)
    
    def get_element(self):
        return self.tape[self.head_x]
    
    def add_right(self):
        self.tape.append('#')
        
    def add_left(self):
        self.tape.insert(0, '#')
    
    def move_head(self, direction):
        if direction == "LEFT":
            self.head_x = max(0, self.head_x - 1)
            
        elif direction == "RIGHT":
            self.head_x += 1
            
    def can_move(self, direction):
        """Returns False if moving out of bounds, True otherwise."""
        if direction == "LEFT" and self.head_x == 0:
            return False
        if direction == "RIGHT" and self.head_x == len(self.tape) - 1:
            return False
        return True
    
    def replace(self, element):
        self.tape[self.head_x] = element
        
    def get_row(self):
        return self.tape
    
    def view_ds(self):
        return self.tape

class Tape2D():
    def __init__(self):
        self.tape = [['#'] + ['#']]
        self.head_x = 0
        self.head_y = 0
    
    def __repr__(self):
        return "\n".join(["".join(row) for row in self.tape])
    
    def get_row(self):
        return self.tape[self.head_y]
    
    def move_head(self, direction):
        if direction == "LEFT":
            self.head_x = max(0, self.head_x - 1)        
        elif direction == "RIGHT":
            self.head_x += 1
        if direction == "UP":
            self.head_y = max(0, self.head_y - 1)        
        elif direction == "DOWN":
            self.head_y += 1
        
    def can_move(self, direction):
        if direction == "LEFT" and self.head_x == 0:
            return False
        elif direction == "RIGHT" and self.head_x == len(self.tape[self.head_y]) - 1:
            return False
        elif direction == "UP" and self.head_y == 0:
            return False
        elif direction == "DOWN" and self.head_y == len(self.tape) - 1:
            return False
        return True
    
    def get_element(self):
        return self.tape[self.head_y][self.head_x]
    
    def add_up(self):
        self.tape.insert(0, ['#']*len(self.tape[self.head_y]))
    
    def add_down(self):
        self.tape.append(['#']*len(self.tape[self.head_y]))
    
    def add_right(self):
        for i in range(len(self.tape)):
            self.tape[i].append('#')
    
    def add_left(self):
        for i in range(len(self.tape)):
            self.tape[i].insert(0, '#')
        
    def view_tape(self):
        return self.tape
    
    def replace(self, element):
        self.tape[self.head_y][self.head_x] = element
    
    def get_tape(self):
        return self.tape
    
    def view_ds(self):
        return "\n".join(["".join(row) for row in self.tape])

        
class InputTape2D():
    def __init__(self, input_string: str):
        self.name = None
        self.tape = [['#'] + list(input_string) + ['#']]
        self.head_x = 0
        self.head_y = 0
    
    def __repr__(self):
        return "\n".join(["".join(row) for row in self.tape])
    
    def get_row(self):
        return self.tape[self.head_y]
    
    def move_head(self, direction):
        if direction == "LEFT":
            self.head_x = max(0, self.head_x - 1)        
        elif direction == "RIGHT":
            self.head_x += 1
        if direction == "UP":
            self.head_y = max(0, self.head_y - 1)        
        elif direction == "DOWN":
            self.head_y += 1
        
    def can_move(self, direction):
        if direction == "LEFT" and self.head_x == 0:
            return False
        elif direction == "RIGHT" and self.head_x == len(self.tape[self.head_y]) - 1:
            return False
        elif direction == "UP" and self.head_y == 0:
            return False
        elif direction == "DOWN" and self.head_y == len(self.tape) - 1:
            return False
        return True
    
    def get_element(self):
        return self.tape[self.head_y][self.head_x]
    
    def add_up(self):
        self.tape.insert(0, ['#']*len(self.tape[self.head_y]))
    
    def add_down(self):
        self.tape.append(['#']*len(self.tape[self.head_y]))
    
    def add_right(self):
        for i in range(len(self.tape)):
            self.tape[i].append('#')
    
    def add_left(self):
        for i in range(len(self.tape)):
            self.tape[i].insert(0, '#')
        
    def view_tape(self):
        return self.tape
    
    def replace(self, element):
        self.tape[self.head_y][self.head_x] = element
    
    def get_tape(self):
        return self.tape
    
    def view_ds(self):
        return "\n".join(["".join(row) for row in self.tape])
