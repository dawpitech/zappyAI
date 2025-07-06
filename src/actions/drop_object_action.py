from .action import Action

class DropObjectAction(Action):
    def __init__(self, object_name):
        super().__init__(name=f"Drop_{object_name}", cost=7)
        self.object_name = object_name
        self.preconditions = {f"has_{object_name}": True}

    def execute(self, agent):
        agent.queue_command(f"Set {self.object_name}")

    def is_applicable(self, state):
        inv = state["inventory"]
        return inv.get(self.object_name, 0) > 0

    def apply(self, state):
        new_state = state.copy()
        inv = new_state["inventory"].copy()

        inv[self.object_name] = max(0, inv.get(self.object_name, 0) - 1)
        new_state["inventory"] = inv

        pos = state["pos"]
        tile = new_state["map"].get_tile(*pos).copy()
        stones = tile["stones"].copy()
        stones[self.object_name] = stones.get(self.object_name, 0) + 1
        tile["stones"] = stones
        new_state["map"].update_tile(*pos, stones=stones, players=tile["players"], tick=new_state["tick"])

        cost = self.compute_cost(state)
        new_state["inventory"]["food"] = max(0, new_state["inventory"].get("food", 0) - cost)
        new_state["tick"] += self.cost

        return new_state

    def on_fail(self, state):
        tile = state["map"].get_tile(*state["pos"])
        if tile:
            tile["last_seen"] = -1
        return state

    def __repr__(self):
        return f"<DropObjectAction {self.object_name} (cost={self.cost})>"
