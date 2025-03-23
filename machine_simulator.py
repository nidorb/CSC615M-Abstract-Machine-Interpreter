from parser import MachineParser
from aux_data import InputTape
import copy

class MachineSimulator:
    def __init__(self, machine_def, input_tape):
        self.parser = MachineParser(machine_def)
        self.memory = self.parser.memory
        self.logic = self.parser.logic
        self.state = self.parser.initial_state
        self.halt = False
        self.accept = False
        self.reject = False
        self.input_tape = InputTape(input_tape)
        self.history = [self.state]

        self.timelines = [self]
        self.active_timelines = [self]
        
    def step(self):
        new_timelines = []
        
        for machine in self.active_timelines:
            #skipped halt states
            if machine.halt:
                continue
            
            element = machine.input_tape.get_element() # read input
            command = machine.logic[machine.state]["command"]
            transitions = machine.logic[machine.state]["transitions"]
                        
            if command in {"SCAN", "SCAN RIGHT", "SCAN LEFT"}:
                
                if command == "SCAN LEFT":
                    if not machine.input_tape.can_move("LEFT"): #checks if tape is at #
                        machine.input_tape.add_left()
                    
                    machine.input_tape.move_head("LEFT")
                    element = machine.input_tape.get_element() # move head to right
                    
                else:
                    if not machine.input_tape.can_move("RIGHT"): #checks if tape is at #
                        machine.input_tape.add_right()
                
                    machine.input_tape.move_head("RIGHT")
                    element = machine.input_tape.get_element() # move head to left
                    
                print(command, "Element: ", element)
                            
                #checks all dest state of element
                if element in transitions:
                    possible_states = transitions[element]
                    
                    #NFA
                    if len(possible_states) > 1: 
                        for state in possible_states[1:]:
                            new_machine = copy.deepcopy(machine)
                            new_machine.state = state
                            new_machine.history.append(state)
                            
                            if new_machine.state == "accept":
                                new_machine.accept = True
                                new_machine.halt = True
                            
                            elif new_machine.state == "reject":
                                new_machine.halt = True
                                new_machine.reject = True
                                
                            elif new_machine.state not in new_machine.logic: #dead state
                                new_machine.halt = True
                            
                            new_timelines.append(new_machine)
                            
                    machine.state = possible_states[0]
                    machine.history.append(machine.state)
                    
                    if machine.state == "accept":
                        machine.accept = True
                        machine.halt = True
                    
                    elif machine.state == "reject":
                        machine.halt = True
                        machine.reject = True
                    
                    elif machine.state not in machine.logic: #dead
                        machine.halt = True
                
                # input has no transitions
                else:
                    machine.halt = True

            elif command in {"READ", "WRITE"}:
                continue
            
            
        self.timelines = [t for t in (self.timelines + new_timelines)]
        self.active_timelines = [t for t in self.timelines if not t.halt]

