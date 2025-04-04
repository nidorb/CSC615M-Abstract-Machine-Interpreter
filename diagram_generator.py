import graphviz

class StateDiagram:
    def __init__(self, logic, initial_state):
        self.logic = logic
        self.initial_state = initial_state
        self.command_map = {
            "SCAN": "S",
            "SCAN LEFT": "SL",
            "SCAN RIGHT": "SR",
            "PRINT": "P",
            "READ": "Rd",
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
                if isinstance(next_states, list):
                    for transition in next_states:
                        if isinstance(transition, tuple) and len(transition) == 2:
                            write_value, next_state = transition
                            label = f"{edge_value}/{write_value}" if edge_value != write_value else f"{edge_value}"
                            dot.edge(state, str(next_state), label=label)
                        else:
                            dot.edge(state, str(transition), label=edge_value)
                elif isinstance(next_states, tuple) and len(next_states) == 2:  # Single tuple case
                    write_value, next_state = next_states
                    label = f"{edge_value}/{write_value}" if edge_value != write_value else f"{edge_value}"
                    dot.edge(state, str(next_state), label=label)
                else:
                    dot.edge(state, str(next_states), label=edge_value)

        dot.render("./static/state_diagram")