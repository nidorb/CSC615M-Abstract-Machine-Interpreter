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
        self.input_tape = InputTape(input_tape)

        self.timelines = [self]
        self.accepted_timeline = None
        
    def step(self):
        active_timelines = [t for t in self.timelines if not t.halt]
        new_timelines = []
        
        for machine in active_timelines:
            if machine.halt:
                continue

            element = machine.input_tape.get_element()
            command = machine.logic[machine.state]["command"]
            transitions = machine.logic[machine.state]["transitions"]
                        
            if command in {"SCAN", "SCAN RIGHT"}:
                if not machine.input_tape.can_move("RIGHT"): #checks if tape is at #
                    machine.input_tape.add_right()
                
                machine.input_tape.move_head("RIGHT")
                element = machine.input_tape.get_element()
                
                #checks all dest state of element
                #fix
                if element in transitions:
                    possible_states = transitions[element]
                    
                    #NFA
                    if len(possible_states) > 1: 
                        for state in possible_states[1:]:
                            new_machine = copy.deepcopy(machine)
                            new_machine.state = state
                            new_timelines.append(new_machine)
                    
                    #DFA
                    machine.state = possible_states[0]


        self.timelines = [t for t in (self.timelines + new_timelines) if not t.halt]

