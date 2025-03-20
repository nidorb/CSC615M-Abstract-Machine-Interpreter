import re
from aux_data import Stack, Queue, Tape

class AbstractMachineParser:
    def __init__(self, input_text):
        self.input_text = input_text.splitlines()
        self.memory = {}
        self.logic = {}
        self.initial_state = None
        self.data_keywords = {"STACK", "QUEUE", "TAPE", "2D_TAPE"}
        self.logic_keywords = {"SCAN", "PRINT", "SCAN RIGHT", "SCAN LEFT", r"READ\((\w+\))", r"WRITE\((\w+\))"}
        self.tape_keywords = {r"LEFT\(\w+\)", r"RIGHT\(\w+\)", r"UP\(\w+\)", r"DOWN\(\w+\)"}
        self.state_keywords = {"accept", "reject"}
        self.transitions=[]
        
        self.parse()

    def parse(self):
        section = None
        for line_number, line in enumerate(self.input_text, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if line == ".DATA":
                section = "DATA"
                continue
            elif line == ".LOGIC":
                section = "LOGIC"
                continue
            
            if section == "DATA":
                self.parse_data(line, line_number)
            elif section == "LOGIC":
                self.parse_logic(line, line_number)
            else:
                print(f"Error: Section is not defined at line {line_number}: {line}")
                exit(1)

    # Parses the data section
    def parse_data(self, line, line_number):
        match = re.match(r"^(\w+)\s(\w+)$", line)
        if match:
            memory_type, name = match.groups()
            
            # Wrong keyword
            if memory_type not in self.data_keywords:
                print(f"Error: Invalid data keyword at line {line_number}: {line}")
                exit(1)
            
            # exisiting Declaration
            if name in self.memory:
                print(f"Error: Duplicate declaration of '{name}' at line {line_number}: {line}")
                exit(1)
            
            #Creates memory object
            if memory_type == "STACK":
                self.memory[name] = Stack()
            elif memory_type == "QUEUE":
                self.memory[name] = Queue()
            elif memory_type == "TAPE":
                self.memory[name] = Tape()
                
        else:
            print(f"Error: Invalid data syntax at line {line_number}: {line}")
            exit(1)
            
    # Parses the logic section
    def parse_logic(self, line, line_number):
        # <SOURCE_STATE_NAME>] COMMAND (<SYMBOL_1>,<DESTINATION_STATE_NAME_1>)
        #                         state       command              transitions
        logic_match = re.match(r"^(\w+)\]\s+([\w\s]+(?:\(\w+\))?)\s+((?:\([\w#]+,\w+\)(?:,\s*)?)*)$", line)
        
        # <SOURCE_STATE_NAME>] COMMAND(<tape_name>) (<SYMBOL_1>/<REPLACEMENT_SYMBOL_1>,<DESTINATION_STATE_NAME_1>)
        #                         state       command              transitions
        tape_match = re.match(r"(\w+)\]\s+([\w\s]+(?:\(\w+\))?)\s+((?:\([\w#]+/[\w#],\w+\)(?:,\s*)?)*)$", line)
        arg = None
        # check for non-tape logic
        if logic_match:
            state, command, transitions = logic_match.groups()            
            
            #checks if state already has command
            if state in self.logic:
                print(f"Error: Duplicate definition of state '{state}' at line {line_number}: {line}")
                exit(1)
            
            #checks if command is valid
            if not any(re.fullmatch(pattern, command) for pattern in self.logic_keywords):
                print(f"Error: Invalid logic keyword at line {line_number}: {line}")
                exit(1)
                
            command_match = re.match(r"(READ|WRITE)\((\w+)\)", command)
            if command_match:
                command, arg = command_match.groups()
                if arg not in self.memory:
                    print(f"Error: Memory object does not exist at line {line_number}: {line}")
                    exit(1)
                
            #initializes first line as initial state
            if self.initial_state is None:
                self.initial_state = state

            parsed_transitions = self.parse_logic_transitions(transitions)
            
            self.logic[state] = {"command": command, "Memory Object": arg, "transitions": parsed_transitions}
            
        # check for tape logic
        elif tape_match:
            state, command, transitions = tape_match.groups()
            
            #checks if state already has command
            if state in self.logic:
                print(f"Error: Duplicate definition of state '{state}' at line {line}")
                exit(1)
            
            #checks if command is valid
            if not any(re.fullmatch(pattern, command) for pattern in self.tape_keywords):
                print(f"Error: Invalid command keyword at line {line_number}: {line}")
                exit(1)
                
            command_match = re.match(r"(LEFT|RIGHT|UP|DOWN)\((\w+)\)", command)
            if command_match:
                command, arg = command_match.groups()
                if arg not in self.memory:
                    print(f"Error: Memory object does not exist at line {line_number}: {line}")
                    exit(1)
                elif self.memory[arg].__class__.__name__ != "Tape":
                    print(f"Error: Memory object is not a Tape at line {line_number}: {line}")
                    exit(1)
            
            #initializes first line as initial state
            if self.initial_state is None:
                self.initial_state = state
                
            parsed_transitions = self.parse_transitions(transitions) if transitions else {}
            
            self.logic[state] = {"command": command, "transitions": transitions}
            
        else:
            print(f"Error: Invalid logic syntax at line {line_number}: {line}")
            exit(1)
    
    def parse_logic_transitions(self, transitions):
        parsed = {}
        
        pattern = r"\(([\w#]+),\s*(\w+)\)" 
        
        # Find all matches
        matches = re.findall(pattern, transitions)
        
        for symbol, state in matches:
            parsed[symbol] = state

        return parsed
    
    def parse_transitions(self, transitions):
        parsed = {}
        for transition in transitions.split(","):
            transition = transition.strip()
            match = re.match(r"\(([^/,]+)/?([^/]*)?,(\w+)\)", transition)
            if match:
                symbol, replacement, destination = match.groups()
                parsed[symbol] = {"replacement": replacement or None, "destination": destination}
        return parsed

    def display(self):
        print("\nAuxiliary Memory:")
        
        for x in self.memory:
            print(x, self.memory[x].__class__.__name__, self.memory[x])

        print("\nState Transitions:")
        for state, details in self.logic.items():
            print(f"  {state} -> {details}")

        print(f"\nInitial State: {self.initial_state}")

# Example Usage
input_text = """
.DATA
STACK S1

.LOGIC
A] WRITE(S1) (1,B)
B] SCAN (0,C), (1,D)
C] WRITE(S1) (#,B)
D] READ(S1) (#,E)
E] SCAN (1,D), (#,F)

"""

parser = AbstractMachineParser(input_text)
parser.display()
#print("Test:", parser.logic["A"]["command"])