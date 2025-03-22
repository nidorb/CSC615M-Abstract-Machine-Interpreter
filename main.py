from machine_simulator import MachineSimulator
from aux_data import InputTape

if __name__ == '__main__':
    machine_def = """
    .LOGIC
    q0] SCAN (0,q0), (0,q2), (1,q1)
    q1] SCAN (0,q0), (0,q1), (1,q2)
    q2] SCAN (0,q0), (1,q1), (2,accept)

    """

    input_tape = "100"


    machine = MachineSimulator(machine_def, input_tape)
    machine.step()
    machine.step()
    machine.step()

    
    for x in machine.timelines:
        print("\n\n", x)
        print("State: ", x.state)
    #     print("Mem: ", x.memory)
    #     print("Logic: ", x.logic)
    


    
    # machine.step()
    # machine.step()
    # machine.step()
    # machine.step()
    # print(machine.logic)

    # print(machine.memory)
    # print(machine.logic[machine.initial_state]["transitions"].get(machine.input_tape.get_element()))
    # print(machine.initial_state)
    # print(machine.input_tape)
