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
        
        self.step_count = 0
        
        self.output = ""
        
    def step(self):
        new_timelines = []
        
        for machine in self.active_timelines:
            #skipped halt states
            if machine.halt:
                continue
            machine.step_count +=1
            element = machine.input_tape.get_element() # read input
            command = machine.logic[machine.state]["command"]
            transitions = machine.logic[machine.state]["transitions"]
            memory_object = machine.logic[machine.state]["memory_object"]
                        
            if command in {"SCAN", "SCAN RIGHT", "SCAN LEFT"}:
                if command == "SCAN LEFT":
                    if not machine.input_tape.can_move("LEFT"):
                        machine.input_tape.add_left()
                        # machine.halt = True
                        # machine.history.append("reject")
                        # machine.state = "reject"
                        # continue
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
                    machine.history.append("reject")
                    machine.state = "reject"
                    machine.halt = True
                
            elif command in {"PRINT", "WRITE"}: #NFA for all transitions (no checking)
                firstkey, firststates = next(iter(transitions.items()))

                for x in transitions:
                    for state in transitions[x]:
                        if x == firstkey and state == firststates[0]:
                            print("skip", x, state)
                            continue

                        new_machine = copy.deepcopy(machine)
                        new_machine.state = state

                        if command == "PRINT":
                            new_machine.output += str(x)
                        else:
                            ds = new_machine.memory[memory_object]
                            if command == "WRITE":
                                ds.push(x)
                                    
                        new_machine.history.append(new_machine.state)
                        new_machine.handle_state_termination()
                        new_timelines.append(new_machine)
                        
                        
                machine.state = firststates[0]
                if command == "PRINT":
                    machine.output += str(firstkey)
                else:
                    ds = machine.memory[memory_object]
                    if command == "WRITE":
                        ds.push(firstkey)

                machine.history.append(machine.state)
                machine.handle_state_termination()               
            
            elif command == "READ":
                ds = machine.memory[memory_object]
                top_element = ds.peek()
                
                if top_element in transitions:
                    possible_states = transitions[top_element]
                    
                    #NFA
                    if len(possible_states) > 1: 
                        for state in possible_states[1:]:
                            new_machine = copy.deepcopy(machine)
                            ds = new_machine.memory[memory_object]
                            ds.pop()
                            new_machine.state = state
                            new_machine.history.append(state)
                            new_machine.handle_state_termination()
                            new_timelines.append(new_machine)                

                    ds = machine.memory[memory_object]
                    ds.pop()
                    machine.state = possible_states[0]
                    machine.history.append(machine.state)
                    machine.handle_state_termination()
                else:
                    machine.history.append("reject")
                    machine.state = "reject"
                    machine.halt = True
                                    
            elif command in {"LEFT", "RIGHT"}:
                isInputTape = False
                #checks if tape is input or not
                if memory_object == machine.input_tape.name:
                    tape = machine.input_tape
                    isInputTape = True
                else:
                    tape = machine.memory[memory_object]

                if command == "LEFT":
                    if not tape.can_move("LEFT"): #checks if tape is at #
                        tape.add_left()
                        # machine.halt = True
                        # machine.history.append("reject")
                        # machine.state = "reject"
                        # continue
                    tape.move_head("LEFT")
                                    
                elif command == "RIGHT":
                    if not tape.can_move("RIGHT"): #checks if tape is at #
                        tape.add_right()       
                    tape.move_head("RIGHT")
                
                element = tape.get_element()
                
                #checks all dest state of element
                if element in transitions:
                    possible_states = transitions[element]

                    #NFA
                    if len(possible_states) > 1: 
                        for replacement, state in possible_states[1:]:
                            new_machine = copy.deepcopy(machine)
                            new_machine.state = state
                            
                            if isInputTape:
                                new_machine.input_tape.replace(replacement)
                                self.check_mark_tape(new_machine.input_tape, command, element, replacement)
                            else:
                                new_machine.memory[memory_object].replace(replacement)
                                self.check_mark_tape(new_machine.memory[memory_object], command, element, replacement)
                                      
                            new_machine.history.append(state)
                            new_machine.handle_state_termination()
                            new_timelines.append(new_machine)
                            
                    replacement, state = possible_states[0]                
                    machine.state = state   
                    if isInputTape:
                        machine.input_tape.replace(replacement)
                        self.check_mark_tape(machine.input_tape, command, element, replacement)
                    else:
                        machine.memory[memory_object].replace(replacement)
                        self.check_mark_tape(machine.memory[memory_object], command, element, replacement)
                    machine.history.append(machine.state)
                    machine.handle_state_termination()
                
                # input has no transitions
                else:
                    machine.history.append("reject")
                    machine.state = "reject"
                    machine.halt = True
            
            elif command in {"UP", "DOWN"}: 
                isInputTape = False
                if memory_object == machine.input_tape.name:
                    tape = machine.input_tape
                    isInputTape = True
                else:
                    tape = machine.memory[memory_object]
                    
                if command == "UP":
                    if not tape.can_move("UP"): #checks if tape is at #
                        tape.add_up()
                    tape.move_head("UP")
                    
                                    
                elif command == "DOWN":
                    if not tape.can_move("DOWN"): #checks if tape is at #
                        tape.add_down()       
                    tape.move_head("DOWN")
                    
                
                element = tape.get_element()
                #checks all dest state of element
                if element in transitions:
                    possible_states = transitions[element]

                    #NFA
                    if len(possible_states) > 1: 
                        for replacement, state in possible_states[1:]:
                            new_machine = copy.deepcopy(machine)
                            new_machine.state = state
                            
                            if isInputTape:
                                new_machine.input_tape.replace(replacement)
                                self.check_mark_tape_updown(new_machine.input_tape, command, element, replacement)
                            else:
                                new_machine.memory[memory_object].replace(replacement)
                                self.check_mark_tape_updown(new_machine.memory[memory_object], command, element, replacement)
                                      
                            new_machine.history.append(state)
                            new_machine.handle_state_termination()
                            new_timelines.append(new_machine)
                            
                    replacement, state = possible_states[0]                
                    machine.state = state   
                    if isInputTape:
                        machine.input_tape.replace(replacement)
                        self.check_mark_tape_updown(machine.input_tape, command, element, replacement)
                    else:
                        machine.memory[memory_object].replace(replacement)
                        self.check_mark_tape_updown(machine.memory[memory_object], command, element, replacement)
                    machine.history.append(machine.state)
                    machine.handle_state_termination()
                
                # input has no transitions
                else:
                    machine.history.append("reject")
                    machine.state = "reject"
                    machine.halt = True
                
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
            
    def check_mark_tape(self, tape, command, element, replacement):
        if element == "#" and replacement != "#":
            if command in {"LEFT", "SCAN LEFT"} and tape.head_x == 0:
                tape.add_left()
                tape.head_x += 1
            elif command in {"RIGHT", "SCAN", "SCAN RIGHT"} and tape.head_x == len(tape.get_row()) - 1:
                tape.add_right()
    
    def check_mark_tape_updown(self, tape, command, element, replacement):
        if element == "#" and replacement != "#":
            if tape.head_x == 0:
                tape.add_left()
                tape.head_x += 1
            elif tape.head_x == len(tape.get_row()) - 1:
                tape.add_right()
    
    def get_memory(self):
        return self.memory

    

