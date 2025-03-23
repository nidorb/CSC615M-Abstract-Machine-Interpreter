from machine_simulator import MachineSimulator
from aux_data import InputTape

if __name__ == '__main__':
    machine_def = """
    #NFA for detecting substring "101"
    
    .DATA
    STACK S1
    QUEUE Q1
    TAPE T1
    .LOGIC
    E] PRINT (0,A), (0,B), (1,A)
    A] SCAN (0,A), (1,B), (1,F)
    B] SCAN (0,F), (1,C)
    C] SCAN (0,accept), (1,E)
    F] PRINT (0,A)

    """

    input_tape = "01"


    machine = MachineSimulator(machine_def, input_tape)
    halt = False
            
    while machine.active_timelines and not halt:  # Run while there are active timelines
        machine.step()
        
        for x in machine.timelines:
            if x.halt:  # Only check machines that have halted
                if x.accept == True:
                    print("Accepted Machine:", x)
                    halt = True
                    break  # Stop execution if accepted
                elif x.reject == True:
                    print("Rejected Machine:", x)
                    halt = True
                    break

    
    for x in machine.timelines:
        print("\n\n", x)
        print("DS: ", x.memory)
        print("State: ", x.state)
        print("Halted: ", x.halt)
        print("Accepted: ", x.accept)
        print("Hisotry: ", x.history)
        print("Output: ", x.output)

        
        
    # print("\n\ntimeline", machine.timelines)
    # print("active timelines", machine.active_timelines)