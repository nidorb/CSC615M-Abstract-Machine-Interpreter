from machine_simulator import MachineSimulator
from aux_data import InputTape
from diagram_generator import StateDiagram
from parser import MachineParser

if __name__ == '__main__':
    machine_def = """
.DATA
STACK S1
.LOGIC
A] WRITE(S1) (#,B), (#,C)
B] READ(S1) (#,B), (#,E)
C] SCAN RIGHT (0,C), (1,D), (X,E)
D] READ(S1) (#,B), (#,E)
E] SCAN RIGHT (1,E), (0,E), (X,F)
F] SCAN RIGHT (0,G), (1,H), (#,I)
G] READ(S1) (Y,F)
H] READ(S1) (Z,F)
I] READ(S1) (#,J)
J] WRITE(S1) (#,K)
K] SCAN LEFT (0,L), (1,M), (X,N)
L] WRITE(S1) (Y,K)
M] WRITE(S1) (Z,K)
N] SCAN LEFT (0,O), (1,P), (X,Q)
O] READ(S1) (Y,N)
P] READ(S1) (Z,N)
Q] READ(S1) (#,accept)

"""

    input_tape = "010101X010101X101010"
    parser = MachineParser(machine_def, input_tape)
    StateDiagram(parser.logic, parser.initial_state)
    machine = MachineSimulator(machine_def, input_tape)
    halt = False
    step_count = 1  # Track number of steps

    while machine.active_timelines and not halt:  # Run while there are active timelines
        print(f"\n{'='*30} STEP {step_count} {'='*30}")

        machine.step()  # Execute one step
        
        for timeline in machine.timelines:
            print("\n--- Machine Timeline ---")
            print(f"Step Count: {step_count}")
            print(f"Current State: {timeline.state}")
            print(f"Halted: {timeline.halt}")
            print(f"Accepted: {timeline.accept}")

            # Print all memory values
            print("\nMemory:")
            for key, value in timeline.memory.items():
                print(f"{key}: {value}")
                print(timeline.memory[key].view_ds())

            # Print input tape information
            print("\nInput Tape:")
            print(f"Memory: {timeline.input_tape}")
            print(f"Head Position: {timeline.input_tape.head_x}")
            print(f"Head Value: {timeline.input_tape.get_element()}")

            # Print transition history
            print("\nHistory:")
            for entry in timeline.history:
                print(entry)

            # Print output (if applicable)
            print("\nOutput:")
            print(timeline.output)

            # Check if this timeline has halted and accepted
            if timeline.halt and timeline.accept:
                print("\n*** Accepted Machine ***")
                halt = True  # Stop execution if accepted
                
        if halt:
            print("\n*** Machine Accepted ***")
            break

        step_count += 1  # Increment step count
        input("\nPress Enter to continue...")

    # Final summary of timelines
    print("\n\nFinal Timelines:")
    for timeline in machine.timelines:
        print("\n--- Final State ---")
        print(f"State: {timeline.state}")
        print(f"Halted: {timeline.halt}")
        print(f"Accepted: {timeline.accept}")

    print("\nActive Timelines:", machine.active_timelines)
    print("Accepted Timelines:", machine.accepted_timelines)
