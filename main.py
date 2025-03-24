from machine_simulator import MachineSimulator
from aux_data import InputTape

if __name__ == '__main__':
    machine_def = """
.DATA
QUEUE Q1
STACK S1
STACK S2
.LOGIC
A] SCAN (a,B), (b,C)
B] WRITE(Q1) (X,A)
C] READ(Q1) (X,D)
D] WRITE(Q1) (Y,E)
E] SCAN (b,C), (c,F)
F] WRITE(Q1) (#,G)
G] READ(Q1) (Y,H)
H] SCAN (c,G), (#,I)
I] READ(Q1) (#,accept)

"""

    input_tape = "aaabbbccc"


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