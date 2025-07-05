from .action import Action

class LookAction(Action):
    def __init__(self):
        super().__init__("Look", cost=7)

    def execute(self, agent):
        agent.queue_command("Look")
    
    def apply(self, state):
        state["tick"] += self.cost
        pos = state["pos"]
        map_ = state["map"]
        tick = state["tick"]
        state["inventory"]["food"] = max(0, state["inventory"].get("food", 0) - self.cost)

        tile = map_.get_tile(*pos)
        if tile:
            tile["last_seen"] = tick

        return state
    
    def apply_agent(self, state, response_str):
        state["tick"] += self.cost
        state["inventory"]["food"] = max(0, state["inventory"].get("food", 0) - self.cost)

        self.update_map_from_look_response(state, response_str)

        return state

    def update_map_from_look_response(self, state, response_str):
        tiles_str = response_str.strip("[] \n").split(',')

        tick = state["tick"]
        map_ = state["map"]
        pos_x, pos_y = state["pos"]
        direction = state["dir"]
        level = state["level"]

        visible_positions = self.get_visible_tiles_positions(pos_x, pos_y, direction, level, map_.width, map_.height)

        for i, tile_content in enumerate(tiles_str):
            stones = {}
            players = 0
            objects = tile_content.strip().split()

            for obj in objects:
                if obj == "player":
                    players += 1
                else:
                    stones[obj] = stones.get(obj, 0) + 1

            if i < len(visible_positions):
                x, y = visible_positions[i]
                tile = map_.get_tile(x, y)
                if tile:
                    tile["last_seen"] = tick
                    map_.update_tile(x, y, stones, players, tick)

        return state

    @staticmethod
    def get_visible_tiles_positions(x, y, direction, level, width, height):
        positions = []

        if direction == 'N':
            forward = (0, -1)
            left = (-1, 0)
        elif direction == 'S':
            forward = (0, 1)
            left = (1, 0)
        elif direction == 'E':
            forward = (1, 0)
            left = (0, 1)
        elif direction == 'W':
            forward = (-1, 0)
            left = (0, -1)
        else:
            raise ValueError(f"Direction inconnue {direction}")

        for dist in range(level + 1):
            center_x = x + forward[0] * dist
            center_y = y + forward[1] * dist

            for offset in range(-dist, dist + 1):
                tile_x = (center_x + left[0] * offset) % width
                tile_y = (center_y + left[1] * offset) % height
                positions.append((tile_x, tile_y))

        return positions

