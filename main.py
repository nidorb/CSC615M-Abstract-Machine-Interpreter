from machine_simulator import MachineSimulator
from aux_data import InputTape
from diagram_generator import StateDiagram
from parser import MachineParser

if __name__ == '__main__':
    machine_def = """
.LOGIC
A] SCAN (0,A), (1,A), (1,B)
B] SCAN (0,C)
C] SCAN (1,accept)
"""

    input_tape = "1000101"



    #machine state diagram generator
    #parser = MachineParser(machine_def, input_tape)
    #StateDiagram(parser.logic, parser.initial_state)
   

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
        for y in x.memory:
            print(y, x.memory[y])
            
        # print("DS1: ", x.memory["S1"].view_ds())
        # print("DS2: ", x.memory["S2"].view_ds())
        # print("DS2: ", x.memory["Q1"])
        print("Input: Mem: ", x.input_tape)
        print("Head: ", x.input_tape.head_x)
        print("Head element: ", x.input_tape.get_element())

        print("State: ", x.state)
        print("Halted: ", x.halt)
        print("Accepted: ", x.accept)
        print("Hisotry: ", x.history)
        print("Output: ", x.output)

        
    # print("\n\ntimeline", machine.timelines)
    print("active timelines", machine.active_timelines)
    print("accepteded timelines", machine.accepted_timelines)