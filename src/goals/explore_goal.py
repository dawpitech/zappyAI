from .goal import Goal

class ExploreGoal(Goal):
    def __init__(self, resource_name: str, freshness_threshold=71, max_distance=5):
        super().__init__(f"Explore_{resource_name}", priority=4)
        self.resource_name = resource_name
        self.freshness_threshold = freshness_threshold
        self.max_distance = max_distance

    def is_reached(self, state):
        current_tile = state["map"].get_tile(*state["pos"])
        if current_tile and current_tile["last_seen"] == state["tick"]:
            return True
        return False


    def _resource_known_on_map(self, state):
        tick = state["tick"]
        game_map = state["map"]

        for tile in game_map.tiles.values():
            if tile["last_seen"] == -1 or tick - tile["last_seen"] > self.freshness_threshold:
                continue
            if tile["stones"].get(self.resource_name, 0) > 0:
                return True
        return False

    def _resource_known_on_map(self, state):
        tick = state["tick"]
        game_map = state["map"]

        for tile in game_map.tiles.values():
            if tile["last_seen"] == -1 or tick - tile["last_seen"] > self.freshness_threshold:
                continue
            if tile["stones"].get(self.resource_name, 0) > 0:
                return True
        return False


    def get_desired_state(self, state):
        best = self._find_best_explore_look(state)
        if not best:
            print("[DEBUG] Aucune position d'exploration intéressante trouvée.")
            return None

        desired = state.copy()
        desired["pos"] = best["pos"]
        desired["dir"] = best["dir"]
        return desired

    def _find_best_explore_look(self, state):
        from collections import deque

        visited = set()
        queue = deque()
        start_pos = state["pos"]
        queue.append((start_pos, []))
        visited.add(start_pos)

        best_score = -1
        best = None

        directions = ["N", "E", "S", "W"]
        tick = state["tick"]
        game_map = state["map"]
        width = game_map.width
        height = game_map.height
        level = state["level"]

        def get_visible_tiles(x, y, direction):
            forward = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}[direction]
            left = {"N": (-1, 0), "S": (1, 0), "E": (0, -1), "W": (0, 1)}[direction]
            positions = []

            for dist in range(level + 1):
                center_x = (x + forward[0] * dist) % width
                center_y = (y + forward[1] * dist) % height
                for offset in range(-dist, dist + 1):
                    tile_x = (center_x + left[0] * offset) % width
                    tile_y = (center_y + left[1] * offset) % height
                    positions.append((tile_x, tile_y))
            return positions

        def count_unseen(positions):
            return sum(
                1
                for x, y in positions
                if (tile := game_map.get_tile(x, y))
                and (tile["last_seen"] == -1 or tick - tile["last_seen"] > self.freshness_threshold)
            )

        while queue:
            (x, y), path = queue.popleft()
            if len(path) > self.max_distance:
                continue

            for dir in directions:
                visible = get_visible_tiles(x, y, dir)
                unseen_count = count_unseen(visible)
                cost = len(path) + 1
                score = unseen_count / cost if cost else 0

                if score > best_score:
                    best_score = score
                    best = {"pos": (x, y), "dir": dir, "score": score, "path": path}

            for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
                nx = (x + dx) % width
                ny = (y + dy) % height
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

        return best
