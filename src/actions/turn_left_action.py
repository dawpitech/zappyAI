from .action import Action

class TurnLeftAction(Action):
    def __init__(self):
        super().__init__("turn_left", cost=1)
        self.preconditions = {}

    def apply(self, state):
        direction = state["dir"]
        directions = ["N", "W", "S", "E"]

        idx = directions.index(direction)
        new_dir = directions[(idx + 1) % len(directions)]

        new_state = state.copy()
        new_state["dir"] = new_dir
        return new_state

    def execute(self, agent):
        print("Commande envoyée au serveur : Left")
        # agent.send_command("Left\n")
