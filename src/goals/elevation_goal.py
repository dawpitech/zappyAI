from .goal import Goal
from .all_requirements_on_tile_goal import AllRequirementsOnTileGoal

class ElevationGoal(Goal):
    def __init__(self, initial_level):
        super().__init__(name=f"Elevate_to_{initial_level + 1}", priority=9)
        self.initial_level = initial_level

    def is_reached(self, state):
        return state["level"] >= self.initial_level + 1

    def update_priority(self, state):
        if state["level"] == self.initial_level:
            self.priority = 9
        else:
            self.priority = 0

    def get_subgoal(self, state):
        if state["level"] == self.initial_level:
            return AllRequirementsOnTileGoal(self.initial_level)
        return None

    def get_desired_state(self, state):
        return {"level": self.initial_level + 1}
