from .goal import Goal
from .find_resources_goal import FindResourceGoal

class SurviveGoal(Goal):
    def __init__(self):
        super().__init__("Survive", priority=10)

    def is_reached(self, state):
        food = state["inventory"].get("food", 0)
        return food > 6000

    def update_priority(self, state):
        food = state["inventory"].get("food", 0)
        if food < 300:
            self.priority = 10
        elif food < 3000:
            self.priority = 6
        else:
            self.priority = 0
    
    def get_subgoal(self, state):
        food = state["inventory"].get("food", 0)
        if food < 6000:
            return FindResourceGoal("food")
        return None
