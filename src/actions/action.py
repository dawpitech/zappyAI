class Action:
    def __init__(self, name, cost=1):
        self.name = name
        self.cost = cost
        self.preconditions = {}
        self.effects = {}

    def is_applicable(self, state):
        """
        Check if all preconditions are valid in the given state.
        """
        for key, value in self.preconditions.items():
            if key not in state or state[key] != value:
                return False
        return True

    def apply(self, state):
        """
        Apply the effects of the action to a copy of the given state.
        Do not modify the original state.
        """
        new_state = state.copy()
        for key, value in self.effects.items():
            new_state[key] = value
        return new_state

    def compute_cost(self, state):
        """
        Can be overridden by subclasses for a dynamic cost.
        By default, returns the fixed cost.
        """
        return self.cost

    def execute(self, agent):
        """
        To be implemented by subclasses: sends the actual command to the server.
        """
        raise NotImplementedError("Chaque action doit définir sa méthode execute().")

    def __repr__(self):
        return f"<Action {self.name} (cost={self.cost})>"
