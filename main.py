from machine_simulator import MachineSimulator
from aux_data import InputTape
from diagram_generator import StateDiagram
from parser import MachineParser

if __name__ == '__main__':
    machine_def = """
.DATA
STACK S1
STACK S2
.LOGIC
A] WRITE(S1) (#,B), (#,O)
B] WRITE(S2) (#,C)
C] WRITE(S1) (X,D)
D] READ(S1) (X,E), (#,G), (X,D)
E] WRITE(S2) (X,F)
F] SCAN (1,D)
G] SCAN (1,H), (#,accept)
H] WRITE(S1) (#,I)
I] READ(S2) (X,J), (#,L)
J] WRITE(S1) (X,I)
L] WRITE(S2) (#,M)
M] WRITE(S2) (X,N)
N] WRITE(S2) (X,F)
O] SCAN (#,P)
P] READ(S1) (#,accept)
"""

    input_tape = "11111"


    #machine state diagram generator
    #parser = MachineParser(machine_def, input_tape)
    #StateDiagram(parser.logic, parser.initial_state)
   

    machine = MachineSimulator(machine_def, input_tape)
    halt = False

    # machine.step()
    # machine.step()
    # machine.step()
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
        print("DS1: ", x.memory["S1"].view_ds())
        print("DS2: ", x.memory["S2"].view_ds())
        # print("DS2: ", x.memory["Q1"])
        for y in x.memory:
            print(y, "Mem: ", x.memory[y])
        print("Input: Mem: ", x.input_tape)
        print("Head: ", x.input_tape.head)
        print("Head element: ", x.input_tape.get_element())

        print("State: ", x.state)
        print("Halted: ", x.halt)
        print("Accepted: ", x.accept)
        print("Hisotry: ", x.history)
        print("Output: ", x.output)

        
    # print("\n\ntimeline", machine.timelines)
    print("active timelines", machine.active_timelines)
    print("accepteded timelines", machine.accepted_timelines)