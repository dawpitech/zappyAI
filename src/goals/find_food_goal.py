from .goal import Goal
from .explore_goal import ExploreGoal

class FindFoodGoal(Goal):
    def __init__(self):
        super().__init__("FindFood", priority=8)
        self.initial_food_amount = None

    def is_reached(self, state):
        current_food = state["inventory"].get("food", 0)
        if self.initial_food_amount is not None and current_food > self.initial_food_amount:
            return True
        return False

    def update_priority(self, state):
        if self.initial_food_amount is None:
            self.initial_food_amount = state["inventory"].get("food", 0)

    def get_subgoal(self, state):
        if not self._food_known_on_map(state):
            return ExploreGoal("food")
        return None

    def get_desired_state(self, state):
        best = self._find_nearest_food(state)
        if not best:
            return None
        desired = state.copy()
        desired["pos"] = best["pos"]
        return desired

    def _food_known_on_map(self, state):
        tick = state["tick"]
        game_map = state["map"]
        freshness_threshold = 71

        for tile in game_map.tiles.values():
            if tile["last_seen"] == -1 or tick - tile["last_seen"] > freshness_threshold:
                continue
            if tile["stones"].get("food", 0) > 0:
                return True
        return False

    def _find_nearest_food(self, state):
        from collections import deque

        tick = state["tick"]
        game_map = state["map"]
        pos = state["pos"]
        width = game_map.width
        height = game_map.height
        freshness_threshold = 71

        visited = set()
        queue = deque()
        queue.append((pos, 0))

        while queue:
            (x, y), dist = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))

            tile = game_map.get_tile(x, y)
            if tile and tile["last_seen"] != -1 and tick - tile["last_seen"] <= freshness_threshold:
                if tile["stones"].get("food", 0) > 0:
                    return {"pos": (x, y), "distance": dist}

            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx = (x + dx) % width
                ny = (y + dy) % height
                if (nx, ny) not in visited:
                    queue.append(((nx, ny), dist + 1))

        return None
