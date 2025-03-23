from machine_simulator import MachineSimulator
from aux_data import InputTape

if __name__ == '__main__':
    machine_def = """
    .LOGIC
    A] SCAN RIGHT (0,A), (1,B), (#,accept), (1,C)
    B] SCAN LEFT (0,C), (1,reject)
    C] SCAN RIGHT (1,A)
    """

    input_tape = "00010101"


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

    print("Number of Timelines: ", len(machine.timelines))
    
    # machine.step()

    
    for x in machine.timelines:
        print("\n\n", x)
        print("State: ", x.state)
        print("Halted: ", x.halt)
        print("Accepted: ", x.accept)
        print("Hisotry: ", x.history)
        
        
    # print("\n\ntimeline", machine.timelines)
    # print("active timelines", machine.active_timelines)