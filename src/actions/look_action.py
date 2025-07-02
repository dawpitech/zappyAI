from .action import Action

class LookAction(Action):
    def __init__(self):
        super().__init__("Look", cost=1)

    def execute(self, agent):
        print("look")
        #agent.queue_command("Look")

    def update_map_from_look_response(self, state, response_str):
        tiles_str = response_str.strip("[] \n").split(',')

        tick = state["tick"]
        map_ = state["map"]
        pos_x, pos_y = state["pos"]
        direction = state["dir"]
        level = state["level"]

        visible_positions = get_visible_tiles_positions(pos_x, pos_y, direction, level, map_.width, map_.height)
        
        for i, tile_content in enumerate(tiles_str):
            stones = {}
            players = 0
            objects = tile_content.strip().split()

            for obj in objects:
                if obj == "player":
                    players += 1
                else:
                    stones[obj] = stones.get(obj, 0) + 1
            
            x, y = visible_positions[i]
            map_.update_tile(x, y, stones, players, tick)
        
        return state


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
            left = (0, -1)
        elif direction == 'W':
            forward = (-1, 0)
            left = (0, 1)
        else:
            raise ValueError(f"Direction inconnue {direction}")

        for dist in range(level + 1):
            center_x = (x + forward[0] * dist) % width
            center_y = (y + forward[1] * dist) % height

            for offset in range(-dist, dist + 1):
                tile_x = (center_x + left[0] * offset) % width
                tile_y = (center_y + left[1] * offset) % height
                positions.append((tile_x, tile_y))

        return positions
