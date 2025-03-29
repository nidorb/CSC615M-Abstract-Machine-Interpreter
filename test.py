from machine_simulator import MachineSimulator
from aux_data import InputTape
from diagram_generator import StateDiagram
from parser import MachineParser

if __name__ == '__main__':
    machine_def = """
.DATA
TAPE T1
TAPE T2
TAPE T3
.LOGIC
A] RIGHT(T1) (a/a,B), (a/b,C)
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
            print("machine.memory", timeline.memory)
            for key, value in timeline.memory.items():
                print(f"{key}: {value}")
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
