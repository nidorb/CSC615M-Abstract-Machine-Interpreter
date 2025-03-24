import graphviz

class StateDiagram:
    def __init__(self, logic, initial_state, filename="state_diagram"):
        self.logic = logic
        self.initial_state = initial_state
        self.filename = filename
        self.command_map = {
            "SCAN": "S",
            "SCAN LEFT": "SL",
            "SCAN RIGHT": "SR",
            "PRINT": "P",
            "READ": "R",
            "WRITE": "W",
            "LEFT": "L",
            "RIGHT": "R",
            "UP": "U",
            "DOWN": "D"
        }
        self.build_graph()

    def build_graph(self):
        dot = graphviz.Digraph(format="png")

        for state, data in self.logic.items():
            command = data["command"]
            state_label = self.command_map.get(command, command)
            if state == self.initial_state:
                fillcolor = "green"
            elif state == "accept":
                fillcolor = "red"
            else:
                fillcolor = "yellow"

            dot.node(state, label=state_label, shape="circle", style="filled", fillcolor=fillcolor)

        # transitions
        for state, data in self.logic.items():
            transitions = data["transitions"]

            for edge_value, next_states in transitions.items():
                if isinstance(next_states, tuple):  # tape instruc
                    write_value, next_state = next_states
                    if edge_value == write_value:
                        label = f"{edge_value}"
                    else:
                        label = f"{edge_value}/{write_value}"
                    dot.edge(state, next_state, label=label)
                elif isinstance(next_states, list):  #mul states
                    for next_state in next_states:
                        dot.edge(state, next_state, label=edge_value)
                else:
                    dot.edge(state, next_states, label=edge_value)

        dot.render(self.filename, view=True)