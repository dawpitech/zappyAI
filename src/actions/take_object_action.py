from .action import Action

class TakeObjectAction(Action):
    def __init__(self, object_name):
        super().__init__(name=f"Take_{object_name}", cost=7)
        self.object_name = object_name
        self.preconditions = {f"tile_has_{object_name}": True}

    def is_applicable(self, state):
        pos = state["pos"]
        tile = state["map"].get_tile(*pos)
        if not tile:
            return False

        count = tile["stones"].get(self.object_name, 0)
        if count == 0:
            return False

        if tile["last_seen"] < state["tick"] - 20:
            return False

        return True

    def apply(self, state):
        new_state = state.copy()
        inv = new_state["inventory"].copy()

        if self.object_name == "food":
            inv["food"] = inv.get("food", 0) + 126
        else:
            inv[self.object_name] = inv.get(self.object_name, 0) + 1

        new_state["inventory"] = inv

        tile = new_state["map"].get_tile(*state["pos"]).copy()
        stones = tile["stones"].copy()
        stones[self.object_name] = max(0, stones.get(self.object_name, 1) - 1)
        tile["stones"] = stones
        new_state["map"].update_tile(*state["pos"], stones=stones, players=tile["players"], tick=new_state["tick"])
        cost = self.compute_cost(state)
        new_state["inventory"]["food"] = max(0, new_state["inventory"].get("food", 0) - cost)

        return new_state

    def execute(self, agent):
        print("Take")
        #agent.queue_command(f"Take {self.object_name}")

    def __repr__(self):
        return f"<TakeObjectAction {self.object_name} (cost={self.cost})>"
