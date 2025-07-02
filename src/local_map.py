class LocalMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = {
            (x, y): {"stones": {}, "players": 0, "last_seen": -1}
            for x in range(width)
            for y in range(height)
        }

    def update_tile(self, x, y, stones, players, tick):
        x_mod = x % self.width
        y_mod = y % self.height
        self.tiles[(x_mod, y_mod)] = {
            "stones": stones,
            "players": players,
            "last_seen": tick
        }

    def get_tile(self, x, y):
        return self.tiles.get((x % self.width, y % self.height))
    
    def clone(self):
        new_map = LocalMap(self.width, self.height)
        new_map.tiles = {k: {"stones": v["stones"].copy(), "players": v["players"], "last_seen": v["last_seen"]}
                        for k, v in self.tiles.items()}
        return new_map

    def __repr__(self):
        return f"<LocalMap {self.width}x{self.height}>"
