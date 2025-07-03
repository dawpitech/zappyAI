from .action import Action

class MoveForwardAction(Action):
    def __init__(self):
        super().__init__("move_forward", cost=7)
        self.preconditions = {}  # Aucune condition particulière pour avancer
        # On ne définit pas d'effet fixe ici car la position dépend de la direction
    
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
        return new_state

    def execute(self, agent):
        print("Commande envoyée au serveur : Forward")
        # agent.send_command("Forward\n")