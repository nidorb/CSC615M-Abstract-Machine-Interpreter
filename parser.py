import re

class AbstractMachineParser:
    def __init__(self, input_text):
        self.input_text = input_text.splitlines()
        self.memory = []
        self.logic = {}
        self.initial_state = None
        self.data_keywords = {"STACK", "QUEUE", "TAPE", "2D_TAPE"}
        self.logic_keywords = {"SCAN", "PRINT", "SCAN RIGHT", "SCAN LEFT", "READ", "WRITE"}
        self.tape_keywords = {"LEFT", "RIGHT", "UP", "DOWN"}
        self.state_keywords = {"accept", "reject"}
        
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

    def parse_data(self, line, line_number):
        match = re.match(r"^(STACK|QUEUE|TAPE|2D_TAPE) (\w+)$", line)
        if match:
            memory_type, name = match.groups()

            # Ensure the exact type-name pair doesn't already exist
            if (memory_type, name) in self.memory:
                print(f"Error: Duplicate declaration of {memory_type} '{name}' at line {line_number}")
                exit(1)

            self.memory.append((memory_type, name))  # Store as a tuple in a list
        else:
            print(f"Error: Invalid data syntax at line {line_number}: {line}")
            exit(1)


    def parse_logic(self, line, line_number):
                                # state space command space
                                # fix
        logic_match = re.match(r"^(\w+)]\s{1}[A-Z]+\s{1}[A-Z]+$", line)
        if logic_match:
            state, command, transitions = logic_match.groups()
            if command not in self.logic_keywords:
                print(f"Error: Invalid logic keyword at line {line_number}: {command}")
                exit(1)

            parsed_transitions = self.parse_transitions(transitions) if transitions else {}

            if self.initial_state is None:
                self.initial_state = state

            self.logic[state] = {"command": command, "transitions": parsed_transitions}
            print(transitions)
        else:
            print(f"Error: Invalid logic syntax at line {line_number}: {line}")
            exit(1)

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
        print("Auxiliary Memory:")
        for mem_type, name in self.memory:
            print(f"  {mem_type}: {name}")

        print("\nState Transitions:")
        for state, details in self.logic.items():
            print(f"  {state} -> {details}")

        print(f"\nInitial State: {self.initial_state}")

# Example Usage
input_text = """.DATA
STACK 123
QUEUE Q1
TAPE S1
TAPE 2
TAPE Q1
TAPE Q3

.LOGIC
A] WRITE (123)
"""

parser = AbstractMachineParser(input_text)
parser.display()
