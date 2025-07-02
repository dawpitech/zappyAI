from local_map import LocalMap

class State:
    def __init__(self, conditions=None, world_width=10, world_height=10):
        if conditions is not None:
            self.conditions = conditions.copy()
        else:
            self.conditions = {
                "id": 0,
                "level": 1,
                "pos": (0, 0),
                "dir": "N",
                "inventory": {},
                "map": LocalMap(world_width, world_height),
                "tick": 0,
            }


    def copy(self):
        new_conditions = self.conditions.copy()
        new_conditions["inventory"] = self.conditions["inventory"].copy()
        new_conditions["map"] = self.conditions["map"].clone()
        return State(new_conditions)

    def __getitem__(self, key):
        return self.conditions.get(key, None)

    def __setitem__(self, key, value):
        self.conditions[key] = value

    def __contains__(self, key):
        return key in self.conditions

    def __repr__(self):
        return f"State({self.conditions})"

    def to_tuple(self):
        return tuple(sorted(self.conditions.items()))
