from machine_simulator import MachineSimulator
from aux_data import InputTape
from diagram_generator import StateDiagram
from parser import MachineParser

if __name__ == '__main__':
    machine_def = """
.DATA
TAPE T1
.LOGIC
A] RIGHT(T1) (0/X,B), (Y/Y,D), (1/1,reject)
B] RIGHT(T1) (0/0,B), (Y/Y,B), (1/Y,C)
C] LEFT(T1) (0/0,C), (Y/Y,C), (X/X,A)
D] RIGHT(T1) (Y/Y,D), (#/#,accept), (1/1,reject)



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