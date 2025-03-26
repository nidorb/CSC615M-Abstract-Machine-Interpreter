from machine_simulator import MachineSimulator
from aux_data import InputTape
from diagram_generator import StateDiagram
from parser import MachineParser

if __name__ == '__main__':
    machine_def = """
.DATA
.DATA
TAPE T1
TAPE T2
TAPE T3
.LOGIC
A] RIGHT(T1) (a/a,B), (b/b,C)
B] RIGHT(T2) (#/X,A)
C] RIGHT(T2) (#/#,D)
D] LEFT(T2) (X/#,E)
E] RIGHT(T3) (#/X,F)
F] RIGHT(T1) (b/b,E), (c/c,G)
G] RIGHT(T3) (#/#,H)
H] LEFT(T3) (X/#,I)
I] RIGHT(T3) (c/c,H), (#/#,J)
J] LEFT(T2) (#/#,K)
K] LEFT(T3) (#/#,accept)
"""

    input_tape = "abbcc"



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
        #print("DS1: ", x.memory["S1"].view_ds())
        #print("DS2: ", x.memory["S2"].view_ds())
        # print("DS2: ", x.memory["Q1"])
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