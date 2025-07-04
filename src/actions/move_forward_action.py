from .action import Action

class MoveForwardAction(Action):
    def __init__(self):
        super().__init__("move_forward", cost=7)
        self.preconditions = {}

    def execute(self, agent):
        print("Forward")
    
    def apply(self, state):
        x, y = state["pos"]
        direction = state["dir"]

        if direction == "N":
            y = (y - 1) % state["map"].height
        elif direction == "S":
            y = (y + 1) % state["map"].height
        elif direction == "E":
            x = (x + 1) % state["map"].width
        elif direction == "W":
            x = (x - 1) % state["map"].width

        new_state = state.copy()
        new_state["pos"] = (x, y)
        cost = self.compute_cost(state)
        new_state["inventory"]["food"] = max(0, new_state["inventory"].get("food", 0) - cost)
        new_state["tick"] += self.cost

        return new_state
