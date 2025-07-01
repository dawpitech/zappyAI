class State:
    def __init__(self, conditions=None):
        self.conditions = conditions if conditions is not None else {
            "id": 0,
            "level": 1
        }

    def copy(self):
        return State(self.conditions.copy())

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
