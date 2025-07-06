from .goal import Goal
from .have_required_resources_goal import HaveRequiredResourcesGoal
from .have_players_on_tile_goal import HavePlayersOnTileGoal

class ElevationGoal(Goal):
    def __init__(self):
        super().__init__(name=f"Elevate", priority=9)
        self.initial_level = 0

    def is_reached(self, state):
        return state["level"] >= self.initial_level + 1

    def update_priority(self, state):
        self.priority = 9

    def get_subgoal(self, state):
        if state["level"] != self.initial_level:
            return None

        if not self._has_required_resources(state):
            return HaveRequiredResourcesGoal(self.initial_level)
        return HavePlayersOnTileGoal(self.initial_level)

    def get_desired_state(self, state):
        self.initial_level = state["level"]
        return {"level": self.initial_level}

    def _has_required_resources(self, state):
        required = self._get_required_resources(self.initial_level)
        inv = state["inventory"]

        for res, count in required.items():
            if inv.get(res, 0) < count:
                return False
        return True

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
