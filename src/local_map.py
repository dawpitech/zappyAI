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
        self.tiles[(x, y)] = {
            "stones": stones,
            "players": players,
            "last_seen": tick
        }

    def get_tile(self, x, y):
        return self.tiles.get((x % self.width, y % self.height))

    def __repr__(self):
        return f"<LocalMap {self.width}x{self.height}>"
