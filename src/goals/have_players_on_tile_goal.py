from .goal import Goal
# from .find_players_goal import FindPlayersGoal  # supposé ou à créer

REQUIRED_PLAYERS = {
    1: 0,
    2: 1,
    3: 1,
    4: 3,
    5: 3,
    6: 5,
    7: 5,
}

class HavePlayersOnTileGoal(Goal):
    def __init__(self, level):
        super().__init__(name=f"HavePlayers_Level_{level}_on_tile", priority=6)
        self.level = level

    def is_reached(self, state):
        pos = state["pos"]
        tile = state["map"].get_tile(*pos)
        if not tile:
            return False

        # if not tile["last_seen"] == state["tick"] :
        #     return False

        required = REQUIRED_PLAYERS.get(self.level, 1)
        return tile["players"] == required + 1

    def get_subgoal(self, state):
        return None

    def update_priority(self, state):
        self.priority = 6 if state["level"] == self.level else 0

    def get_desired_state(self, state):
        return {f"players_on_tile_level_{self.level}": REQUIRED_PLAYERS.get(self.level, 1)}
