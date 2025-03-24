from machine_simulator import MachineSimulator
from aux_data import InputTape
from diagram_generator import StateDiagram
from parser import MachineParser

if __name__ == '__main__':
    machine_def = """
.DATA
STACK S1
.LOGIC
A] WRITE(S1) (#,B)
B] SCAN RIGHT (a,C), (b,D)
C] WRITE(S1) (X,B)
D] READ(S1) (X,E)
E] SCAN RIGHT (b,D), (c,F), (#,F)
F] READ(S1) (#,G)
G] WRITE(S1) (#,H)
H] SCAN LEFT (b,H), (a,I)
I] SCAN RIGHT (a,I), (b,J)
J] WRITE(S1) (X,K)
K] SCAN RIGHT (b,J), (c,L)
L] READ(S1) (X,M)
M] SCAN RIGHT (c,L), (#,N)
N] READ(S1) (#,accept)

"""

    input_tape = "aaabbbccc"

    parser = MachineParser(machine_def, input_tape)
    StateDiagram(parser.logic, parser.initial_state)
   

    machine = MachineSimulator(machine_def, input_tape)
    halt = False
    
    # machine.step()
            
    while machine.active_timelines and not halt:  # Run while there are active timelines
        machine.step()
        for x in machine.timelines:
            if x.halt:  # Only check machines that have halted
                if x.accept == True:
                    print("Accepted Machine:", x)
                    halt = True
                    break  # Stop execution if accepted

    
    for x in machine.timelines:
        print("\n\n", x)
        # print("DS1: ", x.memory["S1"])
        # print("DS2: ", x.memory["S2"])
        # print("DS2: ", x.memory["Q1"])

        print("State: ", x.state)
        print("Halted: ", x.halt)
        print("Accepted: ", x.accept)
        print("Hisotry: ", x.history)
        print("Output: ", x.output)

        
        
    # print("\n\ntimeline", machine.timelines)
    print("active timelines", machine.active_timelines)
    print("accepteded timelines", machine.accepted_timelines)
    
    print("Output: ", machine.output)