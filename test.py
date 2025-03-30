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
B] WRITE(S2) (#,C), (#,D)
C] WRITE(S1) (X,D)
D] READ(S1) (X,E), (#,G), (#,F)
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

    input_tape = "1111"
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
                print(timeline.memory[key].view_ds())
                if timeline.memory[key].__class__.__name__ in {"Tape", "Tape2D"}:
                    print(timeline.memory[key].head_x)
                    print(timeline.memory[key].head_y)

            # Print input tape information
            print("\nInput Tape:")
            print(f"Memory: {timeline.input_tape}")
            print(f"Head Position x: {timeline.input_tape.head_x}")
            print(f"Head Position y: {timeline.input_tape.head_y}")
            print(f"Head Value: {timeline.input_tape.get_element()}")

            # Print transition history
            print("\nHistory:")
            print(timeline.history)

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
