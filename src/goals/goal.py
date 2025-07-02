class Goal:
    def __init__(self, name, priority=1):
        self.name = name
        self.priority = priority

    def is_reached(self, state):
        raise NotImplementedError()

    def update_priority(self, state):
        pass

    def __repr__(self):
        return f"<Goal {self.name} (priority={self.priority})>"
