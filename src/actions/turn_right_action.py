from .action import Action

class TurnRightAction(Action):
    def __init__(self):
        super().__init__("turn_right", cost=7)
        self.preconditions = {}

    def apply(self, state):
        direction = state["dir"]
        directions = ["N", "E", "S", "W"]

        idx = directions.index(direction)
        new_dir = directions[(idx + 1) % len(directions)]

        new_state = state.copy()
        new_state["dir"] = new_dir
        cost = self.compute_cost(state)
        new_state["inventory"]["food"] = max(0, new_state["inventory"].get("food", 0) - cost)
        new_state["tick"] += self.cost
        return new_state

    def execute(self, agent):
        print("Commande envoyée au serveur : Right")
        # agent.send_command("Right\n")
