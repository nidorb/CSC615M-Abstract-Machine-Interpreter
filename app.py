from flask import Flask, render_template, request, jsonify
from machine_simulator import MachineSimulator
from aux_data import Tape, Tape2D, Queue, Stack
from diagram_generator import StateDiagram
from parser import MachineParser
import os

app = Flask(__name__)

# Store machine state globally
machine = None
step_count = 0

DEFAULT_MACHINE_DEF = """.DATA
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
K] LEFT(T3) (#/#,accept)"""

DEFAULT_INPUT = "abbcc"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset():
    global machine, step_count

    data = request.get_json()
    machine_def = data.get("machine_definition", DEFAULT_MACHINE_DEF)
    input_tape = data.get("user_input", DEFAULT_INPUT)
    head_indicator = "⬆"

    input_with_head = f"#{input_tape}#\n{head_indicator}" 

    try:
        # Initialize the parser and machine
        parser = MachineParser(machine_def, input_tape)
        machine = MachineSimulator(machine_def, input_tape)
        memory_str = {key: machine.memory[key].view_ds() for key, value in machine.memory.items()}
        
        return jsonify({
            "machine_definition": machine_def,
            "input_value": input_with_head,
            "head_x": machine.input_tape.head_x,
            "head_y": machine.input_tape.head_y,
            "initial_state": parser.initial_state,
            "memory": memory_str,
            "step_count": machine.step_count,
            "history": machine.history,
            "status": "Active"
        })

    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/step", methods=["POST"])
def step():
    global machine, step_count

    if not machine:
        return jsonify({"error": "Machine not initialized. Please reset first."}), 400

    if not machine.active_timelines:
        return jsonify({"error": "Machine has halted."}), 400

    try:
        machine.step()

        timelines_data = []
        for timeline in machine.timelines:
            if timeline.input_tape.head_y is not None:
                # 2D Tape Handling
                tape_str = timeline.input_tape.view_ds()
                rows = tape_str.split("\n")
                head_x, head_y = timeline.input_tape.head_x, timeline.input_tape.head_y
                
                if 0 <= head_y < len(rows):
                    head_row = " " * head_x + "⬆"
                    rows.insert(head_y + 1, head_row)
                input_with_head = "\n".join(rows)
            else:
                # 1D Tape Handling
                input_tape = str(timeline.input_tape)
                head_indicator = " " * timeline.input_tape.head_x + "⬆"
                input_with_head = f"{input_tape}\n{head_indicator}"
                
            memory_str = {key: timeline.memory[key].view_ds() for key, value in machine.memory.items()}
                                                
            if timeline.state == "accept":
                status = "Accepted"
            elif timeline.state == "reject":
                status = "Rejected"
            else:
                status = "Active"

            timelines_data.append({
                "input_value": input_with_head, 
                "current_state": timeline.state,
                "head_x": timeline.input_tape.head_x,
                "head_y": timeline.input_tape.head_y,
                "output": timeline.output,
                "memory": memory_str,
                "step_count": timeline.step_count,
                "history": timeline.history,
                "status": status
            })

        return jsonify({
            "timelines": timelines_data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400



@app.route("/diagram", methods=["POST"])
def diagram():
    data = request.get_json()
    machine_def = data.get("machine_definition", DEFAULT_MACHINE_DEF)
    input_tape = data.get("user_input", DEFAULT_INPUT)

    try:
        parser = MachineParser(machine_def, input_tape)
        StateDiagram(parser.logic, parser.initial_state)
        diagram_path = "static/state_diagram.png"

        return jsonify({"diagram_url": diagram_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
