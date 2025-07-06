from .action import Action

class IncantationAction(Action):
    INCANTATION_REQUIREMENTS = {
        1: {"players": 1, "linemate": 1},
        2: {"players": 2, "linemate": 1, "deraumere": 1, "sibur": 1},
        3: {"players": 2, "linemate": 2, "sibur": 1, "phiras": 2},
        4: {"players": 4, "linemate": 1, "deraumere": 1, "sibur": 2, "phiras": 1},
        5: {"players": 4, "linemate": 1, "deraumere": 2, "sibur": 1, "mendiane": 3},
        6: {"players": 6, "linemate": 1, "deraumere": 2, "sibur": 3, "phiras": 1},
        7: {"players": 6, "linemate": 2, "deraumere": 2, "sibur": 2, "mendiane": 2, "phiras": 2, "thystame": 1},
    }

    def __init__(self):
        super().__init__("Incantation", cost=300)
        self.level_target = None

    def execute(self, agent):
        print("===========================================there==============================================")
        agent.queue_command("Incantation")

    def is_applicable(self, state):
        level = state["level"]
        if level not in self.INCANTATION_REQUIREMENTS:
            return False

        requirements = self.INCANTATION_REQUIREMENTS[level]
        tile = state["map"].get_tile(*state["pos"])
        if not tile or tile["last_seen"] < state["tick"] - 71:
            return False

        for stone, qty in requirements.items():
            if stone == "players":
                continue
            if tile["stones"].get(stone, 0) < qty:
                return False

        same_level_players = sum(1 for p in tile["players"] if p == level)
        if same_level_players < requirements["players"]:
            return False

        return True

    def apply(self, state):
        new_state = state.copy()
        new_state["level"] += 1
        new_state["tick"] += self.cost
        new_state["inventory"]["food"] = max(0, new_state["inventory"].get("food", 0) - self.cost)
        return new_state

    def on_fail(self, state):
        return state

    def __repr__(self):
        return f"<IncantationAction level {self.level_target or '?'} (cost={self.cost})>"
