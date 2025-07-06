from .goal import Goal
from .find_resources_goal import FindResourceGoal 

class HaveRequiredResourcesGoal(Goal):
    def __init__(self, level):
        super().__init__(name=f"HaveRequiredResources_L{level}", priority=8)
        self.level = level

    def is_reached(self, state):
        return self._has_required_resources(state)

    def get_desired_state(self, state):
        res = {"inventory": self._get_required_resources(self.level)}
        return {"inventory": self._get_required_resources(self.level)}

    def get_subgoal(self, state):
        required = self._get_required_resources(self.level)
        inv = state["inventory"]

        for res, qty in required.items():
            if inv.get(res, 0) < qty:
                return FindResourceGoal(res)
        return None

    def update_priority(self, state):
        self.priority = 8 if state["level"] == self.level else 0

    def _has_required_resources(self, state):
        required = self._get_required_resources(self.level)
        inv = state["inventory"]
        return all(inv.get(res, 0) >= qty for res, qty in required.items())

    def _get_required_resources(self, level):
        requirements = {
            1: {"linemate": 1},
            2: {"linemate": 1, "deraumere": 1, "sibur": 1},
            3: {"linemate": 2, "sibur": 1, "phiras": 2},
            4: {"linemate": 1, "deraumere": 1, "sibur": 2, "phiras": 1},
            5: {"linemate": 1, "deraumere": 2, "sibur": 1, "mendiane": 3},
            6: {"linemate": 1, "deraumere": 2, "sibur": 3, "phiras": 1},
            7: {"linemate": 2, "deraumere": 2, "sibur": 2, "mendiane": 2, "phiras": 2, "thystame": 1},
        }
        return requirements.get(level, {})
