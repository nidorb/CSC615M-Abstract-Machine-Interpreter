from flask import Flask, render_template, request, jsonify
from machine_simulator import MachineSimulator
from aux_data import InputTape
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

    try:
        # Initialize the parser and machine
        parser = MachineParser(machine_def, input_tape)
        machine = MachineSimulator(machine_def, input_tape)
        step_count = 0

        return jsonify({
            "machine_definition": machine_def,
            "input_value": input_tape,
            "initial_state": parser.initial_state,
            "memory": {key: str(value) for key, value in machine.memory.items()}
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
        step_count += 1

        # Get the first active timeline
        timeline = machine.timelines[0]
        input_tape = str(timeline.input_tape)
        print(input_tape)
        
        return jsonify({
            "input_value": input_tape,
            "current_state": timeline.state,
            "step_count": step_count,
            "output": timeline.output,
            "memory": {key: str(value) for key, value in machine.memory.items()}
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
