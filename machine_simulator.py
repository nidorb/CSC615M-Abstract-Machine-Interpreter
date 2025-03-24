from parser import MachineParser
from aux_data import Stack, Queue, Tape, InputTape
import copy

class MachineSimulator:
    def __init__(self, machine_def, input_tape):
        self.parser = MachineParser(machine_def, input_tape)
        self.memory = self.parser.memory
        self.logic = self.parser.logic
        self.state = self.parser.initial_state
        
        self.halt = False
        self.accept = False
        
        self.input_tape = self.parser.input_tape
        
        self.history = [self.state]
        self.timelines = [self]
        self.active_timelines = [self]
        self.accepted_timelines = []
        
        self.output = []
        
    def step(self):
        new_timelines = []
        
        for machine in self.active_timelines:
            #skipped halt states
            if machine.halt:
                continue
            
            element = machine.input_tape.get_element() # read input
            command = machine.logic[machine.state]["command"]
            transitions = machine.logic[machine.state]["transitions"]
            memory_object = machine.logic[machine.state]["memory_object"]
            
            # print(element)
            # print(command)
            # print(transitions)
            # print(memory_object)
                        
            if command in {"SCAN", "SCAN RIGHT", "SCAN LEFT"}:
                if command == "SCAN LEFT":
                    if not machine.input_tape.can_move("LEFT"): #checks if tape is at #
                        machine.input_tape.add_left()
                    machine.input_tape.move_head("LEFT")
                    
                else:
                    if not machine.input_tape.can_move("RIGHT"): #checks if tape is at #
                        machine.input_tape.add_right()     
                    machine.input_tape.move_head("RIGHT")
                
                element = machine.input_tape.get_element()
                            
                #checks all dest state of element
                if element in transitions:
                    possible_states = transitions[element]
                    
                    #NFA
                    if len(possible_states) > 1: 
                        for state in possible_states[1:]:
                            new_machine = copy.deepcopy(machine)
                            new_machine.state = state
                            new_machine.history.append(state)
                            new_machine.handle_state_termination()
                            new_timelines.append(new_machine)                
            
                    machine.state = possible_states[0]
                    machine.history.append(machine.state)
                    machine.handle_state_termination()
                
                # input has no transitions
                else:
                    print(f"[ERROR] No transition found for element '{element}'. Halting.")
                    machine.history.append("reject")
                    machine.state = "reject"
                    machine.halt = True
                
            elif command in {"PRINT", "READ", "WRITE"}:
                for x in transitions:
                    for state in transitions[x]:
                        new_machine = copy.deepcopy(machine)
                        new_machine.state = state

                        if command == "PRINT":
                            new_machine.output.append(x)
                        else:
                            ds = new_machine.memory[memory_object]
                            if command == "WRITE":
                                ds.push(x)

                            elif command == "READ":
                                if ds.peek() == None or ds.peek() != x:
                                    new_machine.halt = True
                                    new_machine.state = "reject"

                                else:
                                    ds.pop()
                                    
                        new_machine.history.append(new_machine.state)
                        new_machine.handle_state_termination()
                        new_timelines.append(new_machine)
                        
                
                self.timelines.remove(machine)
        
        self.timelines += new_timelines
        self.active_timelines = [t for t in self.timelines if not t.halt]
        self.accepted_timelines = [t for t in self.timelines if t.accept]

    #change if reject/accept completely halt
    def handle_state_termination(self):
        if self.state == "accept":
            self.accept = True
            self.halt = True
        elif self.state == "reject":
            self.halt = True
        elif self.state not in self.logic:
            self.halt = True
            self.state = "reject"
            print("Reject")
            self.history.append("reject")
            
    def handle_read(self, ds, x):
        if ds.pop() == None or ds.peek() != x:
            print("Error: Empty Stack or Stack cannot be Read")
            self.halt = True
            self.state = "reject"
            self.history.append("reject")
        

